# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 15:23:55 2017
@author: Aditya
"""
from urllib import request
import json
def url_parser(f):
    st_link=f.find('<a href="')
    if st_link == -1:
        return 0,0
    st_quote = f.find('"',st_link+1)
    end_quote = f.find('"',st_quote + 1)
    return f[(st_quote + 1):end_quote],end_quote

def get_all_links(f):
    url_list = []
    while True: 
        url, endpos = url_parser(f)   
        url_list.append(url)
        if url and endpos:  
            f = f[endpos:] 
        else:
            return url_list
            break  
       
def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)
    return p 

def add_to_index(index,keyword,url):
    if index.get(keyword):
        index[keyword].append(url)
    else:
        index[keyword] = [url]
    return index    
        
def lookup(index,keyword):
    if index.get(keyword):
        print(index.get(keyword))
        
index = {}              
to_crawl = []   
crawled = []  
f = str(open('udacity.html','rb').read())
to_crawl = get_all_links(f) 
file_index = open('website_indexes.txt','w')
file = open('website_links1.txt','w')
j = 0
for i in to_crawl:
    try:
        r = request.urlopen(i)          
        bytecode = r.read()
        html = bytecode.decode()
        s = html.split() 
        for k in range(0,len(s)):
            index = add_to_index(index,s[k],i)
            
#        tmp = get_all_links(html)        
        to_crawl = union(to_crawl,get_all_links(html))
        crawled.append(i) 
        j=j+1
        if j < 10:
            file.writelines("%s\n" % i)
        if j == 10:
            file.close()
            json.dump(index, open("website_indexes.txt",'w'))
            print(index)
     
        print(i)
    except:
        pass
      