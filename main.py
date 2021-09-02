import requests,json
#from pprint import pprint
from bs4 import BeautifulSoup
import sys

if len(sys.argv) == 3:
    username = sys.argv[1]
    password = sys.argv[2]
elif len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "--help"):
    exit()
else:
    username = input("Username:")
    password = input("Password:")


session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en,en-US;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-User": "?1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}
#session.get("https://www.cgd.pt/")

loginPagePOST = {
	"USERNAME": username,
	"login_btn_1": "OK",
	"tipoTrat": "",
	"codFamiliaProduto": "",
	"numIntEspecie": "",
	"RedirFunc": ""
}

reply = session.get("https://caixadirectaonline.cgd.pt/cdo/login.seam", data=loginPagePOST)

loginPOST = {
	"target": "/cdo/private/home.seam",
	"username": "CDO" + username,
	"userInput": username,
	"passwordInput": "******",
	"password": password
}
#session.headers["referrer"] = "https://caixadirectaonline.cgd.pt/cdo/login.seam" #if needed just uncomment, doubt tho

reply = session.post("https://caixadirectaonline.cgd.pt/cdo/auth/forms/login.fcc", data=loginPOST)

try:
    session.cookies["SMSESSION"]
except KeyError:
    print("Authentication failure!")
    exit()

#pprint(vars(reply))
#pprint(dict(session.cookies))
#print(reply.status_code)


page = session.get('https://caixadirectaonline.cgd.pt/cdo/private/contasaordem/consultaSaldosMovimentos.seam')
#pprint(dict(session.cookies))
#print(page.text)

parsed_html = BeautifulSoup(page.text, features="lxml")
saldo = parsed_html.body.find('div', attrs={'class':'saldos disponivel'})
print(saldo.find('p', attrs={'class':'valor'}).label.text, "€")
