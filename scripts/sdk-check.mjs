import assert from 'node:assert/strict';
import {abi} from 'genlayer-js';
for(const [name,args] of [['materialize',['n','mahdiaqal','consensus-outer-join','a'.repeat(40),'examples/left.json','b'.repeat(64),'examples/right-clean.json','c'.repeat(64)]],
 ['get_materialization',['a'.repeat(64)]],['get_joined',['a'.repeat(64),'b'.repeat(64)]]]){
 const data=abi.calldata.encode(abi.calldata.makeCalldataObject(name,args,{}));
 assert.deepEqual(abi.calldata.encode(abi.calldata.decode(data)),data);
}
console.log('3 SDK calldata roundtrips passed');
