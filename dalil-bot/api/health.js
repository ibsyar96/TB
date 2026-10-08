
export default function handler(req,res){
 if(req.method!=='GET')return res.status(405).json({error:'Method not allowed'});
 return res.status(200).json({ok:true,name:'Dalil Tajwid',database_configured:!!(process.env.SUPABASE_URL&&process.env.SUPABASE_PUBLISHABLE_KEY),telegram_configured:!!(process.env.TELEGRAM_BOT_TOKEN&&process.env.TELEGRAM_WEBHOOK_SECRET)});
}
