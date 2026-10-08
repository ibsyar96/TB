import {createHash,timingSafeEqual} from 'node:crypto';
import {lookup} from 'node:dns/promises';
// One-time administration endpoint; remove immediately after Telegram confirms the webhook.
// No Telegram tokens or authorisation secrets are included in source code.
const fingerprint='a17c0c2183e85faf4fc4a5b15089baea';
const host='dalil-tajwid-bot-tahsin-bot.vercel.app';
const url='https://'+host+'/api/telegram';
const gate=x=>{
 if(typeof x!=='string')return false;
 const hash=createHash('md5').update(x).digest('hex');
 return timingSafeEqual(Buffer.from(hash),Buffer.from(fingerprint));
};
export default async function handler(req,res){
 res.setHeader('Cache-Control','private, no-store, max-age=0');
 if(req.method!=='POST')return res.status(405).json({ok:false,error:'Method not allowed'});
 if(!gate(req.headers['x-eztajwid-setup-key']))return res.status(403).json({ok:false,error:'Forbidden'});
 const token=process.env.TELEGRAM_BOT_TOKEN,secret=process.env.TELEGRAM_WEBHOOK_SECRET;
 if(!token||!secret)return res.status(503).json({ok:false,error:'Telegram environment not configured'});
 const tg=async (method,payload)=>{
  const response=await fetch('https://api.telegram.org/bot'+token+'/'+method,{
   method:payload?'POST':'GET',
   headers:{'content-type':'application/json'},
   body:payload?JSON.stringify(payload):undefined,
   signal:AbortSignal.timeout(9000)});
  return response.json();
 };
 try {
  const identity=await tg('getMe');
  if(!identity.ok)return res.status(502).json({ok:false,step:'getMe',error:identity.description||'Telegram rejected bot token'});
  const body={url,secret_token:secret,allowed_updates:['message'],drop_pending_updates:false};
  let setup=await tg('setWebhook',body);
  let usedIpFallback=false;
  if(!setup.ok&&/failed to resolve host/i.test(setup.description||'')){
   const ips=await lookup(host,{all:true,family:4});
   if(!ips.length)throw Error('Unable to resolve production host');
   setup=await tg('setWebhook',{...body,ip_address:ips[0].address});
   usedIpFallback=true;
  }
  if(!setup.ok)return res.status(502).json({ok:false,step:'setWebhook',telegram_message:String(setup.description||'Unknown').slice(0,200),ip_fallback:usedIpFallback});
  const info=await tg('getWebhookInfo');
  return res.status(info.ok?200:502).json({
   ok:info.ok===true&&info.result?.url===url,
   bot_username:identity.result?.username||null,
   registered_url:info.result?.url||null,
   pending_update_count:info.result?.pending_update_count??null,
   last_error_message:info.result?.last_error_message||null,
   ip_fallback:usedIpFallback,
   ip_address_configured:Boolean(info.result?.ip_address)
  });
 }catch(e){
  console.error('EzTajwid admin setup error:',e.name);
  return res.status(502).json({ok:false,error:'Webhook setup request failed'});
 }
}