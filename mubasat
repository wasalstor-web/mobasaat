#!/usr/bin/env node

/**
 * AI Agent - سكربت بسيط للسيرفر
 * يعمل كوكيل ذكي على سيرفرك ويتصل بالمنصة الرئيسية
 * 
 * التثبيت:
 * 1. ارفع هذا الملف على سيرفرك
 * 2. شغله بالأمر: node ai-agent-simple.js
 * 3. السكربت سيشتغل على المنفذ 3000
 */

const http = require('http');
const { exec } = require('child_process');
const crypto = require('crypto');

// ========== الإعدادات ==========
const PORT = process.env.PORT || 3000;
const API_KEY = process.env.API_KEY || crypto.randomBytes(32).toString('hex');

// الأوامر المسموح بها فقط (للأمان)
const ALLOWED_COMMANDS = [
  'ls', 'ls -la', 'ls -lh',
  'pwd', 'whoami', 'date', 'uptime',
  'df -h', 'free -m', 'top -bn1',
  'ps aux', 'netstat -tulpn',
  'pm2 list', 'pm2 status',
  'node --version', 'npm --version',
  'git --version'
];

// ========== السيرفر ==========
const server = http.createServer((req, res) => {
  // CORS Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  // ========== Health Check ==========
  if (req.url === '/health' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime()
    }));
    return;
  }

  // ========== Execute Command ==========
  if (req.url === '/execute' && req.method === 'POST') {
    // التحقق من API Key
    const authHeader = req.headers['authorization'];
    if (!authHeader || authHeader.replace('Bearer ', '') !== API_KEY) {
      res.writeHead(401, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Unauthorized' }));
      return;
    }

    let body = '';
    req.on('data', chunk => { body += chunk.toString(); });
    req.on('end', () => {
      try {
        const { command } = JSON.parse(body);
        
        // التحقق من الأمر
        if (!command) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Command is required' }));
          return;
        }

        // التحقق من القائمة المسموح بها
        const isAllowed = ALLOWED_COMMANDS.some(allowed => 
          command.trim() === allowed || command.trim().startsWith(allowed + ' ')
        );

        if (!isAllowed) {
          res.writeHead(403, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ 
            error: 'Command not allowed',
            allowedCommands: ALLOWED_COMMANDS
          }));
          return;
        }

        // تنفيذ الأمر
        exec(command, { timeout: 30000, maxBuffer: 1024 * 1024 }, (error, stdout, stderr) => {
          if (error) {
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ 
              success: false,
              error: error.message,
              stderr: stderr
            }));
            return;
          }

          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({
            success: true,
            output: stdout,
            stderr: stderr || null,
            timestamp: new Date().toISOString()
          }));
        });

      } catch (error) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Invalid JSON' }));
      }
    });
    return;
  }

  // ========== Not Found ==========
  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Not found' }));
});

// ========== تشغيل السيرفر ==========
server.listen(PORT, () => {
  console.log('=================================');
  console.log('🤖 AI Agent بدأ العمل!');
  console.log('=================================');
  console.log(`🌐 المنفذ: ${PORT}`);
  console.log(`🔑 API Key: ${API_KEY}`);
  console.log('');
  console.log('📝 احفظ هذا المفتاح واستخدمه في رأس Authorization');
  console.log('');
  console.log('✅ الأوامر المسموح بها:');
  ALLOWED_COMMANDS.forEach(cmd => console.log(`   - ${cmd}`));
  console.log('');
  console.log('🔗 الروابط:');
  console.log(`   - Health Check: http://localhost:${PORT}/health`);
  console.log(`   - Execute: http://localhost:${PORT}/execute`);
  console.log('=================================');
});

// معالجة الأخطاء
process.on('uncaughtException', (error) => {
  console.error('❌ خطأ:', error);
});

process.on('SIGTERM', () => {
  console.log('🛑 توقف السيرفر...');
  server.close(() => {
    console.log('✅ تم إيقاف السيرفر');
    process.exit(0);
  });
});
