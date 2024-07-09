const express = require('express');
const jwt = require('jsonwebtoken');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;
const privateKey = fs.readFileSync(path.join(__dirname, 'keys', 'private_key.pem'));
const jwks = JSON.parse(fs.readFileSync(path.join(__dirname, 'keys', 'jwks.json')));

// Endpoint to serve JWKS
app.get('/.well-known/jwks.json', (req, res) => {
  res.json(jwks);
});

// Endpoint to issue JWT
app.post('/token', (req, res) => {
  const token = jwt.sign({ sub: "1234567890", name: "John Doe" }, privateKey, { algorithm: 'RS256', keyid: "1", expiresIn: '1h' });
  res.json({ token });
});

app.listen(port, () => {
  console.log(`JWT Issuer listening at http://localhost:${port}`);
});
