
import {timingSafeEqual} from 'node:crypto';
import {findEntries,loadDalil,formatDalil} from '../lib/dalil.js';
const HELP='📖 BOT DALIL TAJWID\n\nTaip nama hukum atau minta dalil:\n• dalil ikhfa\n• makhraj ض\n• sifat hams\n• mad wajib muttasil\n\nArahan: /start /bantuan /kategori /sumber\n\nJawapan hanya daripada matan yang ada rujukan kitab.';
function verify(a,b){if(!a||!b)return false;const aa=Buffer.from(String(a)),bb=Buffer.from(String(b));return aa.length===bb.length&&timingSafeEqual(aa,bb);}
async function send(token,chatId,text){
 const r=await fetch('https://api.telegram.org/bot'+token+'/sendMessage',{
 method:'POST',headers:{'content-type':'application/json'},
 body:JSON.stringify({chat_id:chatId,text:text.slice(0,4000),link_preview_options:{is_disabled:true}}),
 signal:AbortSignal.timeout(7000)});
 if(!r.ok)throw Error('TELEGRAM_SEND_'+r.status);
}
export default async function handler(req,res){
 if(req.method!=='POST')return res.status(405).json({error:'Method not allowed'});
 const token=process.env.TELEGRAM_BOT_TOKEN,secret=process.env.TELEGRAM_WEBHOOK_SECRET;
 if(!token||!secret)return res.status(503).json({error:'Telegram not yet configured'});
 if(!verify(req.headers['x-telegram-bot-api-secret-token'],secret))return res.status(403).json({error:'Forbidden'});
 const msg=req.body?.message;
 if(!msg?.chat?.id||typeof msg.text!=='string')return res.status(200).json({ok:true,ignored:true});
 const chat=msg.chat.id,txt=msg.text.trim().slice(0,120),cmd=txt.split(' ')[0].toLowerCase().split('@')[0];
 try{
  if(['/start','/bantuan','/help'].includes(cmd))await send(token,chat,HELP);
  else if(cmd==='/sumber')await send(token,chat,'📚 Sumber: Al-Muqaddimah al-Jazariyyah (Ibn al-Jazari), Tuhfatul Atfal (al-Jamzuri). Setiap respons menyatakan kitab, bait dan pautan sumber. Ini matan ulama, bukan hadis.');
  else{
   const entries=await loadDalil();
   if(cmd==='/kategori'){
    const n={tajwid:0,makhraj:0,sifat:0};for(const e of entries){if(e.category in n)n[e.category]++;}
    await send(token,chat,'📚 DALIL TERSEDIA\n\nTajwid: '+n.tajwid+'\nMakhraj: '+n.makhraj+'\nSifat: '+n.sifat+'\n\nCuba: dalil ikhfa, makhraj ض, sifat hams.');
   }else{
    const search=txt.replace(/^\/dalil(?:@\w+)?\s*/i,'').replace(/^\/(makhraj|tajwid|sifat)(?:@\w+)?\s*/i,'$1 ');
    const found=findEntries(entries,search,3);
    if(!found.length)await send(token,chat,'Belum ada matan bersumber untuk kata kunci ini. Cuba istilah lebih khusus.\n\n'+HELP);
    else for(const e of found)await send(token,chat,formatDalil(e));
   }
  }
  return res.status(200).json({ok:true});
 }catch(e){console.error('Dalil Telegram:',e.message);return res.status(503).json({error:'Sementara gagal memproses mesej'});}
}
