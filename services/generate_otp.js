exports.generate_otp = async () => {
    try{
        var otp = Math.floor(1000 + Math.random() * 9000);
        return otp
    }catch (err) {
        return err
    }
}