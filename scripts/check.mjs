import fs from 'node:fs';
import crypto from 'node:crypto';
import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
export const canonical=x=>x===null||typeof x!=='object'?JSON.stringify(x).replace(/[\u007f-\uffff]/g,c=>'\\u'+c.charCodeAt(0).toString(16).padStart(4,'0')):
 Array.isArray(x)?'['+x.map(canonical).join(',')+']':'{'+Object.keys(x).sort().map(k=>canonical(k)+':'+canonical(x[k])).join(',')+'}';
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
export const digest=x=>sha(canonical(x));
async function rpc(method,params){
 const r=await fetch('https://studio.genlayer.com/api',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({jsonrpc:'2.0',id:1,method,params}),signal:AbortSignal.timeout(20000)});
 if(!r.ok)throw Error('HTTP failure');const p=await r.json();if(p.error||p.result==null)throw Error('RPC failure');return p.result;
}
function outerJoin(left,right,matrix){
 const nl=left.length,nr=right.length,edges=Array.from({length:nl+nr},()=>[]);
 if(matrix.length!==nl||matrix.some(row=>!Array.isArray(row)||row.length!==nr||row.some(x=>!['SAME','DIFFERENT','UNKNOWN'].includes(x))))throw Error('Matrix shape/labels');
 for(let i=0;i<nl;i++)for(let j=0;j<nr;j++)if(matrix[i][j]!=='DIFFERENT'){edges[i].push(nl+j);edges[nl+j].push(i);}
 const seen=new Set(),out={joined:[],left_only:[],right_only:[],unresolved:[]};
 for(let seed=0;seed<nl+nr;seed++){
  if(seen.has(seed))continue;const todo=[seed],component=[];seen.add(seed);
  while(todo.length){const node=todo.pop();component.push(node);for(const neighbor of edges[node])if(!seen.has(neighbor)){seen.add(neighbor);todo.push(neighbor);}}
  const li=component.filter(x=>x<nl).sort((a,b)=>a-b),ri=component.filter(x=>x>=nl).map(x=>x-nl).sort((a,b)=>a-b);
  if(!ri.length)out.left_only.push(left[li[0]]);
  else if(!li.length)out.right_only.push(right[ri[0]]);
  else if(li.some(i=>ri.some(j=>matrix[i][j]==='UNKNOWN')))out.unresolved.push({left:li.map(i=>left[i].id),right:ri.map(j=>right[j].id),reason:'UNKNOWN'});
  else if(li.length===1&&ri.length===1)out.joined.push({left:left[li[0]],right:right[ri[0]]});
  else out.unresolved.push({left:li.map(i=>left[i].id),right:ri.map(j=>right[j].id),reason:'AMBIGUOUS'});
 }
 return out;
}
if(process.argv[1]?.endsWith('check.mjs'))try{
 const [mode,value,extra]=process.argv.slice(2);
 if(mode==='source'){
  const norm=x=>x.replace(/\r\n/g,'\n').trimEnd()+'\n';
  const actual=norm(Buffer.from(await rpc('gen_getContractCode',[value]),'base64').toString('utf8'));
  const local=norm(fs.readFileSync('contracts/ConsensusOuterJoin.py','utf8'));
  console.log(JSON.stringify({address:value,source_matches:actual===local,source_sha256:sha(actual)}));if(actual!==local)process.exitCode=1;
 }else if(mode==='state'){
  const client=createClient({chain:studionet}),summaries=[];
  const read=(functionName,args)=>client.readContract({address:value,functionName,args});
  for(const nonce of ['demo-clean','demo-duplicate','demo-badhash']){
   const key=digest({contract:value,creator:extra,nonce});
   const record=await read('get_materialization',[key]);const {root,...body}=record;
   if(digest(body)!==root||record.report.binding.contract!==value||record.report.binding.creator!==extra||record.report.binding.nonce!==nonce)throw Error('Root/identity mismatch');
   const sources=record.report.sources,specs=record.report.binding.sources;
   if(!Array.isArray(sources)||sources.length!==2||specs.length!==2)throw Error('Evidence vector');
   for(let i=0;i<2;i++){
    if(sources[i].url!==specs[i].url)throw Error('Source URL mismatch');
    if(sources[i].body&&sha(sources[i].body)!==sources[i].hash)throw Error('Byte hash mismatch');
    if(sources[i].status==='OK'&&(sources[i].http!==200||sources[i].hash!==specs[i].sha256))throw Error('Commitment/status mismatch');
   }
   if(record.status==='MATERIALIZED'){
    if(sources.some(s=>s.status!=='OK'))throw Error('Bad evidence materialized');
    const tables=sources.map(s=>JSON.parse(s.body).rows.sort((a,b)=>a.id.localeCompare(b.id)));
    if(canonical(outerJoin(...tables,record.report.matrix))!==canonical(record.output))throw Error('Partition mismatch');
    if(canonical(await read('get_joined',[key,root]))!==canonical(record.output.joined))throw Error('Consumer output mismatch');
   }else if(record.status==='BLOCKED'){
    if(sources.every(s=>s.status==='OK')||record.report.matrix.length||Object.values(record.output).some(x=>x.length))throw Error('Blocked output mismatch');
    let rejected=false;try{await read('get_joined',[key,root]);}catch(e){if(e.code!==-32000||e.details!=='execution failed')throw e;rejected=true;}
    if(!rejected)throw Error('Blocked consumer accepted');
   }else throw Error('Unknown materialization state');
   summaries.push({nonce,id:key,root,status:record.status,sources:sources.map(({body,...rest})=>rest),matrix:record.report.matrix,output:record.output});
  }
  console.log(JSON.stringify({address:value,roots_and_partitions_verified:true,materializations:summaries}));
 }else if(['success','error'].includes(mode)){
  let tx=await rpc('eth_getTransactionByHash',[value]);
  for(let i=0;tx.status!=='FINALIZED'&&i<15;i++){await new Promise(r=>setTimeout(r,2000));tx=await rpc('eth_getTransactionByHash',[value]);}
  const leader=tx.consensus_data?.leader_receipt?.find(x=>x.mode==='leader'),raw=leader?.genvm_result?.stderr||leader?.result;
  const decoded=typeof raw!=='string'?'':(/^[A-Za-z0-9+/]*={0,2}$/.test(raw)&&raw.length%4===0?Buffer.from(raw,'base64').toString('utf8'):raw);
  console.log(JSON.stringify({hash:value,address:tx.to_address??tx.to,status:tx.status,execution:leader?.execution_result,consensus:tx.result_name,...(extra?{expected_error_matched:decoded.includes(extra)}:{})}));
  if(tx.status!=='FINALIZED'||leader?.execution_result!==(mode==='error'?'ERROR':'SUCCESS')||tx.result_name!=='MAJORITY_AGREE'||(extra&&!decoded.includes(extra)))process.exitCode=1;
 }else throw Error('Unknown mode');
}catch{console.error('Sanitized verification failure; inspect history before rebroadcast');process.exitCode=1;}
