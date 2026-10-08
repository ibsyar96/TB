
import {findEntries,loadDalil} from '../lib/dalil.js';
export default async function handler(req,res){
 if(req.method!=='GET')return res.status(405).json({error:'Method not allowed'});
 res.setHeader('Cache-Control','no-store');
 const q=String(req.query?.q||'').slice(0,120);
 if(!q.trim())return res.status(200).json({query:q,items:[]});
 try{const entries=await loadDalil();return res.status(200).json({query:q,total:entries.length,items:findEntries(entries,q,6)});}
 catch(e){console.error('Dalil search:',e.message);return res.status(503).json({error:'Pangkalan dalil tidak dapat diakses buat masa ini.'});}
}
