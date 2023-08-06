import numpy as np
import pandas as pd
from pydataset import data


#make funtion to return list of all pydataset datasets
def lista_datasets():
    return(data())

#make funtion to print documentation of specific dataset of pydataset
def documentazione_dataset(nome_dataset):
    print(data(nome_dataset).__doc__)

#make funtion to return dataframe of secific dataset of pydataset
def importa_dataset(nome_dataset):
    return(data(nome_dataset))

#make function to return list of columns in dataframe
def lista_colonne(df):
    return(df.columns)

#make function to return type of columns in dataframe
def tipo_colonne(df):
    return(df.dtypes)

#make function to return type of column in dataframe
def tipo_colonna(df, colonna):
    return(df[colonna].dtype)

#make function to read .csv file print time taken to read and return dataframe
def leggi_csv(file_name):
    import time
    start = time.time()
    df = pd.read_csv(file_name)
    end = time.time()
    print("Tempo impiegato per leggere il file: ", end-start)
    return df

#make function to read feather file and return dataframe and print time taken to read
def leggi_feather(file_name):  
    import time
    start = time.time()
    df = pd.read_feather(file_name)
    end = time.time()
    print("Tempo impiegato per leggere il file: ", end-start)
    return df

#make function to read excel file and return dataframe
def leggi_xls(file_name):
    df = pd.read_excel(file_name)
    return df

#make function to readspecific sheet from excel file and return dataframe
def leggi_sheet(file_name, sheet_name):
    df = pd.read_excel(file_name, sheet_name)
    return df
    
#make function to read .html file and return dataframe
def leggi_html(file_name):
    df = pd.read_html(file_name)
    return df

#make function to read .json file and return dataframe
def leggi_json(file_name):
    df = pd.read_json(file_name)
    return df   

#make function to read .sql file and return dataframe
def leggi_sql(file_name):
    df = pd.read_sql(file_name)
    return df  

#make function to return dataframe with only numeric values
def numerici(df):
    return(df.select_dtypes(include=['number']))

#make function to return dataframe with only categorical values
def categorici(df):
    return(df.select_dtypes(include=['object']))

#make function to return dataframe with only boolean values
def booleani(df):
    return(df.select_dtypes(include=['bool']))

#make function to remove specific colmn from dataset
def rimuovi_colonna(df, colonna):
    return(df.drop(colonna, axis=1))

#make function to remove specific list of columns from dataset
def rimuovi_colonne(df, colonne):
    return(df.drop(colonne, axis=1))

#make function to return dataframe with list columns passed
def seleziona_colonne(df, lista_colonne):
    return(df[lista_colonne])








