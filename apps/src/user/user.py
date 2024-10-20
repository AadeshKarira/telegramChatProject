const express = require('express');
const router = express.Router();
const { ObjectId } = require("mongodb");
const logger = require('../../config/logger');
const user = require("../../models/user").user;
const { fileUploadViaBase64, fileUploadViaMultipart, deleteKey, deleteFolder } = require("../../services/s3");
/* API's for Admin */

//create image
router.post('/', async (req, res) => {
    try {
            let get_insert = await user(req.body).save();
            if (get_insert) {
                res.status(200).json({
                    status: true,
                    statusCode:200,
                    message: "user Registered",
                    data: get_insert
                });
            } else {
                res.status(200).json({
                    status: false,
                    statusCode: 400,
                    message: "something went wrong"
                });

            }
    } catch (err) {
        res.status(400).send({status: false, statusCode: 400, message: err.message})
    }
});

//find all user
router.get('/', async (req, res) => {
    try {
        const get = await user.find({});
        // const get ="hi";
        res.status(200).send({status: true, statusCode: 200, message: "find successfully", data: get});
    } catch (err) {
        res.status(400).send({status: false, statusCode: 400, message: err.message})
    }
});

module.exports = router;