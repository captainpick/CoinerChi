from telegram.ext import Updater, InlineQueryHandler, CommandHandler,CallbackQueryHandler,MessageHandler,ConversationHandler , Filters
import requests
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup ,ReplyKeyboardMarkup ,ReplyKeyboardRemove
import threading,time
from bs4 import BeautifulSoup
import json
import string
# Initial List
############################################################
bit_list=[]
last_list=[]
pair={}
bot = telegram.Bot(token='BOT-TOKEN')

bit_lists=['بیت کوین','اتریوم','لایت کوین','ترون','تدر']
bit_list_farsi={'بیت کوین':'BitcoinBTC','اتریوم':'EthereumETH','لایت کوین':'LitecoinLTC','باینانس کوین':'Binance CoinBNB','ترون':'TRONTRX','تدر':'TetherUSDT'}
############################################################
i =1


# Main Function 
############################################################
def main():
    updater = Updater('BOT-TOKEN',use_context=True,workers=4)
    dp = updater.dispatcher
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.text,MessageHandling))
    updater.dispatcher.add_handler(MessageHandler(Filters.document, Give_Picture),group=1)
    updater.dispatcher.add_handler(MessageHandler(Filters.contact, Get_Phone_Number),group=2)
    # dp.add_handler(CommandHandler('bop',bop))
    updater.start_polling()
    
    ticker = threading.Event()
    while not ticker.wait(600):
        Post(bot,dp)
    
    
   
    updater.idle()

############################################################
def Give_Picture(update,context):
    bot.sendDocument(chat_id='chat_id_number',document=update.message.document.file_id)
    bot.sendMessage(update.message.chat_id,text="از ارسال عکس خود ممنونیم . لطفا برای تایید صبر کنید",
                    reply_markup=telegram.ReplyKeyboardRemove())
    
# Get Coin Content From Site
############################################################
def get_content():
    URL = 'https://coinsara.com/marketcap/'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    list_all={}
    bitcoin_first=True
    eth_first=True
    bit_list_farsi={'بیت کوین':'BitcoinBTC','اتریوم':'EthereumETH','لایت کوین':'LitecoinLTC','باینانس کوین':'Binance CoinBNB','ترون':'TRONTRX','تدر':'TetherUSDT'}
    

    find_attr= soup.find_all("td")

    for it in find_attr:
        try:
            if("تومان" in it.attrs["title"]):
                for bit in bit_list_farsi:
                    if(bit in it.attrs["title"]):
                        if("بیت کوین" in it.attrs["title"] ):
                            if( bitcoin_first==True):
                                list_all[bit]=it.text
                                bitcoin_first=False
                        elif("اتریوم" in it.attrs["title"] ):
                            if( eth_first==True):
                                list_all[bit]=it.text
                                eth_first=False
                        else:
                            list_all[bit]=it.text

        except :
            pass
    
    return list_all
############################################################
def Give_Last_Price():
    message=''
   
    price=0
    all_data=get_content()
    
    for it in bit_lists:
        
        price= all_data[it].replace(",","")
        price= int(float(price.replace(" ","")))
        if (it=='تدر'):
              message+='-------------------------------------\n'

              message +='💰' + it  +' ( '+bit_list_farsi[it]+' ) ' + ' : '+ '\n'
              message+='فروش به ما : ' + str(int((price/100)*98.5))+' تومان ' + '\n'
              message+='خرید از ما : ' + str(int( (price/100)*101.5)) + ' تومان '+ ' \n\n'
        else :
              message +='💰' + it  +' ( '+bit_list_farsi[it]+' ) ' + ' : '+ '\n'
              message+='فروش به ما : ' + str(int((price/100)*99))+' تومان ' + '\n'
              message+='خرید از ما : ' + str(int( (price/100)*101)) + ' تومان '+ ' \n\n'
    message+='\n -------------------------------------\n'
    message+="خرید فروش از ما بدون کارمزد میباشد و مستقیم قیمت های ثبت شده محاسبه میشود . \n"
    message+='\n -------------------------------------\n'
    message+="برای خرید و فروش ارزهای دیجیتال و مشاوره سرمایه گذاری با ادمین ارتباط برقرار کنید . \n"
    message+="@SBZcoinadmin \n"
    message+='\n -------------------------------------\n'
    message+="کانال : @SBZ_coin"
    return message

# Post Function For Calculate Price and Send Message To Channel
############################################################
def Post(bot,update):
    
    message=Give_Last_Price()


    bot.sendMessage(chat_id="@CHannelID",text=message)
############################################################



# Start Function for /start Command
############################################################
def start(update, context):
    keyboard = [[InlineKeyboardButton("فعال سازی اولیه ربات ", callback_data='active')],
                 [InlineKeyboardButton("خرید و فروش ارز دیجیتال", callback_data='buysell')],
                [InlineKeyboardButton("کیف پول", callback_data='moneybag'),InlineKeyboardButton("دریافت آخرین قیمت ارز ها",callback_data="give_new_price")],
                [InlineKeyboardButton("راهنما", callback_data='help'),InlineKeyboardButton("پشتیبانی", callback_data='support')]]   # Define Keyboard For Initial Start
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('به کانال سبزوار بیتکوین خوش آمدید . برای ادامه از دکمه های زیر استفاده کنید .', reply_markup=reply_markup)

