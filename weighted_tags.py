import os
import sys
import math
from bs4 import BeautifulSoup
import pickle

def tokenize(soup):
    token_string = ""
    for character in soup:
        if (character.isascii() and character.isalnum()) == True:
            token_string += character.lower()
        else:
            token_string += " "
    token_list = token_string.split()
    return token_list

def Count(all):
    result={}
    for i in all:
        if not result.get(i):
            result[i]= 1
        else:
            result[i]+= 1
    return result

def handle_importance(path,identifier):
    contents = open(path, "r")
    d=dict()
    title=None
    bold=None
    h1=None
    h2=None
    h3=None
    try:
        soup = BeautifulSoup(contents,"lxml")
        if soup.title != None:
            title=Count(tokenize(soup.title.text)) 
        for content in soup.find_all(['strong','b']):
            bold=Count(tokenize(content.text))
        if soup.h1 != None:
            h1=Count(tokenize(soup.h1.text))
        if soup.h2 != None:
            h2=Count(tokenize(soup.h2.text))
        if soup.h3 != None:
            h3=Count(tokenize(soup.h3.text))     
    except:
        pass 
    if title!=None:
        for i in title:
            if i not in d:
                d[i]=[title[i],0,0,0,0]
            else: d[i][0]+=title[i]
    if bold!=None:
        for i in bold:
            if i not in d:
                d[i]=[0,bold[i],0,0,0]
            else: d[i][0]+=bold[i]
    if h1!=None:
        for i in h1:
            if i not in d:
                d[i]=[0,0,h1[i],0,0]
            else: d[i][2]+=h1[i]
    if h2!=None:
        for i in h2:
            if i not in d:
                d[i]=[0,0,0,h2[i],0]
            else: d[i][3]+=h2[i]
    if h3!=None:
        for i in h3:
            if i not in d:
                d[i]=[0,0,0,0,h3[i]]
            else: d[i][4]+=h3[i]
    return d
 
        
def create_index(path):
    index=dict()
    for root, dirs, files in os.walk(path):
        for name in files:
            document = os.path.join(root,name)
            try:
                name=int(name)
                identifier = root[root.rfind('/')+1:]+document[document.rfind('/'):]
                d=handle_importance(document,identifier)
                for i in d:
                    if i not in index:
                        index[i]=dict()
                    index[i][identifier]=d[i]
            except:
                pass
    d=index.copy()
    for i in d:
        title=bold=h1=h2=h3=0 
        for j in d[i]:
            title+=d[i][j][0]
            bold+=d[i][j][1]
            h1+=d[i][j][2]
            h2+=d[i][j][3]
            h3+=d[i][j][4]
        for j in d[i]:
            if title != 0: d[i][j][0] = d[i][j][0]/title
            if bold != 0: d[i][j][1] = d[i][j][1]/bold
            if h1 != 0: d[i][j][2] = d[i][j][2]/h1
            if h2 != 0: d[i][j][3] = d[i][j][3]/h2
            if h3 != 0: d[i][j][4] = d[i][j][4]/h3
    return index
      


if __name__ == "__main__":   
    path = "WEBPAGES_RAW" # path to WEBPAGES_RAW
    with open('tags.pickle', 'wb') as f:
        pickle.dump(create_index(path), f, -1)


