from telebot import types

import config
import botones
from partida import Partida



@config.bot.callback_query_handler(lambda call: call.data.startswith("responder_"))
def responder(call):
    idRespuesta = int(call.data.split("_")[1])

    sesion  = config.sesionHandler.getSesion(call.from_user.id)
    numPregunta = sesion.numPregunta
    texto=config.mensajes["error"]
    pregunta = sesion.partida.preguntas[sesion.numPregunta]
    if pregunta.opcionCorrecta.id == idRespuesta:
        sesion.partida.aciertos+=1
        texto=config.mensajes["acierto"]
    markup  = types.InlineKeyboardMarkup()
    markup.row_width=1
    opciones=[]
    for itemInfo in pregunta.opciones:
        textoOpcion = itemInfo.getValorCaracteristica(pregunta.caracteristicaRespuesta.id)
        if itemInfo.id == pregunta.opcionCorrecta.id:
            textoOpcion="✅ " + textoOpcion
        elif itemInfo.id == idRespuesta:
            textoOpcion ="❌ " + textoOpcion
        opciones.append(types.InlineKeyboardButton(text=textoOpcion ,callback_data="novalepana"))
    opciones.append(types.InlineKeyboardButton(text=config.mensajes["siguiente_pregunta"] ,callback_data="preguntar"))
    markup.add(*opciones)
    texto+=pregunta.getTextoPregunta()

    config.bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=texto,reply_markup=markup)            



@config.bot.callback_query_handler(lambda call: call.data.startswith("preguntar"))
def siguientePregunta(call):
    sesion  = config.sesionHandler.getSesion(call.from_user.id)
    sesion.numPregunta+=1
    preguntar(call.message.chat.id,call.message.id,call.from_user.id)



@config.bot.callback_query_handler(lambda call: call.data.startswith("repasar_"))
def repasar(call):
    idCategoria = int(call.data.split("_")[1])
    sesion  = config.sesionHandler.getSesion(call.from_user.id)

    itemsInfo = config.itemInfoDB.getItemsInfoByCategoria(idCategoria)
    sesion.partida = Partida(itemsInfo)
    sesion.numPregunta=0

    preguntar(call.message.chat.id,call.message.id,call.from_user.id)
    
def preguntar(chatId,messageId,userId):
    sesion  = config.sesionHandler.getSesion(userId)
    partida = sesion.partida

    if len(partida.preguntas) > sesion.numPregunta:
        pregunta = partida.preguntas[sesion.numPregunta]
        markup  = types.InlineKeyboardMarkup()
        markup.row_width=1
        opciones=[]

        for itemInfo in pregunta.opciones:
                opciones.append(types.InlineKeyboardButton(text=itemInfo.getValorCaracteristica(pregunta.caracteristicaRespuesta.id) ,callback_data="responder_"+str(itemInfo.id)))


        opciones.append(botones.getBoton("cancelar"))
        markup.add(*opciones)
        texto=pregunta.getTextoPregunta()

        config.bot.edit_message_text(chat_id=chatId,message_id=messageId,text=texto,reply_markup=markup)            
    else:
        finRepaso(chatId,messageId,userId)
            
def finRepaso(chatId,messageId,userId):
    sesion  = config.sesionHandler.getSesion(userId)
    config.bot.edit_message_text(chat_id=chatId,message_id=messageId,text=config.mensajes["fin_repaso"].format(aciertos=sesion.partida.aciertos,preguntas=len(sesion.partida.preguntas)))
    
        
    


    
    
