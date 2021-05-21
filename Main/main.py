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
  database="kamjobs"
)

nltk.download('punkt')


mycursor = mydb.cursor()


mycursor.execute("SELECT * FROM emplois ")

myresult = mycursor.fetchall()

#print(myresult)

stop=set(stopwords.words())


stop = list(stop)

stop.extend([".",";","!",",",":","-","_","”","’","”","“","’","/"])

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
  exigence=x[6]
  description= descrip+ ":" +category + ":" +exigence
  #print('\n')
  #print(description)
  mots = nltk.word_tokenize(description)
  #
  #print(mots)
  
  
  #suppr stopwords
  Mots=[m for m in mots if m not in stop ]
 # print(Mots)
   
  #stemming
   #stemming
  
  MotsStem=[]
  for i in Mots :
      MotsStem.append(stemmer.stem(i))
  #print("----------------------")
  #print( MotsStem)
  #print("ID Offre :",x[0])
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


