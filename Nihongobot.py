from telebot import types

import config
import botones
import repasar
import random


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
config.bot.polling(none_stop=True)

        
