import http from 'node:http';
import path from 'node:path';
import { readFile } from 'node:fs/promises';
import { config, ROOT } from './config.js';
import { getDb } from './db.js';
import { readBody, sendJson, sendError, notFound } from './http.js';
import './channels/line.js';
import './channels/mock.js';
import { handleChannelWebhook } from './routes/webhooks.js';
import { handleInternal, sseHandler } from './routes/internal.js';
import { handleAgencyCare } from './routes/agencyCare.js';

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml', '.ico': 'image/x-icon' };

async function serveStatic(res, pathname) {
  const rel = pathname === '/' ? 'index.html' : pathname.replace(/^\/+/, '');
  const filePath = path.join(ROOT, 'public', rel);
  // กัน path traversal: ไฟล์ต้องอยู่ใต้ public/ เท่านั้น
  if (!filePath.startsWith(path.join(ROOT, 'public') + path.sep)) throw notFound();
  let body;
  try { body = await readFile(filePath); } catch { throw notFound(`ไม่พบไฟล์ ${rel}`); }
  res.writeHead(200, {
    'content-type': MIME[path.extname(filePath)] || 'application/octet-stream',
    'content-length': body.length,
    'x-content-type-options': 'nosniff',
  });
  res.end(body);
}

export function createServer() {
  getDb();
  return http.createServer(async (req, res) => {
    const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
    const method = req.method || 'GET';

    try {
      if (url.pathname === '/internal/events' && method === 'GET') return sseHandler(req, res);

      if (method === 'POST' || method === 'PUT' || method === 'PATCH') {
        const { raw, json } = await readBody(req);
        req.rawBody = raw;
        req.body = json;
      }

      if (url.pathname.startsWith('/webhook/')) return await handleChannelWebhook(req, res, url);
      if (url.pathname.startsWith('/internal/')) return await handleInternal(req, res, url, method);
      if (url.pathname.startsWith('/api/v1/')) return await handleAgencyCare(req, res, url, method);
      if (url.pathname === '/healthz') return sendJson(res, 200, { ok: true });
      if (method === 'GET') return await serveStatic(res, url.pathname);

      throw notFound(`ไม่มี endpoint นี้: ${method} ${url.pathname}`);
    } catch (err) {
      if (!res.headersSent) sendError(res, err);
      else res.end();
    }
  });
}

const isMain = process.argv[1] && import.meta.url === `file://${path.resolve(process.argv[1])}`;
if (isMain) {
  const server = createServer();
  server.listen(config.port, () => {
    console.log(`\n  GTG Chat Inbox — prototype`);
    console.log(`  Inbox UI        http://localhost:${config.port}/`);
    console.log(`  Agency Care API http://localhost:${config.port}/api/v1/contacts  (ต้องมี X-API-Key)`);
    console.log(`  LINE webhook    POST http://localhost:${config.port}/webhook/line`);
    console.log(`  Mock webhook    POST http://localhost:${config.port}/webhook/mock`);
    console.log(`  LINE dry-run    ${config.line.dryRun ? 'เปิดอยู่ (ไม่ยิงออก LINE จริง)' : 'ปิด — จะส่งออก LINE จริง'}\n`);
  });
  const shutdown = () => { server.close(() => process.exit(0)); };
  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);
}
