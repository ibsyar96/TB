// Temporary fixed-target webhook setup. Delete immediately after successful registration.
export default async function handler(req,res){
 res.setHeader('Cache-Control','no-store');
 if(req.method!=='GET'||req.query?.key!=='eztajwid-register-once'){
   return res.status(403).json({ok:false,error:'Forbidden'});
 }
 const token=process.env.TELEGRAM_BOT_TOKEN,secret=process.env.TELEGRAM_WEBHOOK_SECRET;
 if(!token||!secret)return res.status(503).json({ok:false,error:'Bot token or webhook secret missing'});
 const base='https://api.telegram.org/bot'+token+'/';
 const url='https://dalil-tajwid-bot-tahsin-bot.vercel.app/api/telegram';
 try{
   const r=await fetch(base+'setWebhook',{
     method:'POST',headers:{'content-type':'application/json'},
     body:JSON.stringify({url,secret_token:secret,allowed_updates:['message'],drop_pending_updates:false}),
     signal:AbortSignal.timeout(8500)
   });
   const response=await r.json();
   if(response.ok!==true)return res.status(502).json({ok:false,error_code:response.error_code||0,description:String(response.description||'Telegram rejected webhook').slice(0,180)});
   const check=await fetch(base+'getWebhookInfo',{signal:AbortSignal.timeout(8500)});
   const info=await check.json();
   return res.status(200).json({ok:true,telegram:response.description||'Webhook registered',registered_url:info.result?.url||null,pending_update_count:info.result?.pending_update_count||0,last_error:info.result?.last_error_message||null});
 }catch(e){
   return res.status(502).json({ok:false,error:'Network error contacting Telegram'});
 }
}
