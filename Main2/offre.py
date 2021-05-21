# -*- coding: utf-8 -*-
"""
Created on Tue May 26 10:13:14 2020

@author: Houssem
"""


import mysql.connector
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer
import numpy

from scipy import spatial

def SimilariteCosinus(idflm1,idflm2):
     return ( 1 - spatial.distance.cosine(matriceBin[idflm1], matriceBin[idflm2]))

"""

Anaconda prompt
pip install nltk
pip install mysql.connector
pip install ipython
pip insatall mysql 
"""
matriceBin=numpy.zeros((0,0))


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="recommendationtest"
    )

cursor = conn.cursor()

cursor.execute("SELECT * FROM test ")
stop=set(stopwords.words('english'))
stop=list(stop)
stop.extend([".",";","!","-","_","(",")","?",":",","])
stemmer = EnglishStemmer()

totalitesmots=set()
nbfilms=0
dictmots={}

for ligne in cursor.fetchall():
    nbfilms+=1
    print("ID Film:",ligne[0])
    #print("Description:",ligne[2])
    
    description=ligne[4]+ligne[5]
    
    mots=nltk.word_tokenize(description)
    #print(mots)
    
    Mots=[m for m in mots if m not in stop ]
    
    motsStem=[]
    for i in Mots:
        motsStem.append(stemmer.stem(i))
    print("-------------------------------------------")
    print(motsStem)
    for m in motsStem:
        totalitesmots.add(m)
    dictmots[ligne[0]]=motsStem    



nbmots=len(totalitesmots)
print(nbfilms)
matriceBin=numpy.zeros((nbfilms,nbmots))

for i in range(nbfilms):
    j=0
    for m in totalitesmots:
        idf=i+1
        if m in dictmots[idf]:
            matriceBin[i][j]=1
        j+=1
        
MatriceSimilariteBin=numpy.zeros((nbfilms,nbfilms))

for s in range(nbfilms):
    for z in range(nbfilms):
        MatriceSimilariteBin[s][z]=SimilariteCosinus(s,z)
print(MatriceSimilariteBin)


top=[]
tops=[]

for s in range(nbfilms):
    first=0
    second=0
    third=0
    top1 = ""
    top2 = ""
    top3 = ""
    for z in range(nbfilms):
       if (MatriceSimilariteBin[s][z]>first) and (MatriceSimilariteBin[s][z]<0.9999998):
           first=MatriceSimilariteBin[s][z]
           top1= str(z+1)
        
    for z in range(nbfilms):
       if (MatriceSimilariteBin[s][z]>second) and (MatriceSimilariteBin[s][z]<first):
           second=MatriceSimilariteBin[s][z]
           top2= str(z+1)
                  
    for z in range(nbfilms):
       if (MatriceSimilariteBin[s][z]>third) and (MatriceSimilariteBin[s][z]<second):
           third=MatriceSimilariteBin[s][z]
           top3= str(z+1)
    
    
    print ("top 1 du film ",str(s+1),"est le film ",top1)    
    print ("top 2 du film ",str(s+1),"est le film ",top2) 
    print ("top 3 du film ",str(s+1),"est le film ",top3)
    
    top=[top1,top2,top3 ]    
    #print(top)
    tops.append(top)
        

print(tops)

for c, p in enumerate(tops):
    format_str = """INSERT INTO topoffre (offre,top1,top2,top3)
    VALUES ({offre}, '{top1}', '{top2}', '{top3}') 
    ON DUPLICATE KEY UPDATE 
       top1=values(top1),
       top2=values(top2),
       top3=values(top3);"""

    sql_command = format_str.format(offre=c+1, top1=p[0], top2=p[1], top3=p[2] )
    #print(sql_command)
    cursor.execute(sql_command)
    



conn.commit()
conn.close()