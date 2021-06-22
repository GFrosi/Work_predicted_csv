import argparse
import pandas as pd
import urllib.request
import lxml.html as lh
from bs4 import BeautifulSoup
import requests
from time import sleep
#from retry import retry
import json
import os
import sys
import csv
from collections import Counter
import json 
from tqdm import tqdm 


def create_url_from_file(list_epirr_id_file):

    '''This function receives a list of epirr and return a list of url for each one, and a dictionay with EpiRR as keys and a 
    empty list as value'''

    dict_epirr = {}
    url_list = []
    root = "https://www.ebi.ac.uk/vg/epirr/view/"
    
    for line in list_epirr_id_file:

        line = line.strip()
        url_path = os.path.join(root, line)
        url_list.append(url_path)
        dict_epirr[line] = []
    
    return(url_list, dict_epirr)


def get_target(urls, dict_epirr):

    """Function to web scrap the EBI pages. This function receives a list of urls and a dictionary. It returns a dict
    with EpiRR as keys and the targets per EpiRR in a list as values."""

    for adrs in tqdm(urls):

        page = requests.get(adrs)
        sleep(2)
        data = page.text
        soup = BeautifulSoup(data, 'lxml')
        
        epirr = adrs.split('/')[-1]
       
        for td in soup.findAll('tbody'):
            # z = []
            
            info = td.text #several \n string
            

            l = info.strip().split('\n') #string to list
            
            
            j = [] #list to receive no empty elements
            
            for  n, e in enumerate(l):
                
                if len(e) <= 1 and l[n+1] == 'View in archive': #empty col (blank element) = Secondary ID col. In this case, we will append 'Secondary ID' to fill the space
                    j.append('Secondary ID')

                elif len(e) > 1:
                    j.append(e) #filtered list

            count = 1
            for i, c in enumerate(j):
                if i == count:
                    # print(c, i)
                    count += 6

                    dict_epirr[epirr].append(c)

    return dict_epirr



def updt_dict_others(dict_epirr):

    '''This funcion receives a dictionary and returns an updated dictionary with no histones values replaced by Others'''

    updated_dict = dict_epirr.copy()


    for k, v in updated_dict.items():

        for i,ele in enumerate(v):

            if 'Histone' not in ele:
                

                v[i] = 'Others'

                updated_dict[k] = v
                
                
    return updated_dict


def updt_dict_hist(updated_dict):

    '''This function receives a dictionary and returns an updated dictionary without the name Histones, just the modification'''
    
    new_dict = updated_dict.copy()

    for k,v in new_dict.items():

        for i,ele in enumerate(v):

            if 'Histone' in ele:

                v[i] = ele.split(' ')[1]

                # print(v) #check replacement

                

                new_dict[k] = v

    return new_dict


def count_elem(new_dict):       
  
    '''This function receives a dict and returns a dict where the values are lists of tupes containig the count per target per EpiRR (keys)'''

    for k,v in new_dict.items():

        # print(v)

        counter = Counter(v)
        
        l_counter = [(i, j) for i,j in counter.items()]
        
        new_dict[k] = l_counter

    return new_dict


def create_dict_empty(new_dict_tuple):
    
    '''This function receives a dict of tuples and returns a dict with EpiRR as keys and a list of zeros 
    (len=7; representing 7 colums) as values'''

    return  {k: list([0,0,0,0,0,0,0]) for k in new_dict_tuple.keys()}


def org_counts(new_dict_tuple, dict_matrix):
    
    '''receives a dict of tules and a dict of matrix (empty) and returns a dict with EpiRR as keys and 
    and a list of count of samples per histone as values (index represents each histone of interest)'''

    dict_histones = {'H3K27ac':0, 'H3K27me3':1,'H3K36me3':2, 'H3K4me1':3,'H3K4me3':4,'H3K9me3':5, 'Others':6}

    for k,v in new_dict_tuple.items():

        for tup in v:
            
            index = dict_histones[tup[0]] #getting value of index 
            dict_matrix[k][index] = tup[1]

          
    return dict_matrix


def write_result(dict_matrix):

    '''receives a dict and prints a csv file where the head is: H3K27ac, H3K27me3, H3K36me3, H3K4me1, H3K4me3, H3K9me3, Others'''
    
    for k,v in dict_matrix.items():
        m = map(str, v)
        # m = ','.join()
        print(k + "," + ','.join(m))



def main():

    list_epirr = open(sys.argv[1], 'r')
    url_list, dict_epirr = create_url_from_file(list_epirr)
    dict_list_targets = get_target(url_list, dict_epirr)
    others_dict = updt_dict_others(dict_list_targets)
    new_dict = updt_dict_hist(others_dict)
    new_dict_tuple = count_elem(new_dict)
    dict_matrix = create_dict_empty(new_dict_tuple)
    new_dict_matrix = org_counts(new_dict_tuple, dict_matrix)
    write_result(new_dict_matrix)



if __name__ == "__main__":


    main()


