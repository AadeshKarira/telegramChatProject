const express = require('express');
const app = express();
require('dotenv').config();
require('./config/db');
const cors = require('cors')
app.use(cors());
app.use(express.json({limit: '5mb'}));

const { image } = require('./src/');

app.use("/image",image);

app.use((req, res, next) => {
    res.status(404).json({
        message: 'Ohh you are lost, read the API documentation to find your way back home :)'
    })
})

app.listen(process.env.PORT, () => {
    console.log(`server running on PORT ${process.env.PORT}`);
})