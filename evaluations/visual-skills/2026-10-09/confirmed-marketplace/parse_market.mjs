import {JSDOM} from 'jsdom';
import fs from 'node:fs';
import path from 'node:path';
const dom=new JSDOM('<!doctype html><html><body></body></html>');
globalThis.window=dom.window;globalThis.document=dom.window.document;
const {default:mermaid}=await import('mermaid');mermaid.initialize({startOnLoad:false});
const dir='/tmp/ai-sdlc-market-mermaid/diagrams';const results=[];
for(const name of fs.readdirSync(dir).filter(x=>x.endsWith('.mmd')).sort()){
 try{await mermaid.parse(fs.readFileSync(path.join(dir,name),'utf8'));results.push({id:name,syntax:'passed',render:'not_attempted_existing_browser_policy_block'});}
 catch(e){results.push({id:name,syntax:'failed',render:'not_attempted_existing_browser_policy_block',error:String(e)});}
}
fs.writeFileSync('/tmp/ai-sdlc-market-mermaid/parse-results.json',JSON.stringify(results,null,2));console.log(JSON.stringify(results,null,2));
