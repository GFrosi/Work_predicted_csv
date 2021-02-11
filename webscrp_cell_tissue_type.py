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
# import sys
import csv

def get_epirr(epi_json):

    '''This function receives a json file and return a list of epirr'''
    
    list_epirr_id = []

    epi = open(epi_json)
    epiatlas = json.load(epi)

    for dset in epiatlas['datasets']:
        if 'epirr_id' in dset:
            list_epirr_id.append(dset['epirr_id'])

    return list(set(list_epirr_id))



def create_url(list_epirr_id):
    '''This function receives a list of epirr and return a list of url for each one'''

    url_list = []
    root = "https://www.ebi.ac.uk/vg/epirr/view/"
    for epirr in list_epirr_id:
        url_path = os.path.join(root, epirr)
        url_list.append(url_path)
    
    return(url_list)



def get_info(urls):

    """Function to web scrap the EBI pages. This function receives a web address and return 3 lists 
    with the EpiRR, cell_type and tissue_type, respectively."""

    epirr_list = []
    cell_list = []
    tissue_list = []

    for adrs in urls:
        print(adrs)

        page = requests.get(adrs)
        sleep(2)
        data = page.text
        soup = BeautifulSoup(data, 'lxml')

        info = soup.findAll("dt") #it is a list
    
        epirr = soup.find("h1")
        epirr_list.append(epirr.text)

        for index,ele in enumerate(info):

            if ele.get_text() == "tissue_type":
                tissue = ele.find_next("dd")
                tissue_list.append(tissue.text)

            if ele.get_text() == "cell_type":
                cell = ele.find_next("dd")
                cell_list.append(cell.text)
                break

            if index == (len(info) -1):
                cell_list.append('NA')
                
    return epirr_list, cell_list, tissue_list


def write_csv_file(path, epirr_list, cell_list, tissue_list):

    '''write a csv file with the infos from the 3 lists generated by the previous function'''
    
    with open(path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(zip(epirr_list, cell_list, tissue_list))


def load_df(file_csv):
    
    '''load a dataframe from a csv file'''

    df = pd.read_csv(file_csv)
        
    return df


def create_dict(df, dict_k, dict_v):

    '''Function to create a dict from dataframe columns. You should pass a dataframe and the column names to be used as keys and values, respectively.'''

    dict_epirr = dict(zip(df[dict_k], df[dict_v]))
    # dict_epirr = {key:row.tolist() for key,row in df.set_index('epirr_id').iterrows()}
    return dict_epirr


def create_new_columns(df, cell_dict, tissue_dict):
    #I can adjust to the column names and the key name 
    '''Function to create new columns in a copy of the original df. Ypu shpuld pass a df, and two dictionaries with the desired value informaiton to be
    added as new columns. In this case the column names and the keys to be accessed are alredy defined'''

    df_final = df.copy()
    df_final['cell_type_extracted'] = df_final['epirr_id'].map(cell_dict)
    df_final['tissue_type_extracted'] = df_final['epirr_id'].map(tissue_dict)

    return df_final
    

def save_df(df, path):

    '''Save df as csv file'''
              
    df.to_csv(path, index = False)


def main():

    # epirr_list = get_epirr(args.json)
    # urls = create_url(epirr_list)
    # list_epi, list_cell, list_tissue = get_info(urls)
    # write_csv_file(args.output, list_epi, list_cell, list_tissue)
    
    
    df_epirr = load_df(args.file)
    df_aug = load_df(args.augmented)
    cell_dict = create_dict(df_epirr, 'epirr_id', 'cell_type')
    tissue_dict = create_dict(df_epirr, 'epirr_id', 'tissue_type')
    df_final = create_new_columns(df_aug, cell_dict, tissue_dict)
    save_df(df_final, args.OUT)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="A script to extract the tissye_type anc cell_type from EBI (epirr information)"
    
    parser.add_argument('-j', '--json', action="store", help='Path to epiatlas_json file', required=True)

    parser.add_argument('-o', '--output', action="store", help='Path to output file with the extracted information (i.e cell_type and tissue_type. CSV extension)', required=True)

    parser.add_argument('-f', '--file', action="store", help='Path to csv file with the extracted epirr, cell_type and tissue_type (the output file generated before)', required=True)

    parser.add_argument('-a', '--augmented', action="store", help='Path to augmented csv file generated by EpiLaP', required=True)
    
    parser.add_argument('-O', '--OUT', action="store", help='Path to the final csv file with the new columns', required=True)

    args = parser.parse_args()
    main()