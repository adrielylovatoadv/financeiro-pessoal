// Importa o dados.json atual para o Postgres. Idempotente (upsert) — pode rodar de novo
// à vontade para ressincronizar com o estado mais recente do app antigo.
//
// Uso: node scripts/migrate.mjs [caminho-para-dados.json]
// Requer POSTGRES_URL (ou POSTGRES_URL_NON_POOLING / DATABASE_URL) no ambiente — rode
// `vercel env pull .env.local` antes, e carregue esse arquivo (ex: `node --env-file=.env.local scripts/migrate.mjs`).

import { readFileSync } from 'node:fs';
import { Client } from 'pg';

const path = process.argv[2] || new URL('../dados.json', import.meta.url);
const raw = JSON.parse(readFileSync(path, 'utf8'));

const connectionString =
  process.env.POSTGRES_URL_NON_POOLING || process.env.POSTGRES_URL || process.env.DATABASE_URL;
if (!connectionString) {
  console.error('Faltou POSTGRES_URL no ambiente. Rode `vercel env pull .env.local` e carregue o arquivo.');
  process.exit(1);
}

const client = new Client({ connectionString });
await client.connect();

try {
  await client.query('begin');

  const configDados = {
    saldo_inicial: raw.saldo_inicial ?? 0,
    template_fixas: raw.template_fixas ?? [],
    poupanca: raw.poupanca ?? { objetivo: '', meta_total: 0, depositos: [] },
  };
  await client.query(
    `insert into config (id, dados) values (1, $1::jsonb)
     on conflict (id) do update set dados = $1::jsonb, version = config.version + 1, updated_at = now()`,
    [JSON.stringify(configDados)]
  );

  const meses = raw.meses || {};
  for (const [mes, dados] of Object.entries(meses)) {
    await client.query(
      `insert into meses (mes, dados) values ($1, $2::jsonb)
       on conflict (mes) do update set dados = $2::jsonb, version = meses.version + 1, updated_at = now()`,
      [mes, JSON.stringify(dados)]
    );
  }

  await client.query('commit');
  console.log(`Migrado: config + ${Object.keys(meses).length} meses.`);
} catch (e) {
  await client.query('rollback');
  console.error('Falhou, rollback aplicado:', e);
  process.exit(1);
} finally {
  await client.end();
}
