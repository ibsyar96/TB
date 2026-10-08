
export function normalize(x) {
 return String(x||'').normalize('NFKD').replace(/\p{M}/gu,'').replace(/ـ/g,'').replace(/[أإآٱ]/g,'ا').replace(/ى/g,'ي').replace(/[^\p{L}\p{N}]+/gu,' ').toLowerCase().trim().replace(/\s+/g,' ');
}
const SKIP=new Set(['dalil','beri','berikan','bagi','nak','minta','apa','apakah','tentang','hukum','maksud','makna','matan','bait','teks','kitab','tolong','saya','aku','dan']);
export function findEntries(entries,query,limit=3){
 const q=normalize(query), words=q.split(' ').filter(Boolean);
 if(!q)return [];
 const cat=['tajwid','makhraj','sifat'].find(c=>words.includes(c));
 const terms=words.filter(w=>!SKIP.has(w)&&!['tajwid','makhraj','sifat'].includes(w));
 const requested=terms.join(' ');
 return entries.filter(e=>e.verification_status==='reviewed'&&(!cat||e.category===cat))
 .map(e=>{
  const title=normalize(e.topic), names=(e.aliases||[]).map(normalize), fields=[title,...names];
  let score=!terms.length&&cat?1:0;
  if(requested&&fields.some(s=>s===requested))score+=100;
  if(requested&&fields.some(s=>s.includes(requested)))score+=35;
  for(const t of terms){
   if(names.includes(t)||title.split(' ').includes(t))score+=22;
   else if(t.length>2&&fields.some(s=>s.includes(t)))score+=12;
   else if(t.length>2&&(normalize(e.arabic_text).includes(t)||normalize(e.meaning_ms).includes(t)))score+=2;
  }
  return {e,score};
 }).filter(x=>x.score>0).sort((a,b)=>b.score-a.score||a.e.topic.localeCompare(b.e.topic,'ms'))
 .slice(0,Math.max(1,Math.min(6,limit))).map(x=>x.e);
}
export function formatDalil(e){
 return '📖 '+e.topic+'\n\n📜 MATAN ARAB\n'+e.arabic_text+'\n\n🇲🇾 MAKSUD\n'+e.meaning_ms
  +'\n\n📚 KITAB: '+e.source_title+'\n✍️ PENGARANG: '+e.source_author
  +'\n🔖 BAIT: '+e.source_verse+'\n🔗 SUMBER TEKS: '+e.source_url
  +'\n\nNota: Ini matan ulama tajwid, bukan hadis.';
}
export async function loadDalil(){
 const url=process.env.SUPABASE_URL,key=process.env.SUPABASE_PUBLISHABLE_KEY;
 if(!url||!key)throw Error('SUPABASE_ENV_MISSING');
 const response=await fetch(url.replace(/\/$/,'')+'/rest/v1/dalil_tajwid_entries?select=slug,category,topic,aliases,source_title,source_author,source_verse,arabic_text,meaning_ms,source_url,verification_status&verification_status=eq.reviewed&limit=1000',
 {headers:{apikey:key,Accept:'application/json'},signal:AbortSignal.timeout(6000),cache:'no-store'});
 if(!response.ok)throw Error('SUPABASE_STATUS_'+response.status);
 const result=await response.json();if(!Array.isArray(result))throw Error('INVALID_DATABASE_RESPONSE');
 return result;
}
