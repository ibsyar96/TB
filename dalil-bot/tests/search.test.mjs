
import test from 'node:test';
import assert from 'node:assert/strict';
import {findEntries,formatDalil,normalize} from '../lib/dalil.js';
const corpus=[
 {slug:'a',category:'tajwid',topic:'Ikhfa haqiqi',aliases:['ikhfa'],verification_status:'reviewed',arabic_text:'صِفْ ذَا ثَنَا',meaning_ms:'Lima belas huruf',source_title:'تحفة الأطفال',source_author:'الجمزوري',source_verse:'16',source_url:'https://example.com'},
 {slug:'b',category:'makhraj',topic:'Makhraj dhad (ض)',aliases:['ض','dhad'],verification_status:'reviewed',arabic_text:'وَالضَّادُ',meaning_ms:'Sisi lidah',source_title:'الجزرية',source_author:'ابن الجزري',source_verse:'13',source_url:'https://example.com'},
 {slug:'c',category:'sifat',topic:'Hams',aliases:['hams'],verification_status:'draft',arabic_text:'x',meaning_ms:'x'}];
test('diacritics normalization',()=>assert.equal(normalize('الضَّادُ'),'الضاد'));
test('Malay query',()=>assert.equal(findEntries(corpus,'dalil ikhfa')[0].slug,'a'));
test('Arabic letter',()=>assert.equal(findEntries(corpus,'makhraj ض')[0].slug,'b'));
test('draft excluded',()=>assert.equal(findEntries(corpus,'sifat hams').length,0));
test('unknown query',()=>assert.equal(findEntries(corpus,'nonsense').length,0));
test('output includes citations',()=>{const s=formatDalil(corpus[0]);for(const t of ['صِفْ','Lima belas','تحفة الأطفال','16'])assert.ok(s.includes(t))});
