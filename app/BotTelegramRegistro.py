import requests

class BotTelegramRegistro:
    
    def __init__(self, token, chat_id):
        self.token = token
        if (chat_id is None):
            # print("Buscamos el chat_id")
            self.chat_id = self._get_chat_id()
        else:
            # print("Chat id : %s" % chat_id)
            self.chat_id=chat_id
            
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def get_chat_id(self, username):
        url = f"{self.base_url}/getUpdates"
        response = requests.get(url)
        data = response.json()
        for update in data["result"]:
            if "message" in update and "chat" in update["message"] and "username" in update["message"]["chat"]:
                if update["message"]["chat"]["username"] == username:
                    return update["message"]["chat"]["id"]
        return None

    def send_to_telegram(self, mensaje):
        url = f"{self.base_url}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": mensaje}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return True
        return False
    
    def send_to_telegram_dummy(self, mensaje):
        return True
