# Dalil Tajwid Bot

Separate Node.js application inside the existing GitHub repository, deployed as a NEW Vercel project with Root Directory = dalil-bot. This directory does not modify Tahsin code.

The answers are selected from reviewed rows in the existing Supabase project's dedicated public.dalil_tajwid_entries table. The table is protected with read-only RLS policies for anonymous users.

Production environment:
- SUPABASE_URL = existing project URL.
- SUPABASE_PUBLISHABLE_KEY = sb_publishable key (send via apikey header only).
- TELEGRAM_BOT_TOKEN = a NEW token obtained by the owner from BotFather.
- TELEGRAM_WEBHOOK_SECRET = a random secret, also configured when calling Telegram setWebhook.

Telegram webhook address: https://YOUR-NEW-PROJECT.vercel.app/api/telegram
Webhook must be set by the owner after saving the token and secret. Do not share tokens in GitHub or public chat.

Telegram commands: /start, /bantuan, /kategori, /sumber; examples include dalil ikhfa, makhraj ض, sifat hams.
Web search at / and /api/search?q=ikhfa. Health check at /api/health.
Tests: npm test.

Text is a scholarly tajwid matan, NOT prophetic hadith. Source editions can have textual variants; this is an initial transcribed corpus that should undergo scholarly proofreading before being advertised as fully exhaustive or critically authenticated.
