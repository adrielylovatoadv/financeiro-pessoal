-- Cole tudo isto no Supabase: menu "SQL Editor" > "New query" > Run.

create extension if not exists pgcrypto;

create table if not exists public.wines (
  id          uuid primary key default gen_random_uuid(),
  name        text not null,
  producer    text,
  type        text,
  tasted_on   date,
  thumb       text,
  photo       text,
  created_by  text,
  created_at  timestamptz not null default now()
);

create table if not exists public.reviews (
  wine_id     uuid not null references public.wines(id) on delete cascade,
  who         text not null,
  rating      numeric(2,1) not null check (rating >= 0.5 and rating <= 5),
  comment     text,
  updated_at  timestamptz not null default now(),
  primary key (wine_id, who)
);

alter table public.wines   enable row level security;
alter table public.reviews enable row level security;

drop policy if exists "wines_all" on public.wines;
drop policy if exists "reviews_all" on public.reviews;
create policy "wines_all"   on public.wines   for all to anon using (true) with check (true);
create policy "reviews_all" on public.reviews for all to anon using (true) with check (true);

grant select, insert, update, delete on public.wines   to anon;
grant select, insert, update, delete on public.reviews to anon;
