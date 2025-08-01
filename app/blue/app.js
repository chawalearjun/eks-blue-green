const express = require('express');
const app = express();
app.get('/', (req, res) => res.send('<h1>Blue-Green Demo - Version BLUE</h1>'));
app.listen(3000, () => console.log('Running BLUE version'));
