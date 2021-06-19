import telebot
import json, ssl
from telebot import types
import time
import mariadb
from pathlib import Path
from os import path, remove
from usuariosBO import UsuarioDB
from categoriasBO import CategoriasDB
from itemInfoBO import ItemInfoDB
from sesiones import SesionHandler
from customPool import CustomPool
import traceback
import locale


global config
global mensajes
global bot
global sesionHandler
global pool
global usuarioDB
import functools


#for lang in locale.locale_alias.values():
#    print(lang)

locale.setlocale(locale.LC_ALL,"es_ES.utf-8")


sesiones = {}
#Finding the absolute path of the config file
scriptPath =path.abspath('__file__')
dirPath = path.dirname(scriptPath)
configPath = path.join(dirPath,'config.json')
#Se leen los archivos de configuracion y de cadenas
config = json.load(open(configPath,encoding='utf-8'))
mensajes = json.load(open(path.join(dirPath,'mensajes.json'),encoding='utf-8'))


bot = telebot.TeleBot(config["botToken"],parse_mode="HTML")

#creación del pool de conexión
dbconfig = config['database']
sesionHandler = SesionHandler()
#pool = mariadb.ConnectionPool(**dbconfig)
pool =CustomPool(dbconfig)
usuarioDB = UsuarioDB(pool)
categoriaDB =  CategoriasDB(pool)
itemInfoDB = ItemInfoDB(pool)

def requiere_sesion(func):

    functools.wraps(func)
    def wrapper(*args,**kwargs):
        value = None
        sesion =  sesionHandler.getSesion(args[0].from_user.id)
        if sesion is None:
            if hasattr(args[0],"inline_message_id") and  args[0].inline_message_id is not None:
                bot.edit_message_text(inline_message_id=args[0].inline_message_id, text=mensajes["usuario_sin_sesion"])
            elif hasattr(args[0],"query") and args[0].query is not None:
                bot.answer_inline_query(args[0].id,[],cache_time=0,switch_pm_text="Se te ha ido la sesión. Pulsa aquí para empezar de nuevo.")
            else:
                bot.edit_message_text(message_id=args[0].message.id, chat_id=args[0].message.chat.id,text=mensajes["usuario_sin_sesion"])
        else :
            value  =func(*args,**kwargs)
        return value
    return wrapper

