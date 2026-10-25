#!/usr/bin/env python3
"""Executable semantic checks for Mandora decisions D1-D4; not a LinkML validator."""
from datetime import datetime
from pathlib import Path
import yaml

MODEL = Path(__file__).resolve().parents[1] / 'model' / 'mandora-core-prototype.yaml'

def parse(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00'))

def validate_party(party, parties):
    errors=[]
    status=party.get('status')
    target=party.get('merged_into_party_id')
    if status == 'merged' and not target: errors.append('merged party requires merged_into_party_id')
    if status != 'merged' and target: errors.append('non-merged party must not have merged_into_party_id')
    if target:
        if target == party.get('id'): errors.append('party cannot merge into itself')
        t=parties.get(target)
        if not t: errors.append('merge target does not exist')
        elif t.get('tenant_id') != party.get('tenant_id'): errors.append('merge target must belong to same tenant')
        seen={party.get('id')}; cur=target
        while cur and cur in parties:
            if cur in seen:
                errors.append('merge redirect cycle detected'); break
            seen.add(cur); cur=parties[cur].get('merged_into_party_id')
    return errors

def validate_role(role):
    errors=[]
    start=role.get('valid_from'); end=role.get('valid_to')
    if not start: errors.append('valid_from is required for temporal role')
    if end is not None and start:
        try:
            if parse(end) <= parse(start): errors.append('valid_to must be later than valid_from for [start, end)')
        except ValueError: errors.append('valid_from/valid_to must be ISO-8601 timestamps')
    return errors

def roles_overlap(a,b):
    # Caller must first establish same tenant, party, role_type and normalized context.
    a0=parse(a['valid_from']); b0=parse(b['valid_from'])
    a1=parse(a['valid_to']) if a.get('valid_to') else None
    b1=parse(b['valid_to']) if b.get('valid_to') else None
    return (b1 is None or a0 < b1) and (a1 is None or b0 < a1)

def run():
    model=yaml.safe_load(MODEL.read_text())
    declared=set(model.get('slots',{})); errors=[]
    for cname, cls in model.get('classes',{}).items():
        for slot in cls.get('slots',[]):
            if slot not in declared: errors.append(f'undeclared slot {cname}.{slot}')
    assert not errors, errors
    # D1: Tenant uses id as root identity and has no tenant_id slot.
    assert 'id' in model['classes']['Tenant']['slots']
    assert 'tenant_id' not in model['classes']['Tenant']['slots']
    # D2: event semantics are distinct; created_at is entity creation metadata.
    assert {'created_at','occurred_at','recorded_at'} <= declared
    assert 'occurred_at' in model['classes']['Event']['slots'] and 'recorded_at' in model['classes']['Event']['slots']
    assert 'created_at' in model['classes']['Party']['slots']
    # D3 positive and negative cases.
    parties={
      'p1': {'id':'p1','tenant_id':'t1','status':'merged','merged_into_party_id':'p2'},
      'p2': {'id':'p2','tenant_id':'t1','status':'active','merged_into_party_id':None},
    }
    assert validate_party(parties['p1'], parties)==[]
    assert validate_party({'id':'x','tenant_id':'t1','status':'merged'}, parties)
    assert validate_party({'id':'x','tenant_id':'t1','status':'active','merged_into_party_id':'p2'}, parties)
    assert validate_party({'id':'p2','tenant_id':'t1','status':'merged','merged_into_party_id':'p1'}, parties)
    assert validate_party({'id':'x','tenant_id':'t2','status':'merged','merged_into_party_id':'p2'}, parties)
    # D4 bounds and half-open overlap.
    assert validate_role({'valid_from':'2026-01-01T00:00:00Z','valid_to':'2026-02-01T00:00:00Z'})==[]
    assert validate_role({'valid_from':'2026-02-01T00:00:00Z','valid_to':'2026-02-01T00:00:00Z'})
    a={'valid_from':'2026-01-01T00:00:00Z','valid_to':'2026-02-01T00:00:00Z'}
    b={'valid_from':'2026-02-01T00:00:00Z','valid_to':'2026-03-01T00:00:00Z'}
    c={'valid_from':'2026-01-15T00:00:00Z','valid_to':'2026-02-15T00:00:00Z'}
    assert not roles_overlap(a,b) and roles_overlap(a,c)
    print('PASS: D1-D4 semantic reference checks (12 assertions); basic model slot-reference check passed.')
    print('LIMITATION: these checks are not LinkML validation, JSON Schema generation, database concurrency tests, or production security tests.')
if __name__=='__main__': run()
