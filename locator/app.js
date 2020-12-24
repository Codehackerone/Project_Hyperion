const express = require('express');
const path = require('path');
const ejsMate = require('ejs-mate');
const app = express();

app.engine('ejs', ejsMate);
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.static(path.join(__dirname, 'public')));
app.get('/:latitude/:longitude', (req, res) => {
    const { latitude, longitude } = req.params;
    res.render('home', { latitude, longitude });
})
const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Serving on port ${port}`)
})