-- EzTajwid-only schema: use in a dedicated NEW Supabase project, NOT TB/Tahsin.
BEGIN;
CREATE TABLE IF NOT EXISTS public.dalil_tajwid_entries (
 slug text PRIMARY KEY,
 category text NOT NULL CHECK(category IN ('tajwid','makhraj','sifat')),
 topic text NOT NULL,
 aliases text[] NOT NULL DEFAULT '{}',
 source_title text NOT NULL,
 source_author text NOT NULL,
 source_verse text NOT NULL,
 arabic_text text NOT NULL,
 meaning_ms text NOT NULL,
 source_url text NOT NULL CHECK(source_url LIKE 'https://%'),
 verification_status text NOT NULL DEFAULT 'draft' CHECK(verification_status IN ('draft','reviewed')),
 created_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.dalil_tajwid_entries ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.dalil_tajwid_entries FROM anon, authenticated;
GRANT SELECT ON public.dalil_tajwid_entries TO anon, authenticated;
CREATE POLICY "Public can read reviewed tajwid dalil" ON public.dalil_tajwid_entries
FOR SELECT TO anon, authenticated USING (verification_status='reviewed');
CREATE INDEX IF NOT EXISTS dalil_tajwid_category_topic_idx
ON public.dalil_tajwid_entries (category,topic);
COMMIT;
