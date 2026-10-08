import {lookup} from 'node:dns/promises';

const base='https://api.telegram.org/bot';
const host='dalil-tajwid-bot-tahsin-bot.vercel.app';
const target='https://'+host+'/api/telegram';

async function register() {
 if(process.env.VERCEL_ENV && process.env.VERCEL_ENV!=='production'){
  console.log('Telegram setup skipped for non-production build');
  return;
 }
 const token=process.env.TELEGRAM_BOT_TOKEN;
 const secret=process.env.TELEGRAM_WEBHOOK_SECRET;
 if(!token || !secret) throw new Error('Required Telegram env variables are missing');
 const post=async body=>{
  const response=await fetch(base+token+'/setWebhook',{
    method:'POST',
    headers:{'content-type':'application/json'},
    body:JSON.stringify(body),
    signal:AbortSignal.timeout(10000)
  });
  return response.json();
 };
 const request={url:target,secret_token:secret,allowed_updates:['message'],drop_pending_updates:false};
 let response=await post(request);
 if(!response.ok && /failed to resolve host/i.test(response.description||'')){
   const {address}=await lookup(host,{family:4});
   response=await post({...request,ip_address:address});
 }
 if(!response.ok)throw new Error('Telegram rejected webhook: '+String(response.description||response.error_code||'unknown').slice(0,120));
 console.log('EzTajwid Telegram webhook registered for '+target);
}
register().catch(err=>{console.error('EzTajwid setup failed: '+err.message);process.exitCode=1;});
