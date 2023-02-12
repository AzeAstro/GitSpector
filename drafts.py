from requests import get
from bs4 import BeautifulSoup


# html=get("https://github.com/AzeAstro/RPC-Project/commits/master").text

# soup=BeautifulSoup(html,"html.parser")


# tagAs=soup.find_all("span")

# for tag in tagAs:
#     if tag.text=="Older":
#         print(tag.get('href'))


print(get("https://github.com/AzeAstro/csso-src/tree/experimental").status_code)
