var mongoose = require("mongoose");
var Schema = mongoose.Schema;
var { ObjectId } = mongoose.Types;

const imageSchema = new mongoose.Schema(
  {
    srno: {
      type: Number,
      required: true,
    },
    image: {
      type: String,
      required: true,
    },
  }
);

const image = mongoose.model("image", imageSchema);

//insert home table
insertOne = async (query) => {
  try{
      const get = await image(query).save();
      return get;
  }catch (err) {
      return err
  }
}

//find all  = without pagination
find = async (match) => {
  try{
      const get = await image.find(match);
      return get;
  }catch (err) {
      return err
  }
}

//find by id
findOne = async (query) => {
  try{
      const get = await image.findOne(query);
      return get;
  }catch (err) {
      return err
  }
}

//with pagination
with_pagination = async (query) => {
  try{
      let limit = 8;
      let page = parseInt(query.page);
      let skipIndex = (page - 1) * limit;
      const get = await image.find();
      const get_paginated = await image.find().limit(limit).skip(skipIndex);

      let count = get.length;
      let pageCount = count / limit;

      let data = {pageCount,get_paginated, count}
      return data
  }
  catch (err) {
      return err
  }
}
//update home table
updateOne = async (query,update) => {
  try{
      const get = await image.updateOne(query,update);
      return get;
  }catch (err) {
      return err
  }
}

//delete home table
deleteOne = async (query) => {
  try{
      const get = await image.deleteOne(query);
      return get;
  }catch (err) {
      return
  }
}

module.exports = {
  insertOne,
  find,
  findOne,
  with_pagination,
  updateOne,
  deleteOne
}