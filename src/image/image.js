const express = require('express');
const router = express.Router();
const { ObjectId } = require("mongodb");
const logger = require('../../config/logger');
const image = require("../../models/image");
const { fileUploadViaBase64, fileUploadViaMultipart, deleteKey, deleteFolder } = require("../../services/s3");

/* API's for Admin */

//create image
router.post('/', async (req, res) => {
    try {
        let get = await image.find({});
        let srno = get.length + 1;
        let temp = req.body.image;
        let file_path = "image/" + srno + ".jpg";
        let get_upload = await fileUploadViaBase64(file_path, temp);
        
            let query = {
                srno: srno,
                image: "xx-xx" + file_path
            }
            let get_insert = await image.insertOne(query);
            if (get_insert) {
                res.status(200).json({
                    status: true,
                    statusCode:200,
                    message: "Image inserted successfully",
                    data: get_insert
                });
            } else {
                res.status(200).json({
                    status: false,
                    statusCode: 400,
                    message: "Image not inserted"
                });

            }
    } catch (err) {
        res.status(400).send({status: false, statusCode: 400, message: err.message})
    }
});

//find all image
router.get('/', async (req, res) => {
    try {
        const get = await image.find({});
        res.status(200).send({status: true, statusCode: 200, message: "find successfully", data: get});
    } catch (err) {
        res.status(400).send({status: false, statusCode: 400, message: err.message})
    }
});

module.exports = router;