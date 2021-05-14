# mastrobot_example.py
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from manager import chooseResponse,returnResponsesPercentage, insertResponse, insertWord
token='1814580873:AAFnmd10CAJ0XTU-A57Rk7dF461MYYw476M'
newResponseBool=False
prevWord=''
# function to handle the /start command
def start(update, context):
    update.message.reply_text('start command received')

# function to handle the /help command
def help(update, context):
    update.message.reply_text('help command received')

# function to handle errors occured in the dispatcher 
def error(update, context):
    global prevWord
    update.message.reply_text(f'I do not know how to respond to this message yet, please submit a response for: "{update.message.text}""')
    prevWord=update.message.text
    newResponseBool=True

# function to handle normal text 
def text(update, context):
    print(prevWord)
    if newResponseBool==False:
      text_received = update.message.text
      print(text_received)
      reply=chooseResponse(text_received)
      print(returnResponsesPercentage(text_received))
      update.message.reply_text(reply[0])
    else:
      text_received = update.message.text
      print(text_received)
      insertWord(prevWord.lower())
      insertResponse(prevWord.lower(),text_received)



def main():
    print("#####    STARTED BOT    #####")
    TOKEN = token

    # create the updater, that will automatically create also a dispatcher and a queue to 
    # make them dialoge
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    # add an handler for normal text (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text, text))

    # add an handler for errors
    dispatcher.add_error_handler(error)

    # start your shiny new bot
    updater.start_polling()

    # run the bot until Ctrl-C
    updater.idle()