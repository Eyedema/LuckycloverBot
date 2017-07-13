# encoding=utf8
from lxml import html
import BeautifulSoup
from bs4 import BeautifulSoup
import pickle
import urllib2
import time


urlFi = 'http://www.quadrifoglio.org/scrivi_orario_strade_tutte.php?comune=FIRENZE'
urlSf = 'http://www.quadrifoglio.org/scrivi_orario_strade_tutte.php?comune=SESTO%20FIORENTINO'
listaFi = []
listaSf = []


def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


print "Florence schedule download started."
start_time = time.time()
htmlFi = urllib2.urlopen(urlFi).read().decode('UTF-8')
print "Florence schedule download complete."
time.sleep(0.5)
print "Sesto Fiorentino schedule download started."
htmlSf = urllib2.urlopen(urlSf).read().decode('UTF-8')
print "Sesto Fiorentino schedule download complete."
print "Download completed in {} seconds.\nSaving pickles...".format(time.time() - start_time)

soupFi = BeautifulSoup(htmlFi, "lxml")
soupSf = BeautifulSoup(htmlSf, "lxml")

for tag in soupFi.find_all('div'):
    listaFi.append(tag.text)

for tag in soupSf.find_all('div'):
    listaSf.append(tag.text)

save_obj(listaFi, 'listaFi')
save_obj(listaSf, 'listaSf')
time.sleep(0.5)
print "Pickles saved in /obj."
