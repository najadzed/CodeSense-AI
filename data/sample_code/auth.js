// auth.js - Express example
const express = require('express');
const app = express();

app.post('/login', (req, res) => {
  const { username } = req.body;
  if (username === 'admin') {
    res.json({ token: 'token123' });
  } else {
    res.status(401).json({ error: 'unauthorized' });
  }
});
module.exports = app;
    