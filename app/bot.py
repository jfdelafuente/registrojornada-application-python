import os
import telebot
import logging
import ViveOrange as viveOrange
from DiaValidator import validar_dia, dia_validate
from dotenv import load_dotenv
from datetime import date
from pathlib import Path

# Importar utilidades de seguridad
from utils.logger import setup_logger

load_dotenv()
token = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(token)

dic_user = {}

# Configurar logging seguro con sanitización
log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(exist_ok=True)
logger = setup_logger(
    name='registrojornada',
    log_file=str(log_dir / 'registrojornada.log'),
    level=logging.INFO,
    console=True
)

# Configurar logger para ViveOrange también
vive_logger = setup_logger(
    name='ViveOrange',
    log_file=str(log_dir / 'vive_orange.log'),
    level=logging.INFO
)



# /start
@bot.message_handler(commands=['start'])
def _start(message):
    dic_user["id"] = str(message.chat.id)
    logger.info(str(message.chat.username)+" - "+str(message.chat.id)+" --- START")

    ## send first msg
    msg = "Hola "+str(message.chat.username)+ ",\n\
        soy el Registro de Jornadas de Orange.\n\
        Para conocer los comandos, use \n/help"    
    bot.send_message(message.chat.id, msg)


# /help
@bot.message_handler(commands=['help'])
def _help(message):
    msg = "Utilice los siguients comandos:\n\
        /dia - Realizar un registro de jornada\n\
        /info - Ver Registro semanal\n\
        /infop - Ver Registro semana pasada "
    bot.send_message(message.chat.id, msg)


# /version
@bot.message_handler(commands=['version'])
def info_version(message):
    msg = "Version info tabulada. Utilice los siguients comandos:\n\
        Para conocer los comandos, use \n/help"
    bot.send_message(message.chat.id, msg)


# /info
@bot.message_handler(commands=['info'])
def info_handler(message):
    logger.info(str(message.text)+" --- INFO REGISTRO SEMANA")
    dia = date.today()
    vive_orange = viveOrange.ViveOrange(False, False)
    mensaje = vive_orange.connectar(dia)
    # mensaje = vive_orange.dummy(dia, "info")
    bot.send_message(message.chat.id, "Here's your info!")
    bot.send_message(message.chat.id, mensaje, parse_mode="Markdown")


# /infop
@bot.message_handler(commands=['infop'])
def info_handler(message):
    logger.info(str(message.text)+" --- INFO REGISTRO SEMANA ANTERIOR")
    dia = date.today()
    vive_orange = viveOrange.ViveOrange(False, True)
    mensaje = vive_orange.connectar(dia)
    # mensaje = vive_orange.dummy(dia, "infop")
    bot.send_message(message.chat.id, "Here's your info!")
    bot.send_message(message.chat.id, mensaje, parse_mode="Markdown")


# /dia
@bot.message_handler(commands=['dia'])
def dia_handler(message):
    logger.info(str(message.chat.username)+" - "+str(message.chat.id)+" --- DIA")
    text = "¿Que día quieres registrar ?\nElige uno: *HOY*,  *AYER*  o un día en formato [YYYYMMDD]."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

def day_handler(message):
    day = message.text
    logger.info(str(message.text)+" --- DAY HANDLER")
    dia_registro = validar_dia(day.upper())
    mensaje, registrar = dia_validate(dia_registro)
    logger.info("Mensaje: %s  -  Registro: %s" % (mensaje, registrar))
    if registrar == True:
        vive_orange = viveOrange.ViveOrange(True, False)
        msg = vive_orange.connectar(dia_registro)
        # msg = vive_orange.dummy(dia_registro, mensaje)
        bot.send_message(message.chat.id, "###  Realizamos Operacion  ####")
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    else:
        text = f'*Hoy es: {dia_registro}.\n¿{mensaje}?*\n¿Quieres registrar el día ??\nTeclea: *Y* o *N*.'
        sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, day_handler_teletrabajo, dia_registro)

def day_handler_teletrabajo(message, day):
    logger.info(str(message.text)+" --- DAY HANDLER TELETRABAJO")
    if message.text == "Y":
        msg_cabecera = "###  Realizamos Operacion  ####"
        vive_orange = viveOrange.ViveOrange(True, False)
        msg = vive_orange.connectar(day)
        # msg = vive_orange.dummy(day, "Dia Forzado")
    else:
        msg_cabecera= "###  Cancelamos operacion  ####"
        msg = "Utilice los siguients comandos:\n\
            /dia - Realizar un registro de jornada\n\
            /info - Ver Registro semanal\n\
            /infop - Ver Registro semana pasada\n"
        
    bot.send_message(message.chat.id, msg_cabecera)
    bot.send_message(message.chat.id, msg, parse_mode="Markdown")

# non-command message
@bot.message_handler(func=lambda m: True)
def chat(message):
    txt = message.text
    if any(x in txt.lower() for x in ["thank","thx","cool"]):
        msg = "anytime"
    elif any(x in txt.lower() for x in ["hi","hello","yo","hey"]):
        msg = "yo" if str(message.chat.username) == "none" else "yo "+str(message.chat.username)
    else:
        msg = "obten ayuda  \n/help"
    bot.send_message(message.chat.id, msg)


def main():
    bot.polling()

if __name__ == '__main__':
    main()