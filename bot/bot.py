# encoding=utf8
import sys
from flask import Flask, request
import telepot
import urllib3
import pickle
import unicodedata
import calendar
from datetime import datetime, timedelta
import bot_parser

reload(sys)
sys.setdefaultencoding('utf8')

replies = {
    'help': 'Questo bot da informazioni sul calendario della pulizia delle strade '
    'nei comuni di Firenze e Sesto Fiorentino. Per avere informazioni su una strada '
    'mandare semplicemente il nome della stessa a questo bot.',
}
proxy_url = "http://proxy.server:3128"
KEY = '297564683:AAHq3cetrsnUehJO1zFqMIAgVYNg9gVh5Lg'
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = "42"
bot = telepot.Bot(KEY)
bot.setWebhook("https://eyedema.pythonanywhere.com/{}".format(secret), max_connections=1)
bot.sendMessage(23616716, "✅  Bot started.")
app = Flask(__name__)



def load_obj(name):
    with open('/home/Eyedema/luckycloverbot/obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

listaStradeFi = load_obj('listaFi')
listaStradeSf = load_obj('listaSf')

def write_log(update):
    username = "---"
    try:
        username = update["message"]["from"]["username"]
    except Exception:
        pass
    text, chat_id, name = bot_parser.parse_update(update)
    with open('/home/Eyedema/luckycloverbot/obj/botlog.log', 'a+') as file:
        file.write(':: {:%Y-%b-%d %H:%M:%S} '.format(datetime.now())+name+' @'+username+' (ID:'+str(chat_id)+') searched for '+text+'\n')
    bot_parser.add_to_broadcast(update)

def send_schedule(update, dayN, nthDay):
    chat_id = bot_parser.parse_update(update)[1]
    schedule = bot_parser.get_schedule(dayN, nthDay)
    alert = bot_parser.hours_alert(schedule)
    bot.sendMessage(chat_id, "{} {}\nOrario 00.00 - 06.00".format(calendar.day_name[dayN], schedule))
    bot.sendMessage(chat_id, "/alert "+str(alert)+"h Spostare la macchina.")
    write_log(update)


def check_florence(chat_id, msg, strada):
    testoMessaggio = "Firenze:\n\n"
    for tag in listaStradeFi:
        if tag.split(' ', 1)[0] == strada:
            testoMessaggio += "🔴  "+tag+"\n"
    if testoMessaggio != "Firenze:\n\n":
        bot.sendMessage(chat_id, testoMessaggio)
        return 1
    return 0

def check_sesto(chat_id, msg, strada):
    testoMessaggio = "Sesto Fiorentino:\n\n"
    for tag in listaStradeSf:
        if tag.split(' ', 1)[0] == strada:
            testoMessaggio += "🔴  "+tag+"\n"
    if testoMessaggio != "Sesto Fiorentino:\n\n":
        bot.sendMessage(chat_id, testoMessaggio)
        return 1
    return 0

def parse_message(update):
    text, chat_id, name = bot_parser.parse_update(update)
    msg = 0
    try:
        text.decode('ascii')
    except (UnicodeEncodeError, UnicodeDecodeError), e:
        stradaX = bot_parser.build_string(text)
        strada = bot_parser.remove_accents(stradaX)
    else:
        strada = bot_parser.build_string(text)
    msg += check_florence(chat_id, msg, strada)
    msg += check_sesto(chat_id, msg, strada)
    if msg == 0:
        bot.sendMessage(chat_id, "Strada non trovata")
    write_log(update)

def welcome(update):
    bot.sendMessage(bot_parser.parse_update(update)[1],replies['help'])
    write_log(update)


def send_info(update):
    message = "Chat ID: "+str(bot_parser.parse_update(update)[1])+"\nChat type: "+update["message"]["chat"]["type"]
    bot.sendMessage(bot_parser.parse_update(update)[1], message)
    write_log(update)

def send_message(update):
    text = bot_parser.parse_update(update)[0]
    if len(text.split())>2:
        bot.sendMessage(text.split()[1], "".join(text.split()[2:]))

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        try:
            text = bot_parser.parse_update(update)[0]
            from_id = update["message"]["from"]["id"]
            if text == '/greco' or text == '/greco@LuckyCloverBot':
                send_schedule(update, 4,1)
            elif text == '/kyoto' or text == '/kyoto@LuckyCloverBot':
                send_schedule(update, 6,2)
            elif text == '/start':
                welcome(update)
            elif text == '/getinfo' and  from_id== 23616716:
                send_info(update)
            elif text.split()[0] == '@LuckyCloverBot':
                parse_message(update)
            elif text == '/getlist' and from_id == 23616716:
                bot.sendMessage(23616716, bot_parser.get_broadcast())
            elif text.split()[0] == '/send' and from_id == 23616716:
                send_message(update)
            elif update["message"]["chat"]["type"] == 'private':
                parse_message(update)
        except KeyError:
            pass
    return "OK"