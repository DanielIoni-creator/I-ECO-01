'use strict';

const fs = require('fs');
const path = require('path');

module.exports = function handler(req, res) {
  if (req.method !== 'GET') return res.status(405).send('Method not allowed');
  const html = fs.readFileSync(path.join(__dirname, '..', 'views', 'zargox.html'), 'utf8');
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'public, max-age=0, must-revalidate');
  return res.status(200).send(html);
};
