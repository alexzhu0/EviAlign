"""Independent business receipt fixtures and adversarial binding checks."""
from copy import deepcopy
from contextlib import redirect_stdout
import hashlib
import importlib
from io import BytesIO, StringIO
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=True, allow_nan=False).encode('ascii')).hexdigest()


def request_fixture():
    return {'kind': 'business-action-request-v1', 'request_id': 'a' * 32,
            'challenge': 'b' * 64, 'issued_at': 1000, 'expires_at': 1300,
            'context': {'actor': 'acme_manager', 'tenant': 'acme', 'role': 'manager',
                        'auth_version': 1, 'policy_version': 1, 'world_id': 'c' * 32},
            'proposal': {'tool': 'approve_refund', 'args': {'request_id': 'r_1', 'decision': 'approved'}},
            'authorization': {'decision': 'permit', 'reason': 'allowed'},
            'resources': {'request_version': 1, 'order_version': 2, 'amount_cents': 100},
            'approval': {'actor': 'acme_manager', 'request_id': 'r_1', 'expires_at': 1200},
            'result_status': 'not_executed'}


def receipt(request):
    result = {'kind': 'business-action-evidence-v1', 'request_id': request['request_id'],
              'challenge': request['challenge'], 'result_status': 'not_executed',
              'request_digest': digest(request)}
    for field in ('context', 'proposal', 'authorization', 'resources', 'approval'):
        result[field + '_digest'] = digest(request[field])
    return result


