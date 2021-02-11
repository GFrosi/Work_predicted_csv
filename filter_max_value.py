import pandas as pd 
import sys
import numpy as np 
import argparse


def load_df(file_csv):
    
    '''load a dataframe from a csv file'''

    df = pd.read_csv(file_csv)
        
    return df


def max_filter(df):
    
    '''Filter the max value for each sample and get the column name to a list. 
    Then the function will return the dataframe with the new column'''

    # df = pd.read_csv(file_csv)
    header = list(df.columns)
    
    # print(header.index('b_cells')) #check the index of the first desired column

    #depending of the csv and desired columns, the slice will change.
    col = header[36:] #getting the all desired columns to transform in a dict with their index (Cell_Type)
    col = header[2:] #directly from test_predict.csv form EpiAtlas
    dict_col = {k:v for k,v in enumerate(col)} #index as keys and col names as values
    

    CT_list = []
    for i, row in df.iterrows():
        
        # a = list(row[36:]) #creating a list with the values per sample to access the max value and the index further
        a = list(row[2:])
        
        num_max = max(a) #getting the max value (prediction) of each sample
        
        if np.isnan(num_max): #as we have some empty cells, this if solved the problem
            CT_list.append(num_max)
            continue
        
        index = a.index(num_max)
        CT_list.append(dict_col[index])

    return CT_list


def create_new_column(df, CT_list):

    df1 = df.copy()

    #df1['Predicted_CT'] = CT_list
    df1['Predicted_CS'] = CT_list
    
    return df1


def save_df(df, path):

    '''Save df as csv file'''

    df.to_csv(path, index = False)
       
            
    

def main():   

    df = load_df(args.file)
    list_ct = max_filter(df)
    df1 = create_new_column(df, list_ct)
    save_df(df1, args.output)



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="A script to extract the maximum value of prediction for each sample (row), and returns a dataframe with a new columns with the predicted target")


    parser.add_argument('-f', '--file', action="store", help='Path to csv file with the predictions)', required=True)
    parser.add_argument('-o', '--output', action="store", help='Path to output file including the new column', required=True)

    args = parser.parse_args()
    main()