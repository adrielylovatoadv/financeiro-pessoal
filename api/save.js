import { getPool, withTransaction } from '../lib/db.js';

const MES_RE = /^\d{4}-\d{2}$/;

class ConflictError extends Error {
  constructor(conflicts) {
    super('conflict');
    this.conflicts = conflicts;
  }
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'method not allowed' });
    return;
  }

  let body = req.body;
  if (typeof body === 'string') {
    try {
      body = JSON.parse(body);
    } catch {
      res.status(400).json({ error: 'json inválido' });
      return;
    }
  }
  if (!body || typeof body !== 'object') {
    res.status(400).json({ error: 'corpo inválido' });
    return;
  }

  const { config, meses } = body;
  if (meses) {
    for (const mes of Object.keys(meses)) {
      if (!MES_RE.test(mes)) {
        res.status(400).json({ error: `chave de mês inválida: ${mes}` });
        return;
      }
    }
  }

  try {
    const versions = await withTransaction(async (client) => {
      const conflicts = {};
      const newVersions = { meses: {} };

      if (config) {
        const r = await client.query(
          `update config set dados = $1::jsonb, version = version + 1, updated_at = now()
           where id = 1 and version = $2 returning version`,
          [JSON.stringify(config.dados), config.expectedVersion]
        );
        if (r.rowCount === 0) conflicts.config = true;
        else newVersions.config = r.rows[0].version;
      }

      for (const [mes, entry] of Object.entries(meses || {})) {
        if (entry.expectedVersion == null) {
          const r = await client.query(
            `insert into meses (mes, dados) values ($1, $2::jsonb)
             on conflict (mes) do nothing returning version`,
            [mes, JSON.stringify(entry.dados)]
          );
          if (r.rowCount === 0) {
            conflicts.meses = conflicts.meses || {};
            conflicts.meses[mes] = true;
          } else {
            newVersions.meses[mes] = r.rows[0].version;
          }
        } else {
          const r = await client.query(
            `update meses set dados = $1::jsonb, version = version + 1, updated_at = now()
             where mes = $2 and version = $3 returning version`,
            [JSON.stringify(entry.dados), mes, entry.expectedVersion]
          );
          if (r.rowCount === 0) {
            conflicts.meses = conflicts.meses || {};
            conflicts.meses[mes] = true;
          } else {
            newVersions.meses[mes] = r.rows[0].version;
          }
        }
      }

      if (Object.keys(conflicts).length) throw new ConflictError(conflicts);
      return newVersions;
    });

    res.status(200).json({ ok: true, versions });
  } catch (e) {
    if (e instanceof ConflictError) {
      const pool = getPool();
      const out = { ok: false, conflicts: {} };

      if (e.conflicts.config) {
        const r = await pool.query('select dados, version from config where id = 1');
        out.conflicts.config = { dados: r.rows[0].dados, version: r.rows[0].version };
      }
      if (e.conflicts.meses) {
        out.conflicts.meses = {};
        for (const mes of Object.keys(e.conflicts.meses)) {
          const r = await pool.query('select dados, version from meses where mes = $1', [mes]);
          if (r.rows[0]) out.conflicts.meses[mes] = { dados: r.rows[0].dados, version: r.rows[0].version };
        }
      }
      res.status(409).json(out);
      return;
    }
    console.error('save error', e);
    res.status(500).json({ error: 'erro ao salvar' });
  }
}