class BusinessActionEvidenceTests(unittest.TestCase):
    def setUp(self):
        try:
            self.module = importlib.import_module('agentharness.business_action_evidence_v1')
        except ModuleNotFoundError:
            self.fail('business action evidence verifier is not implemented')
        self.request = request_fixture()
        self.evidence = receipt(self.request)

    def verify(self, request=None, evidence=None, now=1000):
        report = self.module.verify_business_action_evidence_v1(
            self.request if request is None else request,
            self.evidence if evidence is None else evidence, now=now)
        self.assertEqual(report['result_status'], 'not_executed')
        self.assertEqual(set(report), {'kind', 'ok', 'code', 'result_status'})
        return report

    def test_independent_receipt_and_builder_agree(self):
        self.assertTrue(self.verify()['ok'])
        self.assertEqual(self.module.build_evidence(self.request), self.evidence)
        self.assertEqual(self.module.canonical_digest({'z': '中文', 'a': 1}), digest({'a': 1, 'z': '中文'}))

    def test_every_current_call_component_is_bound(self):
        changes = [('request_id', 'd' * 32), ('challenge', 'e' * 64),
                   ('issued_at', 999), ('expires_at', 1299)]
        for key, value in changes:
            request = deepcopy(self.request)
            request[key] = value
            self.assertFalse(self.verify(request=request)['ok'])
        for section in ('context', 'proposal', 'authorization', 'resources', 'approval'):
            for key, value in self.request[section].items():
                request = deepcopy(self.request)
                request[section][key] = value + 1 if type(value) is int else 'changed'
                with self.subTest(section=section, key=key):
                    self.assertFalse(self.verify(request=request)['ok'])
        request = deepcopy(self.request)
        request['proposal']['args']['request_id'] = 'r_2'
        self.assertEqual(self.verify(request=request)['code'], 'business_action.binding_invalid')

    def test_each_receipt_field_is_checked(self):
        for key in self.evidence:
            for mode in ('remove', 'change', 'extra'):
                evidence = deepcopy(self.evidence)
                if mode == 'remove':
                    del evidence[key]
                elif mode == 'change':
                    evidence[key] = 'f' * 64
                else:
                    evidence['extra'] = 'secret'
                self.assertFalse(self.verify(evidence=evidence)['ok'])

    def test_freshness_boundaries_and_integer_types(self):
        for now, expected in ((999, False), (1000, True), (1299, True), (1300, False),
                              (True, False), (1000.0, False), (-1, False)):
            self.assertEqual(self.verify(now=now)['ok'], expected)

    def test_denial_never_becomes_positive_evidence(self):
        self.request['authorization']['decision'] = 'deny'
        self.evidence = receipt(self.request)
        self.assertEqual(self.verify()['code'], 'business_action.policy_denied')

    def test_strict_request_envelope_and_finite_tools(self):
        mutations = [(('kind',), 'data-access-request-v1'), (('extra',), 'secret'),
                     (('result_status',), 'executed'), (('expires_at',), 1400),
                     (('context', 'auth_version'), True), (('context', 'policy_version'), -1),
                     (('context', 'actor'), '/home/secret'), (('context', 'world_id'), ''),
                     (('context', 'extra'), 'x'), (('proposal', 'tool'), 'shell'),
                     (('proposal', 'args'), []), (('authorization', 'decision'), 'allow'),
                     (('authorization', 'reason'), '/home/secret'), (('resources',), []),
                     (('approval',), []), (('request_id',), 'A' * 32)]
        for path, value in mutations:
            request = deepcopy(self.request)
            target = request
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            with self.subTest(path=path, value=value):
                self.assertEqual(self.verify(request=request)['code'], 'business_action.request_invalid')
                with self.assertRaisesRegex(ValueError, '^business_action.request_invalid$'):
                    self.module.build_evidence(request)
        for tool in ('search_customers', 'list_orders', 'order_detail', 'list_shipments',
                     'list_tickets', 'finance_summary', 'search_documents', 'list_events',
                     'list_refund_requests', 'create_ticket', 'assign_ticket', 'request_refund', 'approve_refund'):
            self.request['proposal']['tool'] = tool
            self.assertTrue(self.verify(evidence=receipt(self.request))['ok'])

    def test_bounded_json_rejects_ambiguous_objects_without_disclosure(self):
        cyclic = {}; cyclic['cycle'] = cyclic
        nested = {}
        for _ in range(15):
            nested = {'nested': nested}
        for value in (float('nan'), float('inf'), 2**70, b'secret', cyclic, nested,
                      {'secret': 'x' * 20000}, list(range(65)), {str(i): i for i in range(65)}):
            request = deepcopy(self.request)
            request['proposal']['args'] = {'value': value}
            report = self.verify(request=request)
            self.assertFalse(report['ok'])
            self.assertNotIn('secret', json.dumps(report))
            with self.assertRaisesRegex(ValueError, '^business_action.json_invalid$'):
                self.module.canonical_digest(value)

    def run_cli(self, raw):
        output = StringIO()
        with patch.object(self.module.sys, 'stdin', SimpleNamespace(buffer=BytesIO(raw))), \
                redirect_stdout(output), patch.object(self.module.time, 'time', return_value=1000):
            code = self.module.main()
        return code, json.loads(output.getvalue())

    def test_cli_strict_json_and_bounded_single_output(self):
        raw = json.dumps({'request': self.request, 'evidence': self.evidence}).encode()
        code, report = self.run_cli(raw)
        self.assertEqual(code, 0)
        self.assertTrue(report['ok'])
        for raw in (b'{"request":{},"request":{},"evidence":{}}', b'{}{}', b'\xff',
                    b'{"request":NaN,"evidence":{}}', b'x' * 20000,
                    b'{"request":{},"evidence":{},"secret":"/home/alex/password"}'):
            code, report = self.run_cli(raw)
            self.assertEqual(code, 2)
            self.assertFalse(report['ok'])
            self.assertEqual(report['result_status'], 'not_executed')
            self.assertNotIn('secret', json.dumps(report))

    def test_internal_exception_is_fixed_error(self):
        with patch.object(self.module, 'canonical_digest', side_effect=RuntimeError('/home/secret')):
            self.assertEqual(self.verify()['code'], 'business_action.internal_error')


if __name__ == '__main__':
    unittest.main()
