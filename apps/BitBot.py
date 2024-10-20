from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import json
import socket
import io
import os
from io import BytesIO
from config import db
from models.user import User  # Replace 'your_module_path' with the actual path to your models
from services import helper,s3
import base64


TOKEN: Final ='xxxxxxxxxxxxxxxxxxxxxxx'
BOT_USERNAME: Final ='@Starter_Bit_Bot'
URL = 'http://xxxxxxxxxxxxxx/'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello from Bits and pieces")


async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["steps"]="started"
    await update.message.reply_text("Please enter following following details using comma(,) as delimiter; name,gender,gender of interest,age,location");

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(socket.getfqdn())
    await update.message.reply_text(f"{socket.getfqdn()} Hello, how can I help you")

async def custome_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please send custome command")

async def file_upload_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["steps"]="fileUpload"
    await update.message.reply_text("Please upload profile picture")

def handel_response(text: str) -> str:
    processed: str =text.lower()

    if 'hello' in processed:
        return 'hi, how are you'

    if 'how are you' in processed:
        return 'I am fine'

    founders= ['harshvardhan','aadesh']
    if any(x in processed for x in founders):
        return 'hello my creater'

    else:
        return 'I did not understant that'


def handle_register(text: str) ->str:
    processed:str = text.lower()
    data=text.split(",")
    try:
        payload="{"+f'"telegramId":"{data[0]}","name":"{data[1]}","gender":"{data[2]}","genderOfInterest":"{data[3]}","age":{data[4]},"location":"{data[5]}"'+"}";
        json_object=json.loads(payload)
        print("payload is L",json_object)
        # response_from_server = requests.post(URL+"user",json = json_object)
        

        # Assuming req.body contains the data for creating a new user
        new_user = User(**json_object)
        get_insert = new_user.save()

        print(get_insert)
    except Exception as e:
        print("exception is:",e)
        if("E11000 duplicate key error collection" in str(e)):
            return 'user already registered with this telegramId'
    return 'registration successfull'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str= update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id} in {message_type}:"{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME,'').strip()
            response: str = handel_response(new_text)
        else:
            return
    else:
        if context.user_data['steps']== "started":
            response: str = handle_register(str(update.message.chat.id)+","+text)
            context.user_data['steps']= "finished"
        else:
            response: str = handel_response(text)

    print('response ',response)
    await update.message.reply_text(response)

async def handle_file_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str= update.message.chat.type
    print(f'uploading file...')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME,'').strip()
            response: str = handel_response(new_text)
        else:
            return
    else:
        if context.user_data['steps']== "fileUpload":
            file = update.message.photo[0].file_id
            obj = await context.bot.get_file(file)
            print(obj.file_path)
            extension = os.path.splitext(obj.file_path)
            await obj.download_to_drive(str(update.message.chat.id)+str(extension[1]))
            context.user_data['steps']=="Finished"

            with open(str(update.message.chat.id)+str(extension[1]), 'rb') as image_file:
                base64_data = image_file.read()
                # print("base64_data",base64_data)
                s3.file_upload_via_base64("profiles/pics/"+str(update.message.chat.id)+str(extension[1]),base64_data)
            await update.message.reply_text("Image received")

#error
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    print('started ...')
    #Commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custome',custome_command))
    app.add_handler(CommandHandler('register',register_command))
    app.add_handler(CommandHandler('file_upload',file_upload_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.ALL, handle_file_upload))

    #error
    app.add_error_handler(error)

    print('polling ...')
    app.run_polling(poll_interval = 3)
