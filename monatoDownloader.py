#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import subprocess


base = 'https://www.monato.be/'


def getLinks(link):
    page = requests.get(str(link))
    soup = BeautifulSoup(page.content, 'html.parser')
    return [lk for lk in soup.find_all('a') if lk.attrs['href'][-4:] == '.pdf']


def downloadYear(year):
    lnks = getLinks(base + f'{year}/pdfindex.php')
    if len(lnks) == 0:
        lnks = getLinks(base + f'{year}/index.php')
    for elm in lnks:
        nm = elm.attrs['href']
        lnk = base + f'{year}/' + nm
        print(lnk)
        subprocess.call(['wget', '-O', nm, lnk])


for year in range(1980, 2019):
    downloadYear(year)
