
import requests,json
from bs4 import BeautifulSoup

f = open("cookies.json", "r")

cookieFile = json.loads(f.read())

cookies={}

for x in cookieFile:
    cookies[x["Name raw"]] = x["Content raw"]


r = requests.get('https://caixadirectaonline.cgd.pt/cdo/private/contasaordem/consultaSaldosMovimentos.seam', cookies=cookies, headers={"user-agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"})
#print(r.text)
parsed_html = BeautifulSoup(r.text, features="lxml")
saldo = parsed_html.body.find('div', attrs={'class':'saldos disponivel'})
#print(saldo)
print(saldo.find('p', attrs={'class':'valor'}).label.text, "€")
