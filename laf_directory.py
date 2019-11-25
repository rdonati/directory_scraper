from bs4 import BeautifulSoup
import requests
import os

count = 0
done = False
names = []

while(not done):
    url = "https://search.lafayette.edu/?query=*&type=directory&start=" + str(count) + "&engine=directory"
    site = requests.get(url)
    soup = BeautifulSoup(site.text, "html.parser")
    results = soup.find_all('h4', itemprop = "name")
    if(len(results) == 0):
        done = True
    for result in results:
        names.append(result)
    count += 10
    print(count)
    
for name in names:
    print(name.getText())

def printSomething():
    print("Something")

