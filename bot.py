from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, CommandHandler, ContextTypes, CallbackQueryHandler, filters, ApplicationBuilder
from telegram.constants import ParseMode
import speech_recognition as sr
from translate import Translator
import time
import pyttsx3
from pydub import AudioSegment
import io, os


async def  start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global setting_keyboard, language_keyboard
    language_keyboard = [ 
                 
                 [InlineKeyboardButton('🇬🇧 English', callback_data='en'),                      InlineKeyboardButton('🇷🇺 Russia', callback_data='ru'),                      InlineKeyboardButton('🇨🇳 Chinese', callback_data='zh'),
                 ],
                 [InlineKeyboardButton('🇯🇵 Japanese', callback_data='ja'),                  InlineKeyboardButton('🇰🇷 Korean', callback_data='ko'),                  InlineKeyboardButton('🇮🇳 Hindi', callback_data='hi'),
                 ],
                 [InlineKeyboardButton('🇺🇿 Uzbek', callback_data='uz'),                  InlineKeyboardButton('🇰🇿 Kazakh', callback_data='kk'),                  InlineKeyboardButton('🇸🇦 Arabic', callback_data='ar-001'),
                 ],
                 [InlineKeyboardButton('🇪🇸 Spanish', callback_data='es'),                  InlineKeyboardButton('🇫🇷 French', callback_data='fr'),                  InlineKeyboardButton('🇹🇷 Turkish', callback_data='tr'),
                 ] ]
    
    setting_keyboard = [
        [InlineKeyboardButton("⚙️Settings", callback_data='settings')]
    ]
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="<b><i>Hello, Welcome to Voice-translator.\nPlease, click this button to set the settings </i></b>!", reply_markup=InlineKeyboardMarkup(setting_keyboard), parse_mode=ParseMode.HTML)

async def  buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
      global query 
      query = update.callback_query
      query.answer()

      if query.data == "settings":
          context.user_data['step']="settings"
          await query.edit_message_text( text=f"<b><i>You have seleced<b> {query.data} </b>option, Please message me which person you would like to speak with in the message chat as like forward.</i></b>", parse_mode=ParseMode.HTML)

      elif query.data == "en":
          
          context.user_data['step']="en"
          my_language = "en"
          await query.edit_message_text( text=f"<b><i>You have seleced<b> {query.data} lang </b>option, please write anything for selecting your friend language...</i></b>", parse_mode=ParseMode.HTML)

      elif query.data == "ru":
          my_language = "ru"
          context.user_data['step']="ru"
          await query.edit_message_text( text=f"<b><i>You have seleced<b> {query.data} lang </b>option, Selecd your friend language !</i></b>", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(language_keyboard))        
    
      elif query.data == "back":
          context.user_data['step']="back"
          setting_keyboard = [
                 [InlineKeyboardButton("⚙️Settings", callback_data='settings')]
           ]   
          await query.edit_message_text( text=f"You have returned to the Settings section😊", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(setting_keyboard))

async def  settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if context.user_data['step']=="settings":
        global my_chat_id, friend_chat_id

        my_chat_id = update.effective_chat.id
        print(my_chat_id)
       
        friend_chat_id = update.message.forward_from.id
        print(friend_chat_id)

        if update.message.forward_from.id==friend_chat_id:
            text2 = "<b><i>Message has been recieved.\nSelect your language, and wait for result!</i></b>"
                
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text2, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(language_keyboard)) 
             
    elif context.user_data['step']=='en':
                
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Select your friend language !", reply_markup=InlineKeyboardMarkup(language_keyboard))

        time.sleep(5)

        await context.bot.send_message(chat_id=update.effective_chat.id, text="<b>Congratulations, you have successfully completed the settings. You can start voice chat via <b><i> Voice-translator</i></b>, now send message to your friend.</b>", parse_mode=ParseMode.HTML) 


async def chatvoicetran(update: Update, context: ContextTypes.DEFAULT_TYPE):


             print(update.message.from_user.id)
             if update.effective_chat.id == my_chat_id:

                file_id =  await update.message.voice.get_file()
                file_object = await file_id.download_as_bytearray()

                with io.BytesIO(file_object) as data:

                    wav_file = AudioSegment.from_file(data)
                    wav_file = wav_file.set_channels(1)
                    wav_file = wav_file.set_sample_width(2)

                wav_file.export("audio3/voice.wav", format='wav')

                r = sr.Recognizer()
                audiofile = sr.AudioFile("audio3/voice.wav")
                with audiofile as source:
                    audio = r.record(source)
                text = r.recognize_google(audio, language="en")
                print(text)
 
                translator = Translator(from_lang="en", to_lang="ru")
                translator_text = translator.translate(text=text)
                print(translator_text)
                
                engine = pyttsx3.init()
                voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
                engine.setProperty('voice', voice_id)
                engine.setProperty('rate', 150)
                engine.setProperty('volume', 1)

                engine.save_to_file(translator_text, 'audio3/myvoice.wav')
                engine.runAndWait()

                keyboard = [
                     [InlineKeyboardButton("🔄Main", callback_data='back')]
                ]

                await context.bot.send_voice(chat_id=friend_chat_id, voice='audio3/myvoice.wav', reply_markup=InlineKeyboardMarkup(keyboard))  

                os.remove('audio3/voice.wav')
                os.remove('audio3/myvoice.wav')  

             elif update.effective_chat.id == friend_chat_id:

                file_id =  await update.message.voice.get_file()
                file_object = await file_id.download_as_bytearray()

                with io.BytesIO(file_object) as data:

                    wav_file = AudioSegment.from_file(data)
                    wav_file = wav_file.set_channels(1)
                    wav_file = wav_file.set_sample_width(2)

                wav_file.export("audio3/voice1.wav", format='wav')

                r = sr.Recognizer()
                audiofile = sr.AudioFile("audio3/voice1.wav")
                with audiofile as source:
                    audio = r.record(source)
                text = r.recognize_google(audio, language="ru")
                print(text)
                
                translator = Translator(from_lang="ru", to_lang="en")
                translator_text = translator.translate(text=text)
                
                engine = pyttsx3.init()
                voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
                engine.setProperty('voice', voice_id)
                engine.setProperty('rate', 150)
                engine.setProperty('volume', 1)

                engine.save_to_file(translator_text, 'audio3/yourvoice.wav')
                engine.runAndWait()
                keyboard_data = [
                     [InlineKeyboardButton("🔄Main", callback_data='back')]
                ]

                await context.bot.send_voice(chat_id=my_chat_id, voice='audio3/yourvoice.wav', reply_markup=InlineKeyboardMarkup(keyboard_data)) 

                os.remove('audio3/voice1.wav')
                os.remove('audio3/yourvoice.wav')        
         

application = ApplicationBuilder().token("6139727846:AAF0bp4l7hf8xLks_A6CxaO_Gl-hEMczgy8").build()

start_handler = CommandHandler('start', start)
application.add_handler(start_handler)    

message_handler = MessageHandler(filters.TEXT, settings)
application.add_handler(message_handler)

application.add_handler(CallbackQueryHandler(buttons))

voice_chat_handler = MessageHandler(filters.VOICE, chatvoicetran)
application.add_handler(voice_chat_handler)

print("Bot ishga tushdi...")
application.run_polling()