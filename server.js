const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const mime = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.json': 'application/json',
  '.ico': 'image/x-icon'
};

const root = __dirname;

http.createServer(function(req, res) {
  var rp = url.parse(req.url).pathname;
  // ensure forward slashes
  rp = rp.replace(/\\/g, '/');
  var fp = path.join(root, rp).replace(/\\/g, '/');
  if (fp.endsWith('/')) fp += 'index.html';

  fs.readFile(fp, function(err, data) {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404: ' + req.url);
      return;
    }
    var ext = path.extname(fp).toLowerCase();
    var headers = { 'Content-Type': mime[ext] || 'application/octet-stream' };
    // No cache for dev
    headers['Cache-Control'] = 'no-store, no-cache, must-revalidate';
    headers['Pragma'] = 'no-cache';
    headers['Expires'] = '0';
    res.writeHead(200, headers);
    res.end(data);
  });
}).listen(8096, '0.0.0.0', function() {
  console.log('Server running on http://localhost:8096');
});

// Keep alive
setInterval(function() {}, 60000);
