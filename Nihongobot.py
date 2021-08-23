from telebot import types
from flask import Flask, request
import config
import botones
import repasar
import random
import sys
import telebot

app = Flask(__name__)

@app.route('/')
def home():
    return 'TelegramBots listening'

@app.route('/Nihongobot', methods=['POST'])
def getMessage():
    print("request recieved", file=sys.stderr)
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    config.bot.process_new_updates([update])
    return "!", 200


@config.bot.callback_query_handler(lambda call: call.data =="cancelar")
def cancelar(call):
    config.bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=config.mensajes["adios"]);
    

    
@config.bot.message_handler(commands=['start'])
def inicio(message):


    usuario = config.usuarioDB.getUsuario(message.from_user.id);

    if not usuario :
        markup  = types.InlineKeyboardMarkup()
        texto="""Lo siento, no estás  autorizado."""
        config.bot.send_message(message.chat.id, text=texto, reply_markup=markup)
    else:
        sesion = config.sesionHandler.crearSesion(usuario)
        markup  = types.InlineKeyboardMarkup()
        markup.row_width=1
        opciones = []
        categorias = config.categoriaDB.getCategorias()

        for categoria in categorias:
            opciones.append(types.InlineKeyboardButton(text="Repasar "+categoria.nombre,callback_data="repasar_"+str(categoria.id)))

        opciones.append(botones.getBoton("cancelar"))
        markup.add(*opciones)
        config.bot.send_message(message.chat.id, text=config.mensajes["saludo"].format(nombreUsuario=usuario.nombre), reply_markup=markup)

print('bot arrancado')


random.seed()
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8080)
    


        
