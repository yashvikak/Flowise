-- =====================================================================
-- Portfolio IQ — projects table schema
-- Run once in Supabase (SQL Editor). Safe to commit: NO secrets here.
-- Documents the database structure so it can be recreated or reviewed.
-- =====================================================================

create table public.projects (
  id               uuid primary key default gen_random_uuid(),
  name             text          not null,
  manager          text,
  business_unit    text,
  status           text          not null default 'On Track'
                     check (status in ('On Track', 'At Risk', 'Delayed')),
  percent_complete integer       not null default 0
                     check (percent_complete between 0 and 100),
  -- Money as numeric(14,2) so amounts can include cents; must be >= 0.
  approved_budget  numeric(14,2) not null default 0
                     check (approved_budget >= 0),
  actual_spend     numeric(14,2) not null default 0
                     check (actual_spend >= 0),
  start_date       date,
  target_date      date,
  -- Empty for now; links a project to a logged-in user once we add auth.
  owner_id         uuid          references auth.users on delete cascade,
  created_at       timestamptz   not null default now(),
  updated_at       timestamptz   not null default now(),

  -- Target completion cannot be earlier than the start date (when both exist).
  constraint projects_dates_valid
    check (start_date is null or target_date is null or target_date >= start_date)
);

-- Automatically refresh "updated_at" whenever a row is edited.
create or replace function public.set_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger projects_set_updated_at
  before update on public.projects
  for each row execute function public.set_updated_at();

-- =====================================================================
-- Row Level Security (RLS)
-- =====================================================================
alter table public.projects enable row level security;

-- ⚠️ TEMPORARY PROTOTYPE POLICY — REPLACE BEFORE PRODUCTION ⚠️
-- No authentication yet, so there is no user identity to scope rows to.
-- This grants the public (anon) key full read/write. Granted to "anon"
-- ONLY, so it will NOT apply to logged-in ("authenticated") users once
-- auth is added. Acceptable ONLY for a learning prototype. Before going
-- live, DELETE this policy and add rules such as:
--     using (owner_id = auth.uid())   -- each user sees only their own rows
create policy "TEMP prototype: anon full access"
  on public.projects
  for all
  to anon
  using (true)
  with check (true);
