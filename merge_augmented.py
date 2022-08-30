import pandas as pd
import argparse


def load_df(file_csv):
    '''load a dataframe
    from a csv file'''

    return pd.read_csv(file_csv)


def merge_dfs(df1, df2):
    '''This function receives two dataframes.
    Returns a merged dataframe including
    all rows'''

    return df1.merge(df2,how='left', left_on='MD5', right_on='MD5')


def save_df(df, path):
    '''Save df as csv file'''
              
    df.to_csv(path, index = False)



def main():

    df1 = load_df(args.file)
    df2 = load_df(args.FILE)
    df3 = merge_dfs(df1, df2)
    save_df(df3, args.out)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="a script to merge two dataframes keeping all rows"
    )

    parser.add_argument('-f', '--file', action="store", help='first csv file to be loaded. This file will be the major df to the merge command', required=True)
    parser.add_argument('-F', '--FILE', action="store", help='second csv file to be loaded and merged with the first one', required=True)
    parser.add_argument('-o', '--out', action="store", help='Path to save the merged csv file with the new columns', required=True)


    args = parser.parse_args()
    main()
