-- Schema do "Meu Dinheiro" — rodar uma vez (SQL editor do Neon no dashboard da Vercel,
-- ou: psql "$POSTGRES_URL_NON_POOLING" -f scripts/schema.sql)

create table if not exists config (
  id         smallint primary key default 1 check (id = 1),
  dados      jsonb not null,
  version    integer not null default 1,
  updated_at timestamptz not null default now()
);

create table if not exists meses (
  mes        text primary key,
  dados      jsonb not null,
  version    integer not null default 1,
  updated_at timestamptz not null default now()
);

create table if not exists historico (
  id        bigserial primary key,
  entidade  text not null,
  chave     text not null,
  dados     jsonb not null,
  version   integer not null,
  criado_em timestamptz not null default now()
);

create or replace function registra_historico_config() returns trigger as $$
begin
  insert into historico(entidade, chave, dados, version) values ('config', 'config', NEW.dados, NEW.version);
  return NEW;
end;
$$ language plpgsql;

create or replace function registra_historico_mes() returns trigger as $$
begin
  insert into historico(entidade, chave, dados, version) values ('mes', NEW.mes, NEW.dados, NEW.version);
  return NEW;
end;
$$ language plpgsql;

drop trigger if exists trg_config_historico on config;
create trigger trg_config_historico
  after insert or update on config
  for each row execute function registra_historico_config();

drop trigger if exists trg_meses_historico on meses;
create trigger trg_meses_historico
  after insert or update on meses
  for each row execute function registra_historico_mes();

insert into config (id, dados)
values (1, '{"saldo_inicial":0,"template_fixas":[],"poupanca":{"objetivo":"","meta_total":0,"depositos":[]}}'::jsonb)
on conflict (id) do nothing;
