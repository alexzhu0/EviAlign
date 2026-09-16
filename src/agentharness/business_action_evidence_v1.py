"""Pure, bounded business evidence correlation; never runtime authorization.

The runtime owns trusted requests, authentication, business validation, current
resource/approval checks and execution. Digests are unkeyed, not signatures.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import time

MAX_INPUT_BYTES = 16 * 1024
MAX_DEPTH = 12
TOOLS = frozenset(('search_customers', 'list_orders', 'order_detail', 'list_shipments',
                   'list_tickets', 'finance_summary', 'search_documents', 'list_events',
                   'list_refund_requests', 'create_ticket', 'assign_ticket',
                   'request_refund', 'approve_refund'))
_NAME = re.compile(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}', re.ASCII)
_HEX32 = re.compile(r'[0-9a-f]{32}', re.ASCII)
_HEX64 = re.compile(r'[0-9a-f]{64}', re.ASCII)
_SECTIONS = ('context', 'proposal', 'authorization', 'resources', 'approval')
_REQUEST_KEYS = {'kind', 'request_id', 'challenge', 'issued_at', 'expires_at',
                 'result_status', *_SECTIONS}
_CONTEXT_KEYS = {'actor', 'tenant', 'role', 'auth_version', 'policy_version', 'world_id'}
_DIGEST_KEYS = ('request_digest', *(field + '_digest' for field in _SECTIONS))
_EVIDENCE_KEYS = {'kind', 'request_id', 'challenge', 'result_status', *_DIGEST_KEYS}


def _json_text(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False)


def _bounded(value):
    pending = [(value, 0)]
    nodes = 0
    while pending:
        item, depth = pending.pop()
        nodes += 1
        if depth > MAX_DEPTH or nodes > 2048:
            return False
        if type(item) is dict:
            if len(item) > 64 or any(type(key) is not str or len(key) > 64 for key in item):
                return False
            pending.extend((child, depth + 1) for child in item.values())
        elif type(item) is list:
            if len(item) > 64:
                return False
            pending.extend((child, depth + 1) for child in item)
        elif type(item) is str:
            if len(item) > MAX_INPUT_BYTES:
                return False
        elif type(item) is int:
            if item.bit_length() > 63:
                return False
        elif type(item) is float:
            if not math.isfinite(item):
                return False
        elif item is not None and type(item) is not bool:
            return False
    return len(_json_text(value)) <= MAX_INPUT_BYTES


def canonical_digest(value):
    """SHA-256 over bounded sorted compact ASCII JSON, without normalization."""
    try:
        if _bounded(value):
            return hashlib.sha256(_json_text(value).encode('ascii')).hexdigest()
    except Exception:
        pass
    raise ValueError('business_action.json_invalid') from None


def _keys(value, keys):
    return type(value) is dict and value.keys() == keys


def _matches(value, pattern):
    return type(value) is str and pattern.fullmatch(value) is not None


def _integer(value, minimum=0):
    return type(value) is int and minimum <= value <= 2**63 - 1


def _request_valid(value):
    if not _bounded(value) or not _keys(value, _REQUEST_KEYS):
        return False
    if (value['kind'] != 'business-action-request-v1'
            or value['result_status'] != 'not_executed'
            or not _matches(value['request_id'], _HEX32)
            or not _matches(value['challenge'], _HEX64)
            or not _integer(value['issued_at']) or not _integer(value['expires_at'])
            or value['expires_at'] - value['issued_at'] != 300):
        return False
    context, proposal, authorization = (value[key] for key in _SECTIONS[:3])
    return (
        _keys(context, _CONTEXT_KEYS)
        and all(_matches(context[key], _NAME) for key in ('actor', 'tenant', 'role', 'world_id'))
        and all(_integer(context[key], 1) for key in ('auth_version', 'policy_version'))
        and _keys(proposal, {'tool', 'args'})
        and type(proposal['tool']) is str and proposal['tool'] in TOOLS
        and type(proposal['args']) is dict
        and _keys(authorization, {'decision', 'reason'})
        and authorization['decision'] in ('permit', 'deny')
        and _matches(authorization['reason'], _NAME)
        and type(value['resources']) is dict and type(value['approval']) is dict
    )


def _receipt(request):
    result = {'kind': 'business-action-evidence-v1', 'request_id': request['request_id'],
              'challenge': request['challenge'], 'result_status': 'not_executed',
              'request_digest': canonical_digest(request)}
    result.update((field + '_digest', canonical_digest(request[field])) for field in _SECTIONS)
    return result


def build_evidence(request):
    """Build an unsigned correlation receipt for a structurally valid request."""
    try:
        if _request_valid(request):
            return _receipt(request)
    except Exception:
        pass
    raise ValueError('business_action.request_invalid') from None


def _report(code):
    return {'kind': 'business-action-verification-v1', 'ok': code == 'ok',
            'code': 'business_action.' + code, 'result_status': 'not_executed'}


def verify_business_action_evidence_v1(request, evidence, *, now: int):
    """Check exact current-request correlation and issued_at <= now < expires_at.

Approval contents are bound, not interpreted; runtime owns their validity.
"""
    try:
        if not _integer(now) or not _request_valid(request):
            return _report('request_invalid')
        if not request['issued_at'] <= now < request['expires_at']:
            return _report('request_expired')
        if not (_bounded(evidence) and _keys(evidence, _EVIDENCE_KEYS)
                and evidence['kind'] == 'business-action-evidence-v1'
                and evidence['result_status'] == 'not_executed'
                and _matches(evidence['request_id'], _HEX32)
                and _matches(evidence['challenge'], _HEX64)
                and all(_matches(evidence[key], _HEX64) for key in _DIGEST_KEYS)):
            return _report('evidence_invalid')
        if evidence != _receipt(request):
            return _report('binding_invalid')
        return _report('ok' if request['authorization']['decision'] == 'permit' else 'policy_denied')
    except Exception:
        return _report('internal_error')


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError


def main():
    """Consume one bounded JSON envelope, emitting only a fixed evidence report."""
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError
        document = json.loads(raw.decode('utf-8'), object_pairs_hook=_unique_object,
                              parse_constant=_reject_constant)
        if not _bounded(document) or not _keys(document, {'request', 'evidence'}):
            raise ValueError
    except (ValueError, UnicodeError, RecursionError):
        report = _report('request_invalid')
    except Exception:
        report = _report('internal_error')
    else:
        try:
            report = verify_business_action_evidence_v1(document['request'], document['evidence'],
                                                        now=int(time.time()))
        except Exception:
            report = _report('internal_error')
    sys.stdout.write(_json_text(report) + '\n')
    return 0 if report['ok'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
