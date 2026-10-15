import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const [baseArg,modulesArg]=process.argv.slice(2);
if(!baseArg||!modulesArg)throw new Error('Usage: node parse.mjs <evaluation-directory> <tool-directory-with-package.json>');
const base=path.resolve(baseArg);
const require=createRequire(path.join(path.resolve(modulesArg),'package.json'));
const {JSDOM}=require('jsdom');const dom=new JSDOM('<!doctype html><html><body></body></html>');
globalThis.window=dom.window;globalThis.document=dom.window.document;
const {default:mermaid}=await import(pathToFileURL(require.resolve('mermaid')).href);
mermaid.initialize({startOnLoad:false});
const result=[];
for(const run of ['outputs','repeat-outputs'])for(const condition of fs.readdirSync(path.join(base,run)).sort()){
 const dir=path.join(base,run,condition);
 for(const filename of fs.readdirSync(dir).filter(n=>n.endsWith('.md')).sort()){
  const raw=fs.readFileSync(path.join(dir,filename),'utf8');const blocks=[...raw.matchAll(/```mermaid\s*\n([\s\S]*?)```/g)];
  for(let i=0;i<blocks.length;i++){
   const record={file:path.relative(base,path.join(dir,filename)),block:i+1,render:'not_run'};
   try{await mermaid.parse(blocks[i][1]);record.syntax='passed';}catch(e){record.syntax='failed';record.error=String(e);}
   result.push(record);
  }
 }
}
const version=require('mermaid/package.json').version;
fs.writeFileSync(path.join(base,'syntax-results.json'),JSON.stringify({mermaid_version:version,results:result},null,2)+'\n');
console.log(JSON.stringify({version,total:result.length,passed:result.filter(r=>r.syntax==='passed').length,failures:result.filter(r=>r.syntax==='failed')},null,2));
if(result.some(r=>r.syntax==='failed'))process.exitCode=1;
