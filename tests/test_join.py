import ast
import hashlib
import itertools
import json
import re
from pathlib import Path
from types import SimpleNamespace
import pytest

TREE = ast.parse(Path('contracts/ConsensusOuterJoin.py').read_text())
NS = {'json': json, 'hashlib': hashlib, 're': re, 'LABELS': ('SAME', 'DIFFERENT', 'UNKNOWN')}
exec(compile(ast.Module(body=[n for n in TREE.body if isinstance(n, ast.FunctionDef)
     and n.name not in ('fail', 'fetch_source')], type_ignores=[]), 'actual-helpers', 'exec'), NS)
CLEAN = [['SAME','DIFFERENT','DIFFERENT'], ['DIFFERENT','SAME','DIFFERENT'], ['DIFFERENT']*3]
DUP = [['SAME','SAME','DIFFERENT','DIFFERENT'], ['DIFFERENT','DIFFERENT','SAME','DIFFERENT'], ['DIFFERENT']*4]
LEFT = NS['parse_table'](Path('examples/left.json').read_text())
RIGHT = NS['parse_table'](Path('examples/right-clean.json').read_text())


@pytest.fixture
def join(direct_vm, direct_deploy, direct_alice):
    direct_vm.sender = direct_alice
    return direct_deploy('contracts/ConsensusOuterJoin.py')


def materialize(contract, vm, nonce='test', matrix=CLEAN, duplicate=False, bad_hash=False, http=200, body=None):
    vm.clear_mocks()
    left = Path('examples/left.json').read_bytes() if body is None else body
    name = 'right-duplicate.json' if duplicate else 'right-clean.json'
    right = Path('examples/' + name).read_bytes()
    vm.mock_web(r'.*/left\.json', {'status': http, 'body': left})
    vm.mock_web(r'.*/right-.*\.json', {'status': 200, 'body': right})
    if matrix is not None:
        vm.mock_llm(r'(?s).*INDEPENDENT RELATIONAL JOIN.*', json.dumps({'matrix': matrix}))
    return contract.materialize(nonce, 'mahdiaqal', 'consensus-outer-join', 'a'*40,
        'examples/left.json', '0'*64 if bad_hash else hashlib.sha256(left).hexdigest(),
        'examples/'+name, hashlib.sha256(right).hexdigest())


def test_full_outer_join_acquires_actual_bodies(join, direct_vm):
    key = materialize(join, direct_vm)
    record = join.get_materialization(key)
    assert record['status'] == 'MATERIALIZED'
    out = record['output']
    assert [(x['left']['id'], x['right']['id']) for x in out['joined']] == [('L1','R1'),('L2','R3')]
    assert [x['id'] for x in out['left_only']] == ['L3']
    assert [x['id'] for x in out['right_only']] == ['R4']
    assert not out['unresolved']
    for source in record['report']['sources']:
        assert source['body'] and source['hash'] == hashlib.sha256(source['body'].encode()).hexdigest()
    root = record.pop('root')
    assert root == NS['digest'](record)
    assert join.get_joined(key, root) == out['joined']
    with direct_vm.expect_revert('No matching materialized result'):
        join.get_joined(key, '0'*64)


def test_duplicate_aliases_not_arbitrarily_assigned(join, direct_vm):
    key = materialize(join, direct_vm, matrix=DUP, duplicate=True)
    out = join.get_materialization(key)['output']
    assert [(x['left']['id'],x['right']['id']) for x in out['joined']] == [('L2','R3')]
    assert out['unresolved'] == [{'left':['L1'], 'right':['R1','R2'], 'reason':'AMBIGUOUS'}]


def test_unknown_propagates_across_whole_component(join, direct_vm):
    matrix = [['SAME','UNKNOWN','DIFFERENT'], ['DIFFERENT','SAME','DIFFERENT'], ['DIFFERENT']*3]
    key = materialize(join, direct_vm, matrix=matrix)
    out = join.get_materialization(key)['output']
    assert not out['joined']
    assert out['unresolved'] == [{'left':['L1','L2'], 'right':['R1','R3'], 'reason':'UNKNOWN'}]


@pytest.mark.parametrize('kind', ['hash','http','schema','duplicate_id','encoding','oversize'])
def test_failed_evidence_blocks_all_joined_output(join, direct_vm, kind):
    body = None
    if kind == 'schema': body = b'{"schema":"wrong","rows":[]}'
    if kind == 'duplicate_id':
        body = json.dumps({'schema':'join-table-v1','rows':[LEFT[0], LEFT[0]]}).encode()
    if kind == 'encoding': body = b'\xff\xfe\xfa'
    if kind == 'oversize': body = b'x'*5121
    key = materialize(join, direct_vm, matrix=None, bad_hash=kind=='hash', http=503 if kind=='http' else 200, body=body)
    record = join.get_materialization(key)
    assert record['status'] == 'BLOCKED' and not record['report']['matrix']
    assert all(not values for values in record['output'].values())
    with direct_vm.expect_revert('No matching materialized result'):
        join.get_joined(key, record['root'])


