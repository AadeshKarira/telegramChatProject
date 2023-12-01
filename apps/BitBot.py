from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import json
import socket

TOKEN: Final ='6763464118:AAH-DBNJ5iYI_GICfKRjZmOnA_K424Ogce8'
BOT_USERNAME: Final ='@Starter_Bit_Bot'
URL = 'http://13.232.2.16/'

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
        response_from_server = requests.post(URL+"user",json = json_object)
        print(response_from_server.headers)
    except Exception as e:
        print("exception is:",e)
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

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #error
    app.add_error_handler(error)

    print('polling ...')
    app.run_polling(poll_interval = 3)
