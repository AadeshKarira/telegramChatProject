var mongoose = require("mongoose");
var Schema = mongoose.Schema;
var { ObjectId } = mongoose.Types;

const userSchema = new mongoose.Schema(
  {
    telegramId:{
      type: String,
      required: true,
    },
    name:{
      type: String,
      required: true,
    },
    gender:{
      type: String,
      required: true,
    },
    genderOfInterest:{
      type: String,
      required: true,
    },
    age: {
      type: Number,
      required: true,
    },
    location: {
      type: String,
      required: true,
    },
    image: {
      type: String
    },
  }
);

const user = mongoose.model("user", userSchema);

// //insert home table
// insertOne = async (query) => {
//   try{
//       const get = await user(query).save();
//       return get;
//   }catch (err) {
//       return err
//   }
// }

// //find all  = without pagination
// find = async (match) => {
//   try{
//       const get = await user.find(match);
//       return get;
//   }catch (err) {
//       return err
//   }
// }

// //find by id
// findOne = async (query) => {
//   try{
//       const get = await user.findOne(query);
//       return get;
//   }catch (err) {
//       return err
//   }
// }

// //with pagination
// with_pagination = async (query) => {
//   try{
//       let limit = 8;
//       let page = parseInt(query.page);
//       let skipIndex = (page - 1) * limit;
//       const get = await user.find();
//       const get_paginated = await user.find().limit(limit).skip(skipIndex);

//       let count = get.length;
//       let pageCount = count / limit;

//       let data = {pageCount,get_paginated, count}
//       return data
//   }
//   catch (err) {
//       return err
//   }
// }
// //update home table
// updateOne = async (query,update) => {
//   try{
//       const get = await user.updateOne(query,update);
//       return get;
//   }catch (err) {
//       return err
//   }
// }

// //delete home table
// deleteOne = async (query) => {
//   try{
//       const get = await user.deleteOne(query);
//       return get;
//   }catch (err) {
//       return
//   }
// }

module.exports = {
  user
}