############################################################

# Back Function
############################################################
def back_to_start(update, context):
    keyboard = [[InlineKeyboardButton("فعال سازی اولیه ربات ", callback_data='active')],
                 [InlineKeyboardButton("خرید و فروش ارز دیجیتال", callback_data='buysell')],
                [InlineKeyboardButton("کیف پول", callback_data='moneybag'),InlineKeyboardButton("دریافت آخرین قیمت ارز ها",callback_data="give_new_price")],
                [InlineKeyboardButton("راهنما", callback_data='help'),InlineKeyboardButton("پشتیبانی", callback_data='support')]]   # Define Keyboard For Initial Start
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(' برای ادامه از دکمه های زیر استفاده کنید .', reply_markup=reply_markup)

############################################################

# Button Function for Click Handling and Button Response
############################################################
def button(update, context):
    query = update.callback_query
 
  
    if(query.data=="active"):
        # keyboard = [[InlineKeyboardButton("ارسال شماره ", callback_data='active')],[InlineKeyboardButton("برگشت ", callback_data='back')]]
        # reply_markup = InlineKeyboardMarkup(keyboard)
        reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('ارسال شماره', request_contact=True)]])

        query.message.reply_text("ارسال شماره را تایید کنید",reply_markup=reply_markup)
        keyboard = [[InlineKeyboardButton("برگشت ", callback_data='back')]]
        reply = InlineKeyboardMarkup(keyboard)

        query.message.reply_text(text="برای بازگشت کلیک کنید",reply_markup=reply)
        # query.answer("با فشردن کلیک شماره ی خود را برای تایید ارسال کنید ." )
  

        
    elif(query.data=="buysell"):    
        query.answer("خرید و فروش")
        # replys = ReplyKeyboardRemove()
        # query.edit_message_text(reply_markup=replys)
        keyboard = [[InlineKeyboardButton("خرید", callback_data='buy')],
                 [InlineKeyboardButton("فروش", callback_data='sell')]]
        reply = ReplyKeyboardMarkup(keyboard)

        query.message.reply_text("انتخاب کنید :",reply_markup=reply)

        
    elif(query.data=="give_new_price"):
        message = Give_Last_Price()
        keyboard = [[InlineKeyboardButton("برگشت ", callback_data='back')]]
        reply = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text=message,reply_markup=reply)


    elif(query.data=="is_authenticated"):
        user_id =str( query.message.chat.id)
        
        with open('read.json') as json_file:
            data = json.load(json_file)
        
        if(data[user_id][0]["is_authenticated"]=="yes"):
                
                query.answer(text="شما احراز هویت شده اید")
        else:
                query.answer(text="شما احراز هویت نشده اید . نسبت به ارسال مدارک خود اقدام نمایید")
           
        
        # query.message.reply_text("عکس خود را بفرستید")


    elif(query.data=="back"):
        keyboard = [[InlineKeyboardButton("فعال سازی اولیه ربات ", callback_data='active')],
                 [InlineKeyboardButton("خرید و فروش ارز دیجیتال", callback_data='buysell')],
                [InlineKeyboardButton("کیف پول", callback_data='moneybag'),InlineKeyboardButton("دریافت آخرین قیمت ارز ها",callback_data="give_new_price")],
                [InlineKeyboardButton("راهنما", callback_data='help'),InlineKeyboardButton("پشتیبانی", callback_data='support')]]   # Define Keyboard For Initial Start

    
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(text = 'به کانال سبزوار بیتکوین خوش آمدید . برای ادامه از دکمه های زیر استفاده کنید .', reply_markup=reply_markup)
    
    

############################################################
def Get_Phone_Number(update,context):
            # Message=update.effective_message.contact.phone_number
            reply_markup = telegram.ReplyKeyboardRemove()

            update.message.reply_text('از ارسال شماره ممنونیم' ,reply_markup=reply_markup)
        

# Give Phone Number For Signup Users
############################################################
def MessageHandling(update,context):
        
        #update.message.text
        Message  =  update.message.text
        
       
            
            
        
        if(Message=="خرید"):
                keyboard = [[InlineKeyboardButton("بررسی تایید شدن ", callback_data='is_authenticated')],
                [InlineKeyboardButton("فرستادن عکس ", callback_data='photo_send')],
                 [InlineKeyboardButton("برگشت", callback_data='back')]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                update.message.reply_text('برای بررسی کلیک کنید', reply_markup=reply_markup)

              
        elif(Message=="فروش"):
                    update.message.reply_text('با شماره ی 09333333333 تماس بگیرید .')
                    back_to_start(update,context)
            
        else:
                    if(update.message.text.isdecimal()):
                        print("dsdsd")
                    else:
                        update.message.reply_text('لطفا از دستورات مشخص استفاده کنید',message_id=update.message.message_id)
                    
                    
                        back_to_start(update,context)

                    
                    



        
            

       
       
        
############################################################


# Help Function
############################################################
def help_command(update, context):
    update.message.reply_text("Use /start to test this bot.")
############################################################

    
# if Condition for Run Program
############################################################
if __name__ == '__main__':
    main()
############################################################
