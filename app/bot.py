"""Telegram bot for Orange workday registration."""

import logging
import telebot
from datetime import date
from dotenv import load_dotenv

# Import configuration and utilities
from config import get_settings
from utils.logger import setup_logger
from DiaValidator import validar_dia, dia_validate
import ViveOrange as viveOrange

# Import ServiceContainer and exceptions
from core import get_container
from exceptions import RegistroJornadaException

# Load environment variables
load_dotenv()

# Get settings using Pydantic Settings
settings = get_settings()

# Get service container (dependency injection)
container = get_container()

# Initialize bot using container
bot = telebot.TeleBot(container.secrets_manager.get_secret('BOT_TOKEN_ENCRYPTED'))

dic_user = {}

# Setup logging with settings
logger = setup_logger(
    name='registrojornada',
    log_file=str(settings.logs_dir / 'registrojornada.log'),
    level=logging.INFO,
    console=True
)

# Setup logger for ViveOrange
vive_logger = setup_logger(
    name='ViveOrange',
    log_file=str(settings.logs_dir / 'vive_orange.log'),
    level=logging.INFO
)



# /start
@bot.message_handler(commands=['start'])
def _start(message):
    dic_user["id"] = str(message.chat.id)
    logger.info(f"{message.chat.username} - {message.chat.id} --- START")

    try:
        # Use NotificationService for greeting
        container.notification_service.send_greeting(
            username=message.chat.username,
            chat_id=message.chat.id
        )
    except Exception as e:
        logger.error(f"Error sending greeting: {e}")
        # Fallback to direct bot message
        bot.send_message(
            message.chat.id,
            f"Hola {message.chat.username},\nsoy el Registro de Jornadas de Orange."
        )


# /help
@bot.message_handler(commands=['help'])
def _help(message):
    try:
        # Use NotificationService for help message
        container.notification_service.send_help_message(chat_id=message.chat.id)
    except Exception as e:
        logger.error(f"Error sending help: {e}")
        # Fallback
        msg = "Utilice los siguientes comandos:\n/dia - Realizar un registro de jornada\n/info - Ver Registro semanal\n/infop - Ver Registro semana pasada"
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
    logger.info(f"{message.text} --- INFO REGISTRO SEMANA")

    try:
        dia = date.today()
        vive_orange = viveOrange.ViveOrange(False, False)
        mensaje = vive_orange.connectar(dia)

        container.notification_service.send_info("Generando informe semanal...", chat_id=message.chat.id)
        container.notification_service.send_message(mensaje, chat_id=message.chat.id)

    except RegistroJornadaException as e:
        # Handle application errors
        error_msg = container.error_handler.handle_exception(e, {
            'user': message.chat.username,
            'command': '/info'
        })
        container.notification_service.send_message(error_msg, chat_id=message.chat.id)

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error in /info: {e}", exc_info=True)
        container.notification_service.send_message(
            "❌ Error inesperado al generar informe. Revisa los logs.",
            chat_id=message.chat.id
        )


# /infop
@bot.message_handler(commands=['infop'])
def infop_handler(message):
    logger.info(f"{message.text} --- INFO REGISTRO SEMANA ANTERIOR")

    try:
        dia = date.today()
        vive_orange = viveOrange.ViveOrange(False, True)
        mensaje = vive_orange.connectar(dia)

        container.notification_service.send_info("Generando informe semana anterior...", chat_id=message.chat.id)
        container.notification_service.send_message(mensaje, chat_id=message.chat.id)

    except RegistroJornadaException as e:
        # Handle application errors
        error_msg = container.error_handler.handle_exception(e, {
            'user': message.chat.username,
            'command': '/infop'
        })
        container.notification_service.send_message(error_msg, chat_id=message.chat.id)

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error in /infop: {e}", exc_info=True)
        container.notification_service.send_message(
            "❌ Error inesperado al generar informe. Revisa los logs.",
            chat_id=message.chat.id
        )


# /dia
@bot.message_handler(commands=['dia'])
def dia_handler(message):
    logger.info(f"{message.chat.username} - {message.chat.id} --- DIA")
    text = "¿Qué día quieres registrar?\nElige uno: *HOY*, *AYER* o un día en formato [YYYYMMDD]."
    sent_msg = container.notification_service.send_message(text, chat_id=message.chat.id)
    bot.register_next_step_handler_by_chat_id(message.chat.id, day_handler)

def day_handler(message):
    day = message.text
    logger.info(f"{message.text} --- DAY HANDLER")

    try:
        dia_registro = validar_dia(day.upper())
        mensaje, registrar = dia_validate(dia_registro)
        logger.info(f"Mensaje: {mensaje} - Registro: {registrar}")

        if registrar:
            # Register the workday
            vive_orange = viveOrange.ViveOrange(True, False)
            msg = vive_orange.connectar(dia_registro)
            container.notification_service.send_success("Operación Realizada", chat_id=message.chat.id)
            container.notification_service.send_message(msg, chat_id=message.chat.id)
        else:
            # Ask for confirmation
            text = f'*Fecha: {dia_registro.strftime("%d/%m/%Y")}*\n{mensaje}\n\n¿Quieres registrar el día de todas formas?\nTeclea: *Y* o *N*.'
            container.notification_service.send_message(text, chat_id=message.chat.id)
            bot.register_next_step_handler_by_chat_id(message.chat.id, day_handler_teletrabajo, dia_registro)

    except RegistroJornadaException as e:
        error_msg = container.error_handler.handle_exception(e, {
            'user': message.chat.username,
            'command': '/dia',
            'day': day
        })
        container.notification_service.send_message(error_msg, chat_id=message.chat.id)

    except Exception as e:
        logger.error(f"Unexpected error in day_handler: {e}", exc_info=True)
        container.notification_service.send_message(
            "❌ Error inesperado al procesar la fecha. Revisa el formato.",
            chat_id=message.chat.id
        )

def day_handler_teletrabajo(message, day):
    logger.info(f"{message.text} --- DAY HANDLER TELETRABAJO")

    try:
        if message.text.upper() == "Y":
            # Force registration
            vive_orange = viveOrange.ViveOrange(True, False)
            msg = vive_orange.connectar(day)
            container.notification_service.send_success("Operación Realizada (Forzada)", chat_id=message.chat.id)
            container.notification_service.send_message(msg, chat_id=message.chat.id)
        else:
            # Cancel operation
            container.notification_service.send_warning("Operación Cancelada", chat_id=message.chat.id)
            container.notification_service.send_help_message(chat_id=message.chat.id)

    except RegistroJornadaException as e:
        error_msg = container.error_handler.handle_exception(e, {
            'user': message.chat.username,
            'command': '/dia (forced)',
            'day': day
        })
        container.notification_service.send_message(error_msg, chat_id=message.chat.id)

    except Exception as e:
        logger.error(f"Unexpected error in day_handler_teletrabajo: {e}", exc_info=True)
        container.notification_service.send_message(
            "❌ Error inesperado al registrar jornada.",
            chat_id=message.chat.id
        )

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