import requests
from telegram import Bot

def get_chat_id(bot_token):
    url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['result']:
            chat_id = data['result'][0]['message']['chat']['id']
            return chat_id
        else:
            print("No updates found. Make sure you've started a conversation with your bot.")
    else:
        print(f"Failed to fetch updates. Status code: {response.status_code}")


async def send_message(bot_token, chat_id, text):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=text)

chat_id = get_chat_id('7153111852:AAG1Weo9gaf0yy2CakXbJ2D8muckAPm2NaI')

async def main(text):
    await send_message('7153111852:AAG1Weo9gaf0yy2CakXbJ2D8muckAPm2NaI', chat_id, text)



