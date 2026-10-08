-- Run only on the new EzTajwid Supabase project.
create table if not exists public.dalil_tajwid_entries (
 slug text primary key,
 category text not null,
 topic text not null,
 aliases text[] not null default '{}',
 source_title text not null,
 source_author text not null,
 source_verse text not null,
 arabic_text text not null,
 meaning_ms text not null,
 source_url text not null,
 verification_status text not null default 'draft',
 created_at timestamptz not null default now()
);
alter table public.dalil_tajwid_entries enable row level security;
