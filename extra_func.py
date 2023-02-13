import streamlit as st
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup


def read_up_file(uploaded_file,ftype='stringio',cut=None): 
    if uploaded_file is not None:
        # To convert to a string based IO:
        if ftype=='stringio':
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            return stringio

        # To read file as string:
        elif ftype=='string_data':
            string_data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
            if cut:
                return string_data[:cut]
            else:
                return string_data

        # Can be used wherever a "file-like" object is accepted:
        elif ftype=='dataframe':
            dataframe = pd.read_csv(uploaded_file)
            return dataframe
        else:
            return uploaded_file.getvalue()

def parse_text_tag(text,tag):
    soup = BeautifulSoup(text, 'html.parser')
    return [tag.text for tag in soup.find_all(tag)]

def create_dict(list1, list2): 
    if len(list1) != len(list2): 
        return 'Lists must be of equal length!' 
    return dict(zip(list1, list2)) 

def snippets_dict_get(snippets_path,reverce=True):
    with open(snippets_path,'r') as f:
        text = f.read()
    l1 = parse_text_tag(text,'name')
    l2 = parse_text_tag(text,'split')
    if reverce:
        return create_dict(l2, l1)
    else:
        return create_dict(l1, l2)