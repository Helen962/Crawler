import os
import sys
import math
from bs4 import BeautifulSoup
import pickle
stopWords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
                  "aren't", "as",
                  "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
                  "can't", "cannot",
                  "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
                  "during", "each",
                  "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
                  "having", "he", "he'd",
                  "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how",
                  "how's", "i", "i'd",
                  "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself",
                  "let's", "me", "more", "most",
                  "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
                  "other", "ought", "our", "ours",
                  "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's",
                  "should", "shouldn't", "so",
                  "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
                  "then", "there", "there's",
                  "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to",
                  "too", "under", "until",
                  "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't",
                  "what", "what's", "when",
                  "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's",
                  "with", "won't", "would",
                  "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
                  "yourselves"]

def tokenize(path):
    contents = open(path, "r")
    final_list=[]
    try:
        soup = BeautifulSoup(contents, "lxml")  
        # BeautifulSoup is a Python package for working with broken HTML
        token_string = ""
        for character in soup.text:
            if (character.isascii() and character.isalnum()) == True:
                token_string += character.lower()
            else:
                token_string += " "
        token_list = token_string.split()
        token_list = [x for x in token_list if x not in stopWords]
        for i in token_list:
            if not i.isnumeric(): 
                final_list.append(i)
    except:
        pass
    return final_list

def Count(all):
    result={}
    for i in all:
        if not result.get(i):
            result[i]= 1
        else:
            result[i]+= 1
    return result

def create_index(path):
    l=[]
    count=0 
    for root, dirs, files in os.walk(path):
        for name in files:
            document = os.path.join(root,name)
            try:
                name=int(name)
                count+=1
                identifier = root[root.rfind('/')+1:]+document[document.rfind('/'):]
                l.append([document,identifier])
            except:
                pass
    return count,l


def df_score(l):
    df = dict()
    for document,identifier in l:
        a=Count(tokenize(document))
        for b in a: 
            if b not in df:
                df[b]=1
            else:
                df[b]+=1
    return df


def build_index(l,dfl,N):
    index = dict()
    doc_length=dict()
    for document,identifier in l:
        length=0
        a=Count(tokenize(document))
        for b in a: 
            if b not in index:
                index[b]=dict()
            tf=a[b]
            itf=1+math.log10(tf)
            df=dfl[b]
            idf=math.log10(N/df)
            wt=itf*idf
            l=[tf,itf,df,idf,wt]
            index[b][identifier]=l
            if identifier not in doc_length:
                doc_length[identifier]=0
            doc_length[identifier]+=l[-1]**2
    for i in doc_length:
        doc_length[i]=doc_length[i]**(1/2)
    return index,doc_length


if __name__ == "__main__":
    path = "WEBPAGES_RAW" # path to WEBPAGES_RAW

    l=create_index(path)
    N=l[0]
    print("count: ",N)
    dfl= df_score(l[1])
    print("unique_word: ", len(dfl))
    index,doc_length = build_index(l[1],dfl,N)
    with open('index.pickle', 'wb') as f:
        pickle.dump(index, f, -1)
    with open('doc_length.pickle', 'wb') as f2:
        pickle.dump(doc_length, f2, -1)
    


    
    
