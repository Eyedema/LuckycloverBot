# encoding=utf8
import sys
from flask import Flask, request
import telepot
import urllib3
from datetime import datetime, timedelta
import calendar
import pickle
import unicodedata
reload(sys)
sys.setdefaultencoding('utf8')

replies = {
    'help': 'Questo bot da informazioni sul calendario della pulizia delle strade '
    'nei comuni di Firenze e Sesto Fiorentino. Per avere informazioni su una strada '
    'mandare semplicemente il nome della stessa a questo bot.',
}
my_id = 999999
proxy_url = "http://proxy.server:3128"
KEY = '297564683:XXXXXXXXXXXXXXXXX'
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = "XXXXXXXXXXXXXXXXXXXXX"
bot = telepot.Bot(KEY)
bot.setWebhook("https://eyedema.pythonanywhere.com/{}".format(secret), max_connections=1)
bot.sendMessage(my_id, "✅  Bot started.")
app = Flask(__name__)

def load_obj(name):
    with open('/home/Eyedema/obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

listaStradeFi = load_obj('listaFi')
listaStradeSf = load_obj('listaSf')

def write_log(text, name, userID):
    with open('/home/Eyedema/obj/botlog.log', 'a+') as file:
        file.write(':: {:%Y-%b-%d %H:%M:%S} '.format(datetime.now())+name+' (ID:'+str(userID)+') searched for '+text+'\n')

def build_string(suffix):
    suffix = suffix.upper()
    appendix = suffix.rsplit(None, 1)[-1]
    return appendix.split("'")[-1]

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])+"'"

def hours_alert(date):
    d1 = datetime.strptime(date, '%Y-%m-%d')
    d2 = d1 - timedelta(days=1)
    hours = (datetime.now().hour) - 7
    return abs((d2 - datetime.today()).days*24 - hours)

def get_schedule(dayN, nthDay):
    this_month_schedule = calendar.Calendar(dayN).monthdatescalendar(datetime.today().year, datetime.today().month)[nthDay][0]
    next_month_schedule = calendar.Calendar(dayN).monthdatescalendar(datetime.today().year, datetime.today().month+1)[nthDay][0]
    return str(this_month_schedule) if this_month_schedule > datetime.today().date() else str(next_month_schedule)

def send_message(chat_id, dayN, nthDay):
    schedule = get_schedule(dayN, nthDay)
    alert = hours_alert(schedule)
    bot.sendMessage(chat_id, "{} {}\nOrario 00.00 - 06.00".format(calendar.day_name[dayN], schedule))
    bot.sendMessage(chat_id, "/alert "+str(alert)+"h Spostare la macchina.")

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

def parse_message(chat_id, update):
    text = update["message"]["text"]
    msg = 0
    try:
        text.decode('ascii')
    except (UnicodeEncodeError, UnicodeDecodeError), e:
        stradaX = build_string(text)
        strada = remove_accents(stradaX)
    else:
        strada = build_string(text)
    msg += check_florence(chat_id, msg, strada)
    msg += check_sesto(chat_id, msg, strada)
    if msg == 0:
        bot.sendMessage(chat_id, "Strada non trovata")
    write_log(update["message"]["text"], update["message"]["from"]["first_name"], chat_id)

def welcome(chat_id):
    bot.sendMessage(chat_id,replies['help'])

def send_info(update):
    message = "Chat ID: "+str(update["message"]["chat"]["id"])+"\nChat type: "+update["message"]["chat"]["type"]
    bot.sendMessage(update["message"]["chat"]["id"], message)
    write_log(update["message"]["text"], update["message"]["from"]["first_name"],update["message"]["chat"]["id"])

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        try:
            text = update["message"]["text"]
            chat_id = update["message"]["chat"]["id"]
            if text == '/greco' or text == '/greco@LuckyCloverBot':
                send_message(chat_id, 4,1)
            elif text == '/kyoto' or text == '/kyoto@LuckyCloverBot':
                send_message(chat_id, 6,2)
            elif text == '/start':
                welcome(chat_id)
            elif text == '/getinfo' and update["message"]["from"]["id"] == my_id:
                send_info(update)
            elif text.split()[0] == '@LuckyCloverBot':
                parse_message(chat_id, update)
            elif update["message"]["chat"]["type"] == 'private':
                parse_message(chat_id, update)
        except KeyError:
            pass
    return "OK"