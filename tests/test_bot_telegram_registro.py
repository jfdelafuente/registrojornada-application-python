import unittest
from unittest.mock import patch
from BotTelegramRegistro import BotTelegramRegistro


class BotTelegramRegistroTestCase(unittest.TestCase):
    @patch("requests.get")
    def test_get_chat_id_success(self, mock_get):
        # Configurar el comportamiento simulado de requests.get
        mock_response = {
            "result": [
                {
                    "message": {
                        "chat": {"id": 123456789, "username": "usuario1"}
                    }
                },
                {
                    "message": {
                        "chat": {"id": 987654321, "username": "usuario2"}
                    }
                }
            ]
        }
        mock_get.return_value.json.return_value = mock_response

        # Inicializar el objeto BotTelegramRegistro con un token ficticio
        bot = BotTelegramRegistro("TOKEN_FICTICIO", 123456789)

        # Llamar a la función get_chat_id con el nombre de usuario
        chat_id = bot.get_chat_id("usuario1")

        # Verificar que el chat_id devuelto sea el esperado
        self.assertEqual(chat_id, 123456789)

    @patch("requests.get")
    def test_get_chat_id_user_not_found(self, mock_get):
        # Configurar el comportamiento simulado de requests.get
        mock_response = {"result": []}
        mock_get.return_value.json.return_value = mock_response

        # Inicializar el objeto BotTelegramRegistro con un token ficticio
        bot = BotTelegramRegistro("TOKEN_FICTICIO", 232333)

        # Llamar a la función get_chat_id con un nombre de usuario no existente
        chat_id = bot.get_chat_id("usuario_no_existente")

        # Verificar que se devuelva None cuando el usuario no se encuentra
        self.assertIsNone(chat_id)

    @patch("requests.post")
    def test_enviar_mensaje_success(self, mock_post):
        # Configurar el comportamiento simulado de requests.post
        mock_post.return_value.status_code = 200

        # Inicializar el objeto BotTelegramRegistro con un token ficticio
        bot = BotTelegramRegistro("TOKEN_FICTICIO", 123456789)

        # Llamar a la función enviar_mensaje con un chat_id y mensaje ficticios
        result = bot.send_to_telegram("Mensaje de prueba")

        # Verificar que el mensaje se envió correctamente
        self.assertTrue(result)

    @patch("requests.post")
    def test_enviar_mensaje_failure(self, mock_post):
        # Configurar el comportamiento simulado de requests.post
        mock_post.return_value.status_code = 400

        # Inicializar el objeto BotTelegramRegistro con un token ficticio
        bot = BotTelegramRegistro("TOKEN_FICTICIO", 123456789)

        # Llamar a la función enviar_mensaje con un chat_id y mensaje ficticios
        result = bot.send_to_telegram("Mensaje de prueba")

        # Verificar que se produjo un fallo al enviar el mensaje
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
