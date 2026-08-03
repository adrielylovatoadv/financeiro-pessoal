import { getPool } from '../lib/db.js';

function saoPauloParts(date) {
  const fmt = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Sao_Paulo',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
  const parts = Object.fromEntries(fmt.formatToParts(date).map((p) => [p.type, p.value]));
  return { mes: `${parts.year}-${parts.month}`, dia: parseInt(parts.day, 10) };
}

function fmtMoney(v) {
  return Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function fmtLancamento(l) {
  const parcela = l.parcela ? ` (${l.parcela})` : '';
  return `• ${l.descricao}${parcela} — ${fmtMoney(l.valor)}`;
}

export default async function handler(req, res) {
  if (process.env.CRON_SECRET) {
    if (req.headers.authorization !== `Bearer ${process.env.CRON_SECRET}`) {
      res.status(401).json({ error: 'unauthorized' });
      return;
    }
  }

  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;
  if (!token || !chatId) {
    res.status(500).json({ error: 'TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID não configurados' });
    return;
  }

  const hoje = saoPauloParts(new Date());
  const amanha = saoPauloParts(new Date(Date.now() + 86400000));
  const mesesChave = [...new Set([hoje.mes, amanha.mes])];

  const pool = getPool();
  const { rows } = await pool.query('select mes, dados from meses where mes = any($1)', [mesesChave]);

  const hojeVencem = [];
  const amanhaVencem = [];
  for (const row of rows) {
    const lancamentos = row.dados?.lancamentos || [];
    for (const l of lancamentos) {
      if (l.pago) continue;
      if (row.mes === hoje.mes && l.data === hoje.dia) hojeVencem.push(l);
      if (row.mes === amanha.mes && l.data === amanha.dia) amanhaVencem.push(l);
    }
  }

  if (!hojeVencem.length && !amanhaVencem.length) {
    res.status(200).json({ ok: true, enviado: false });
    return;
  }

  const linhas = [];
  if (hojeVencem.length) {
    linhas.push('🔴 *Vencem hoje:*');
    linhas.push(...hojeVencem.map(fmtLancamento));
  }
  if (amanhaVencem.length) {
    if (linhas.length) linhas.push('');
    linhas.push('🟡 *Vencem amanhã:*');
    linhas.push(...amanhaVencem.map(fmtLancamento));
  }

  const r = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: chatId, text: linhas.join('\n'), parse_mode: 'Markdown' }),
  });

  if (!r.ok) {
    const err = await r.text();
    console.error('telegram error', err);
    res.status(502).json({ error: 'falha ao enviar telegram', detail: err });
    return;
  }

  res.status(200).json({ ok: true, enviado: true, hoje: hojeVencem.length, amanha: amanhaVencem.length });
}
