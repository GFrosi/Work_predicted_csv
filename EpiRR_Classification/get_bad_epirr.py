import argparse
import pandas as pd
import urllib.request
import lxml.html as lh
from bs4 import BeautifulSoup
import requests
from time import sleep
#from retry import retry
import os
import sys
from tqdm import tqdm 



def create_url_from_file(list_epirr_id_file):
    '''Receives a file containing the epirr IDs 
    and returns a list of url for each one'''

    url_list = []
    root = "https://www.ebi.ac.uk/vg/epirr/view/"
    
    for line in list_epirr_id_file:

        line = line.strip()
        url_path = os.path.join(root, line)
        url_list.append(url_path)

    return url_list

def get_bad_epirr(url_list):
    """Receives a list of url
    and returns two list with 
    good and bad EpiRR"""

    list_good = []
    list_bad = []

    for adrs in tqdm(url_list):

        page = requests.get(adrs)
        sleep(2)
        data = page.text
        soup = BeautifulSoup(data, 'lxml')
        epirr = adrs.split('/')[-1]
            
        for header in soup.findAll('h1'):
            info = header.text.strip()
            
            if info == "Not found":
                list_bad.append(epirr)
            else:
                list_good.append(info)      

    return list_good, list_bad


def save_list(list_bad):

    with open("bad_epirr.txt", 'w') as f:
        f.write("\n".join(list_bad))


def main():

    list_epirr = open(sys.argv[1], 'r')
    url_list = create_url_from_file(list_epirr)
    list_good, list_bad = get_bad_epirr(url_list)
    save_list(list_bad)


if __name__ == "__main__":


    main()