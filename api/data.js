import { getPool } from '../lib/db.js';

export default async function handler(req, res) {
  if (req.method !== 'GET') {
    res.status(405).json({ error: 'method not allowed' });
    return;
  }

  const pool = getPool();
  const [configRes, mesesRes] = await Promise.all([
    pool.query('select dados, version from config where id = 1'),
    pool.query('select mes, dados, version from meses'),
  ]);

  const configRow = configRes.rows[0];
  const meses = {};
  const mesesVersions = {};
  for (const row of mesesRes.rows) {
    meses[row.mes] = row.dados;
    mesesVersions[row.mes] = row.version;
  }

  res.status(200).json({
    saldo_inicial: configRow?.dados?.saldo_inicial ?? 0,
    template_fixas: configRow?.dados?.template_fixas ?? [],
    poupanca: configRow?.dados?.poupanca ?? { objetivo: '', meta_total: 0, depositos: [] },
    meses,
    _versions: { config: configRow?.version ?? 1, meses: mesesVersions },
  });
}
