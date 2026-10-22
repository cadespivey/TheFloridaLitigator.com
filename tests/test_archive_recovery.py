import shutil
import subprocess
from pathlib import Path

import pytest


def test_archive_loading_recovers_retired_hash_and_fails_boundedly():
    node = shutil.which('node')
    if not node:
        pytest.skip('Node unavailable')
    script = r'''
const assert=require('node:assert/strict');
const {loadArchive}=require(process.argv[1]);
const url='https://example.org/site/assets/archive-1111111111111111.json';
const reply=(status,data)=>({status,ok:status===200,json:async()=>data});
(async()=>{
 let calls=[];
 assert.deepEqual(await loadArchive(url,async(...args)=>{calls.push(args);return reply(200,{current:true});}),{current:true});
 assert.equal(calls.length,1);
 for(const status of [404,410]){
  calls=[];const responses=[reply(status),reply(200,{archive:'archive-2222222222222222.json'}),reply(200,{recovered:true})];
  assert.deepEqual(await loadArchive(url,async(...args)=>{calls.push(args);return responses.shift();}),{recovered:true});
  assert.deepEqual(calls.slice(1),[
   ['https://example.org/site/assets/current-archive.json',{cache:'no-store'}],
   ['https://example.org/site/assets/archive-2222222222222222.json',{cache:'no-store'}]]);
 }
 for(const pointer of [reply(404),reply(200,{archive:'https://evil.test/a.json'}),reply(200,{archive:'../private.json'})]){
  calls=[];const responses=[reply(404),pointer];
  await assert.rejects(loadArchive(url,async(...args)=>{calls.push(args);return responses.shift();}));
  assert.equal(calls.length,2);
 }
 let responses=[reply(404),reply(200,{archive:'archive-2222222222222222.json'}),reply(404)];
 await assert.rejects(loadArchive(url,async()=>responses.shift()));assert.equal(responses.length,0);
 calls=[];await assert.rejects(loadArchive(url,async(...args)=>{calls.push(args);return reply(500);}));assert.equal(calls.length,1);
})().catch(error=>{console.error(error);process.exitCode=1;});
'''
    subprocess.run([node, '-e', script, str(Path('src/flwu/data/web/search.js').resolve())],
                   check=True, capture_output=True, text=True)
