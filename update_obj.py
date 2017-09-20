# encoding=utf8
from lxml import html
import BeautifulSoup
from bs4 import BeautifulSoup
import pickle
import urllib2
import time
import threading
import anywhereselenium


urlFi = 'http://www.quadrifoglio.org/scrivi_orario_strade_tutte.php?comune=FIRENZE'
urlSf = 'http://www.quadrifoglio.org/scrivi_orario_strade_tutte.php?comune=SESTO%20FIORENTINO'
start = time.time()
urls = [urlFi, urlSf]
listaFi = []
listaSf = []


def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def fetch_url(url):
    urlHandler = urllib2.urlopen(url)
    html = urlHandler.read().decode('UTF-8')
    print "'%s\' fetched in %ss\nParsing html..." % (url, (time.time() - start))
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all('div'):
		if url == urlFi:
		    listaFi.append(tag.text)
		    save_obj(listaFi, 'listaFi')
		else:
			listaSf.append(tag.text)
			save_obj(listaSf, 'listaSf')


threads = [threading.Thread(target=fetch_url, args=(url,)) for url in urls]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print "Elapsed Time: %s" % (time.time() - start)
print "Pickles saved in /obj."
anywhereselenium.automate()
