const express = require('express');
const jwt = require('jsonwebtoken');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = 3000;
const SECRET_KEY = 'your_secret_key'; // Replace with your own secret key

app.use(bodyParser.json());

// Serve JWKS file
app.get('/.well-known/jwks.json', (req, res) => {
    res.sendFile(path.join(__dirname, 'jwks.json'));
});

// Endpoint to generate a new JWT token
app.post('/generate', (req, res) => {
    const { username } = req.body;
    const token = jwt.sign({ username }, SECRET_KEY, { expiresIn: '1h', issuer: 'example.com' });
    res.json({ token });
});

// Endpoint to validate the JWT token
app.get('/validate', (req, res) => {
    const token = req.headers['authorization'];
    if (!token) {
        return res.status(403).send('Token is required');
    }

    jwt.verify(token.split(' ')[1], SECRET_KEY, (err, decoded) => {
        if (err) {
            return res.status(403).send('Invalid token');
        }
        res.json({ message: 'Token is valid', decoded });
    });
});

app.listen(PORT, () => {
    console.log(`JWT Issuer running on http://localhost:${PORT}`);
});
