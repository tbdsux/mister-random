import requests
from bs4 import BeautifulSoup

gif_vif = "https://www.gif-vif.com/random/"

resp = requests.get(gif_vif).text

soup = BeautifulSoup(resp, 'html.parser')

memes = soup.find_all("div", class_="left_new_gl_mob")

for i in memes:
    print(i.find("img")['src'])