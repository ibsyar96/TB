import {timingSafeEqual} from 'node:crypto';

// Temporary authenticated setup route. Remove this file once the webhook is registered.
function safeEqual(a,b){
 if(typeof a!=='string'||typeof b!=='string'||!a||!b)return false;
 const left=Buffer.from(a),right=Buffer.from(b);
 return left.length===right.length&&timingSafeEqual(left,right);
}
export default async function handler(req,res){
 res.setHeader('Cache-Control','no-store');
 if(req.method!=='GET')return res.status(405).json({ok:false,error:'Method not allowed'});
 const supplied=req.query?.key;
 if(!safeEqual(supplied,process.env.WEBHOOK_SETUP_KEY)){
   return res.status(403).json({ok:false,error:'Forbidden'});
 }
 const token=process.env.TELEGRAM_BOT_TOKEN,secret=process.env.TELEGRAM_WEBHOOK_SECRET;
 if(!token||!secret)return res.status(503).json({ok:false,error:'Telegram environment variables missing'});
 try {
   const response=await fetch('https://api.telegram.org/bot'+token+'/setWebhook',{
     method:'POST',
     headers:{'Content-Type':'application/json'},
     body:JSON.stringify({
       url:'https://dalil-tajwid-bot.vercel.app/api/telegram',
       secret_token:secret,
       allowed_updates:['message'],
       drop_pending_updates:false
     }),
     signal:AbortSignal.timeout(8500)
   });
   const result=await response.json();
   return res.status(result.ok?200:502).json({
     ok:result.ok===true,
     description:typeof result.description==='string'?result.description.slice(0,160):'Unknown Telegram response',
     error_code:result.error_code||null
   });
 }catch(error){
   console.error('Webhook setup network failure: '+String(error.name));
   return res.status(502).json({ok:false,error:'Unable to contact Telegram'});
 }
}
