import mysql.connector
import nltk
import numpy as np
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords 
from scipy import spatial

def Similaritecosinus(idp1,idp2)  :
    return(1 - spatial.distance.cosine(matriceBin[idp1],matriceBin[idp2]))#matriceBin[idp1] ligne kemla 

#matriceBin[idp1] ligne kemla 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="recommendationtest"
)

mycursor = mydb.cursor()


mycursor.execute("SELECT * FROM test ")

myresult = mycursor.fetchall()




stop=set(stopwords.words())

stop = list(stop)

stop.extend([".",";","!",",",":"])

stemmer = EnglishStemmer()

#cration d1 ojet qui sauvegrade tout les mots unique de Motsteam dhors de loop
MotsUniques=set()
#nombre du columns du matrice = nbre du mots uniques
NBMots=0
NBProduit=0
#creation objet qui sauvegarde la description Motsteem
DictMots={}


description=""
for x in myresult:
    
 
  descrip=x[4]
  category=x[5]
  title=x[6]
  description= title+ ":" +category + ":" +descrip 
  print('\n')
  print(description)
  mots = nltk.word_tokenize(description)
  #print(mots)
  
  
  #suppr stopwords
  Mots=[m for m in mots if m not in stop ]
  print(Mots)
   
  #stemming
   #stemming
  
  MotsStem=[]
  
  for i in Mots :
      MotsStem.append(stemmer.stem(i))
  print("----------------------")
  print( MotsStem)
  print("Code Book :",x[0])
  NBProduit+=1
  
 #Sauvegarder les Mots uniques dans MotsUniques
  for m in MotsStem :
      MotsUniques.add(m)
      DictMots[x[0]]=MotsStem
        

print("Produits sauvegarder :")
print(MotsUniques)
NBMots=len(MotsUniques)

print("Nombre de Mots sans redondance:",NBMots)#j
print("Nombre du produit :",NBProduit)#i

#Creation Matrice binaire qui contient les mots unique 

matriceBin= np.zeros((NBProduit,NBMots))#Matrice rempli par zero

#Parcours description pour avoir si on doit lui affcter 1 ou pas
print("Ma description :")
print(DictMots)

#for i in range(NBProduit):#produit
    #j=0 #indicemotuniques
    #for m in MotsUniques:#mots bidha
        
        #if m in DictMots[i+1] :
         #   matriceBin[i][j]=1
        #j+=1

#Calcule du similarité produit produit 2 a 2
MatriceSimilariteBin=np.zeros((NBProduit,NBProduit))
for s in range(NBProduit):
    for z in range(NBProduit):
        MatriceSimilariteBin[s][z]= Similaritecosinus(s,z)
print(MatriceSimilariteBin)
#maximum

#maximum


top=[]
tops=[]



for s in range(NBProduit):
    first=0
    second=0
    third=0
    for z in range(NBProduit):
       if (MatriceSimilariteBin[s][z]>first) and (MatriceSimilariteBin[s][z]<1):
           first=MatriceSimilariteBin[s][z]
           idfirst= str(z+1)
        
    for y in range(NBProduit):
       if (MatriceSimilariteBin[s][y]>second) and (MatriceSimilariteBin[s][y]<first):
           second=MatriceSimilariteBin[s][y]
           idsecond= str(y+1)
                  
    for x in range(NBProduit):
       if (MatriceSimilariteBin[s][x]>third) and (MatriceSimilariteBin[s][x]<second):
            third=MatriceSimilariteBin[s][x]
            idthird= str(x+1)
    
    
    print ("top 1 du film ",str(s+1),"est le film ",idfirst)    
    print ("top 2 du film ",str(s+1),"est le film ",idsecond) 
    print ("top 3 du film ",str(s+1),"est le film ",idthird)
    
    top=[idfirst,idsecond,idthird ]    
    #print(top)
    tops.append(top)
        

print(tops)
#stmt= """INSERT INTO film_similaire (idfilm,ids1,ids2,ids3,) VALUES (%s, %s,%s, %s)"""
#cursor.executemany(stmt, tops)
for c, p in enumerate(tops):
    format_str = """INSERT INTO TopOffre(offre,top1,top2,top3)
    VALUES ({idbook}, '{idfirst}', '{idsecond}', '{idthird}')
   ;"""

    sql_command = format_str.format(idbook=c+1, idfirst=p[0], idsecond=p[1], idthird=p[2], )
    print(sql_command)
    mycursor.execute(sql_command)
    



mydb.commit()
mydb.close()

    
mydb.close()

    