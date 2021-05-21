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

mycursor = mydb.cursor()


mycursor.execute("SELECT * FROM emplois ")

myresult = mycursor.fetchall()

#print(myresult)

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
  exigence=x[6]
  description= descrip+ ":" +category + ":" +exigence
  print('\n')
  print(description)
  mots = nltk.word_tokenize(description)
  #print(mots)
  
  
  
