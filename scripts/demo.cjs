const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),{spawnSync}=require('node:child_process');
const [mode,address,commit]=process.argv.slice(2);
if(!['clean','duplicate','badhash','replay'].includes(mode)||!/^0x[0-9a-fA-F]{40}$/.test(address??'')||! /^[0-9a-f]{40}$/.test(commit??''))throw Error('Mode, contract and pinned fixture commit required');
const right=mode==='duplicate'?'examples/right-duplicate.json':'examples/right-clean.json';
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(path.join(__dirname,'..',p))).digest('hex');
const nonce=mode==='replay'?'demo-clean':'demo-'+mode;
const args=[nonce,'mahdiaqal','consensus-outer-join',commit,'examples/left.json',mode==='badhash'?'f'.repeat(64):hash('examples/left.json'),right,hash(right)];
const result=spawnSync(process.execPath,[path.join(__dirname,'run-cli.cjs'),'write',address,'materialize','--args',...args],{windowsHide:true,stdio:'inherit'});
process.exitCode=result.status??1;
