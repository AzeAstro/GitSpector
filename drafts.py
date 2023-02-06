from requests import get
from bs4 import BeautifulSoup


html=get("https://github.com/DevilXD/TwitchDropsMiner/commits/master").text

soup=BeautifulSoup(html,"html.parser")


tagAs=soup.find_all("span")

for tag in tagAs:
    if tag.text=="Older":
        print(tag.get('href'))