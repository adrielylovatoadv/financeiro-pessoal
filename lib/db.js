import { Pool } from 'pg';

const connectionString =
  process.env.POSTGRES_URL || process.env.POSTGRES_URL_NON_POOLING || process.env.DATABASE_URL;

let pool;
export function getPool() {
  if (!pool) {
    if (!connectionString) throw new Error('POSTGRES_URL não configurada');
    pool = new Pool({ connectionString, max: 3 });
  }
  return pool;
}

export async function withTransaction(fn) {
  const client = await getPool().connect();
  try {
    await client.query('begin');
    const result = await fn(client);
    await client.query('commit');
    return result;
  } catch (e) {
    await client.query('rollback');
    throw e;
  } finally {
    client.release();
  }
}