def test_nonce_replay_and_author_namespace(join, direct_vm, direct_bob):
    first = materialize(join, direct_vm)
    with direct_vm.expect_revert('Materialization nonce used'):
        materialize(join, direct_vm)
    direct_vm.sender = direct_bob
    second = materialize(join, direct_vm)
    assert first != second


@pytest.mark.parametrize('matrix', [[], [['SAME']], [['SAME']*3]*2, [[True]*3]*3,
    [['same']*3]*3, [['UNKNOWN']*4]*3])
def test_invalid_ai_matrix_rejected(join, direct_vm, matrix):
    with direct_vm.expect_revert('Malformed or contradictory join matrix'):
        materialize(join, direct_vm, matrix=matrix)


@pytest.mark.parametrize('path', ['../secrets.json','/absolute.json','examples//a.json','examples/./a.json','https://bad.json','a%2fb.json'])
def test_source_path_escape_rejected(path):
    with pytest.raises(ValueError):
        NS['source_spec']('owner','repo','a'*40,path,'b'*64)


def test_exact_text_contradiction_rejected():
    with pytest.raises(ValueError):
        NS['parse_matrix']({'matrix':[['DIFFERENT']]}, [LEFT[0]], [LEFT[0]])


def test_duplicate_json_keys_rejected():
    with pytest.raises(ValueError):
        NS['parse_table']('{"schema":"join-table-v1","schema":"wrong","rows":[]}')


def test_forged_body_hash_rejected():
    spec = {'url':'https://raw.githubusercontent.com/o/r/'+'a'*40+'/t.json','sha256':'b'*64}
    row = {'url':spec['url'],'http':200,'status':'OK','hash':'b'*64,'body':Path('examples/left.json').read_text()}
    with pytest.raises(ValueError): NS['validate_source'](spec,row)


def test_actual_validator_rejects_semantic_and_binding_disagreement():
    cls = next(n for n in TREE.body if isinstance(n, ast.ClassDef))
    method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name=='materialize')
    fn = next(n for n in method.body if isinstance(n, ast.FunctionDef) and n.name=='validator')
    class Return:
        def __init__(self, data): self.calldata=data
    expected = {'binding':{'nonce':'x'},'sources':[{'body':'actual evidence'}], 'matrix':CLEAN}
    ns = dict(NS, gl=SimpleNamespace(vm=SimpleNamespace(Return=Return)), observe=lambda:expected)
    exec(compile(ast.Module(body=[fn], type_ignores=[]),'actual-validator','exec'),ns)
    assert ns['validator'](Return(expected))
    assert not ns['validator'](Return(dict(expected,matrix=[['UNKNOWN']*3]*3)))
    assert not ns['validator'](Return(dict(expected,binding={'nonce':'other'})))
    assert not ns['validator'](Return(dict(expected,sources=[{'body':'substituted'}])))
    assert not ns['validator'](object())


def test_exhaustive_partition_and_no_silent_ambiguity():
    left=[dict(LEFT[i],label='left'+str(i)) for i in range(3)]
    right=[dict(RIGHT[i],label='right'+str(i)) for i in range(3)]
    for labels in itertools.product(NS['LABELS'],repeat=9):
        matrix=[list(labels[i*3:(i+1)*3]) for i in range(3)]
        out=NS['outer_join'](left,right,matrix)
        lid=[x['left']['id'] for x in out['joined']]+[x['id'] for x in out['left_only']]
        rid=[x['right']['id'] for x in out['joined']]+[x['id'] for x in out['right_only']]
        for group in out['unresolved']:
            lid+=group['left'];rid+=group['right']
        assert sorted(lid)==sorted(x['id'] for x in left)
        assert sorted(rid)==sorted(x['id'] for x in right)
        for pair in out['joined']:
            i=next(i for i,x in enumerate(left) if x['id']==pair['left']['id'])
            j=next(j for j,x in enumerate(right) if x['id']==pair['right']['id'])
            assert matrix[i][j]=='SAME'
            assert sum(x!='DIFFERENT' for x in matrix[i])==1
            assert sum(row[j]!='DIFFERENT' for row in matrix)==1


def test_transposition_preserves_join_pairs():
    for labels in itertools.product(NS['LABELS'],repeat=4):
        matrix=[list(labels[:2]),list(labels[2:])]
        a=NS['outer_join'](LEFT[:2],RIGHT[:2],matrix)
        b=NS['outer_join'](RIGHT[:2],LEFT[:2],[list(x) for x in zip(*matrix)])
        assert {(x['left']['id'],x['right']['id']) for x in a['joined']} == {(x['right']['id'],x['left']['id']) for x in b['joined']}
