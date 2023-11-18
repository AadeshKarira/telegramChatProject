const jwt = require('jsonwebtoken');
exports.create_token = async (_id) => {
    try{
        let token = jwt.sign({id:_id},process.env.JWT_KEY,{expiresIn:"30d"});
        return token;
    }catch (err) {
        return err
    }
  }
  