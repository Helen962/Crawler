import os
import sys
import math
import pickle
import json
import indexer 

def handle_input(s):
    all=""
    for char in s:
        if not char.isascii() or not char.isalnum():
            all+=" "
        else:
            all+=char.lower()
    input=indexer.Count(all.split())
    return input

def handle_query(data,input):
    query=dict()
    query_length=0
    for i in input:
        tf=input[i]
        for j in data[i]:
            df = data[i][j][3]
            break
        wt=tf*df
        query_length+=wt**2
        query[i]=wt
    query_length= query_length**(1/2)
    for i in query:
        query[i]=query[i]/query_length
    return query

def handle_doc(data,input,doc_length):
    doc=dict()
    for i in input:
        dic=dict()
        for j in data[i]:
            itf= data[i][j][1]
            wt = itf*1
            dic[j] = wt/doc_length[j]
        doc[i] = dic
    return doc
            
def cos_scores(query,doc):
    score=dict()
    for i in query:
        for j in doc[i]:
            if j not in score:
                score[j]=doc[i][j]*query[i]
            else:
                score[j]+=doc[i][j]*query[i]
    list = sorted(score.items(),key = lambda item: item[1],reverse=True)
    return list
    
def net_scores(query,cos_s,tag_s):
    score=dict()
    for i in query:
        for j in cos_s:
            try:
                s=0
                if tag_s[i][j[0]]:
                    t=tag_s[i][j[0]]
                    s=(t[0]*0.4+t[1]*0.3+t[2]*0.2+t[3]*0.2+t[4]*0.2)/sum(t)
                    if j[0] not in score:
                        score[j[0]]=j[1]
                    score[j[0]]+=s
            except: pass
    for j in cos_s:
        if j[0] not in score.keys():
            score[j[0]] = j[1]
    list = sorted(score.items(),key = lambda item: item[1],reverse=True)
    return list

if __name__ == "__main__":
    link_json = json.load(open('/Users/yangtang/Desktop/MINIDATA/bookkeeping.json'))
    with open('index.pickle', 'rb') as f:
        data = pickle.load(f)
    with open('doc_length.pickle', 'rb') as f2:
        doc_length = pickle.load(f2)     
    with open('tags.pickle', 'rb') as f3:
        tags = pickle.load(f3)  
    
    input = handle_input('Informatics') 
    #input = handle_input('Mondego') 
    #input = handle_input('Irvine') 
    #input = handle_input('artificial intelligence') 
    #input = handle_input('computer science') 
    
    #print(input)
    query=handle_query(data,input)
    #print("query: ",query)
    doc=handle_doc(data,input,doc_length)
    cos_scores=cos_scores(query,doc)
    #print(cos_scores)
    net=net_scores(query,cos_scores,tags)[:20]
    for i in net:
        print("Doc_ID:",i[0],"    Score:",i[1])
        print("Link:",link_json[i[0]])
        print()
    #print(net[20:])
    