# -*- coding: utf8 -*-

from __future__ import division
from random import randint
import pysynth
from TIPE_main_droite import *

#############################################################################################################
#####################---- LISTE DE TOUTES LES NOTES DU PIANO DANS L'ORDRE CROISSANT ----#####################
#############################################################################################################                                                                                                   
liste_des_notes = ['a0','a#0','b0','c1','c#1','d1','d#1','e1','f1','f#1','g1','g#1','a1','a#1','b1','c2',  ##
                   'c#2','d2','d#2','e2','f2','f#2','g2','g#2','a2','a#2','b2','c3','c#3','d3','d#3','e3', ## 
                   'f3','f#3','g3','g#3','a3','a#3','b3','c4','c#4','d4','d#4','e4','f4','f#4','g4','g#4', ##
                   'a4','a#4','b4','c5','c#5','d5','d#5','e5','f5','f#5','g5','g#5','a5','a#5','b5','c6',  ##
                   'c#6','d6','d#6','e6','f6','f#6','g6','g#6','a6','a#6','b6','c7','c#7','d7','d#7','e7', ##
                   'f7','f#7','g7','g#7','a7','a#7','b7','c8']                                             ##
#############################################################################################################
                    


############################################### première partie #############################################


def premier(n):
    for k in range(2,int(n**(0.5))+1):
        if (n//k)==(n/k):
            return(False)
    return(True)    # retourne le booléen True si un nombre est premier
        
        
def listepremier(n):
    liste=[]
    for k in range(2,n+1):
        if premier(k)==True:
            liste+=[k]               
    return(liste)   #retourne la liste des n premiers nombres premiers


L=listepremier(200000) # choix arbitraire

def decompose(n):
    m=n
    a=0                        
    while L[a]<=m:
        a+=1
    liste=[]
    for k in range(a):
        b=L[k]
        p=0
        while (m/b)==(m//b):
            p+=1
            m=m/b
        if p!=0:
            liste+=[(b,p)]
        if m==1:
            return(liste)
    return(liste)     # decompose un nombre en produit de nombres premiers

def pgcd(a,b):
    while a%b != 0:
        a,b = b,a%b
    return(b)

def ppcm(a,b):
    return (a * b) / pgcd(a,b)

def pgcdliste(liste):
    if len(liste)== 2:
        return (pgcd(liste[0],liste[1]))        
    return (pgcd(liste.pop(-1),pgcdliste(liste)))#retourne le pgcd d'une liste d'éléments
	
def ppcmliste(liste):
    if len(liste) == 2:
        return (ppcm(liste[0],liste[1]))
    return(ppcm(liste.pop(-1),ppcmliste(liste)))#retourne le ppcm d'une liste d'éléments

def degredouceur(n):
    liste = decompose(n)
    s = 1
    for u in range (len (liste)):   
        ni = liste[u][0]
        pi = liste[u][1]
        s += (ni*pi-pi)    
    return(s)               #renvoi le degré de douceur de n

def degredouceur_liste(liste):      
    a= pgcdliste(liste)
    for k in range (len(liste)):
        liste[k] = ((liste[k])/a)
    deg = ppcmliste(liste)
    return(degredouceur(deg))#renvoi le degré de douceur d'une liste d'éléments        






def combinaisonsomme(n,l):#algorithme recursif qui trouve l'ensemble des combinaisons de n 
    if n==l[0]:           #comme somme d'elements de l (l étant triée)si n est le plus petit 
        return([[n]])     #élement de l il n'y qu'une seule façon de l'écrire comme somme d'élements de l
    elif n==0:            #si n=0 il n'y a rien à faire
        return([[]])
    elif n<l[0]:          #si n est plus petit que le plus petit élément et qu'il est non nul alors c'est impossible
        return(False)
    res=[]
    
    
    l1=combinaisonsomme(n-l[-1],l)
    if l1!=False:
        for x in l1 :
        
            res.append([l[-1]]+x)    
    if len(l)>2:
        l2=l[:-1]
        res+=combinaisonsomme(n,l2)
    return(res)        


    
def couple2(d):#calcule le rapport de frequences de façon optimale par rapport à d, nombre de demis tons
    if d==1:
        return([32,30])

    Liste1=[2,3,4,5,7,8,9] #valeurs de réference                          
    Liste2=[[9,8],[6,5],[5,4],[4,3],[3,2],[8,5],[5,3]] #fréquences correspondantes 
    listecombi=combinaisonsomme(d,Liste1)
    listecouple=[]  #liste des couples p,q possibles
    for x in listecombi:
        p=1
        q=1
        for i in x:
            j=Liste1.index(i)
            p*=Liste2[j][0]
            q*=Liste2[j][1]
        listecouple.append([p,q])
    listeppcm=[]        #liste des ppcm de p et q divisés par leur pgcd (le but est qu'il soit minimal)
    for x in listecouple:
        a=x[0]
        b=x[1]
        pg=pgcd(a,b)
        pp=ppcm(a/pg,b/pg)
        listeppcm.append(pp)
    j=listeppcm.index(min(listeppcm))
    return(listecouple[j])

#################################### comparaison d'une note à une liste ##################################    
import time
def comparenoteliste(note_de_droite,listealeatoire):
    temps_depart = time.time()
    notes_triees = []
    degre_trier = []
    notes_finales = []
    liste_douceur = []
    li = []
    listetotal = []
    listefin = []       
    listedesdegres = [] #cette liste sera composée du rapport de fréquences de chaque couple
    if note_de_droite == 'r':
        return('r')     #la pause 'r' n'étant pas dans la liste des notes on en fait un cas particulier
    else:
        
        i0=liste_des_notes.index(note_de_droite) #on prend l'emplacement de la note de la main droite
        for k in range(len(listealeatoire)):
            i1=liste_des_notes.index(listealeatoire[k])
            d=abs(i0-i1)
            listetotal.append([note_de_droite,listealeatoire[k]])
            rapportfreq = couple2(d) #rapport des fréquences entre les deux notes qui sont comparées
            
            listedesdegres.append(rapportfreq)
            pg=pgcd(rapportfreq[0],rapportfreq[1])
            rapportfreq[1]/=pg
            rapportfreq[0]/=pg
            
            li.append (ppcmliste(rapportfreq))
            
            
        for t in range (len(li)):
            if li[t] < 200000:   #liste des 200000 premiers nombres premiers 
                listefin.append(listedesdegres[t])
                notes_finales.append(listealeatoire[t])         #notes_finales.append(listealeatoire[t])
        for d in range(len(listefin)):                          #est composée de nombres inférieurs à
            liste_douceur.append(degredouceur_liste(listefin[d]))    #200000 on peut alors calculer
        for k in range (len(liste_douceur)):                         # le degré de douceur 
            degre_trier.append([liste_douceur[k] ,notes_finales[k]])
            degre_trier.sort()
        for h in range (len(degre_trier)):    
            notes_triees.append(degre_trier[h][1])
        leader = notes_triees[0]
        temps_fin =time.time()
        tot = (temps_fin-temps_depart)
    return(leader,tot)  # retourne la note à superposer ayant le meilleur degré de douceur
    


    #print(listealeatoire)                                                  
    #print(listedesdegres)
    #print(listefin)
    #print(liste_douceur)
    #print(li)
    #print(notes_finales)    
    #print(degre_trier)
    #print(notes_triees)
    #print (leader)


######################################### choix des notes à comparer ########################################
    
def listenote(l):  #prend en argument la liste des notes et des temps de la main droite 
    note=[]
    for x in l:
        if x[0]!='r':
            i=liste_des_notes.index(x[0])%12
            if i not in note:
                note.append(i)
    note.sort()
    res=[]
    k=0
    while(12*(k+1))<len(liste_des_notes):
        for i in note:
            res.append(liste_des_notes[i+12*k])    
        k+=1                                      
            
    return(res) #retourne toutes les notes présentes dans la liste entrée en argument ainsi
                #que ces mêmes notes dans toutes les octaves


def aleatoire_main_gauche_intelligent(note_de_droite,n,note):#prend en argument une note de
                                                             #la main droite, un entier n, et une
    l = []                                                   #liste de notes pouvant être jouées
    listemaingauche = []                                     #par la main gauche
    if note_de_droite == 'r':
        return('r')
    else:
        indice = note.index(note_de_droite)
        listemaingauche = note[:indice]
        for k in range (n):
            l.append (listemaingauche[randint(0,len(listemaingauche)-1)])    
    return(l)  #retourne une liste de notes composée de n notes qui sont à la fois 
               #à gauche de la note "note_de_droite" et qui en plus sont les mêmes que
               #les notes présente dans la liste des notes de la main droite à une ou plusieurs
               #octaves plus basses



################################# programme du jeu de la main gauche au piano ###############################



def transforme(liste):#prend en argument une liste composée de notes et du temps qu'elles durent
    l=[]
    for k in range(len(liste)):
        if liste[k][1] not in l:
            l.append(int(liste[k][1]))#l est la liste des temps
    copie=l[:]  
    a=ppcmliste(copie)    
    for k in range(len(l)):
        l[k]=a/l[k]
    copie=l[:]
    
    b=pgcdliste(copie)
    res=[]
    for k in range(len(liste)):    
        for i in range(int((a/liste[k][1])/b)):
            res.append([liste[k][0],int(a/b)])
    return(res)      #change une liste de note pour avoir des temps reguliers


def main_gauche(listedroite):      #prend en argument une liste composée des notes de 
    note=listenote(listedroite)    #la main droite et du temps que durent chacunes d'entre elles
    
    piste1 = []
    piste2 = []
    piste3 = []
    lnotedroite = []
    liste_main_gauche = []
    liste_main_gauche2 = []
    deb = time.time()
    for k in range (len(listedroite)):
        lnotedroite.append(listedroite[k][0])
        
    for i in range(len(lnotedroite)):
        liste_main_gauche.append([lnotedroite[i],comparenoteliste(lnotedroite[i],aleatoire_main_gauche_intelligent(lnotedroite[i],8,note))])                                                                        

        piste1.append(liste_main_gauche[i][0])
        piste2.append([liste_main_gauche[i][1],listedroite[i][1]])
                                                                                                                                                          
        duree = temps_pistes(listedroite)
    fin = time.time()
    tot = fin-deb
    print('la duree de la musique sera de',duree,'secondes','complexite',tot)    
    return(piste2)#renvoie une liste composée des notes sélectionnées par le programme  
                  #ainsi que leur temps respectifs pouvant être superposées à celles de la main droite


#############################################################################################################
################################################## LE TEMPS #################################################
#############################################################################################################


############################################## le temps régulier ############################################


def temps_pistes(listedroite):#Cette fonction prend en argument une liste composée 
    liste_temps_en_secondes = []  #de notes et de leur temps respectif
    ltemps = []
    s = 0
    
    for k in range(len(listedroite)):
        ltemps.append(listedroite[k][1])
        
    for j in range(len(ltemps)):
        liste_temps_en_secondes.append(2/(ltemps[j]))
        
    for temps in range(len(liste_temps_en_secondes)):
        s += liste_temps_en_secondes[temps]
    return(s)   #renvoie le temps que la musique dure en secondes 

                
def trouve_temps(sec):
    return 2/sec      #prend le temps en secondes et le convertit en temps en musique 
                      # exemple 1 seconde = 2 temps en musique

def convertit_temps(temps):# fait l'inverse de "trouve_temps(sec)"
    res = (2/temps)
    return res

                   
        
    
def decoupe_liste(n,liste):# prend en argument un entier n et une liste composée de notes ainsi que leur temps
    l=[]                   # respectif
    reste = (len(liste)%n)
    listereste = []
    if reste >= 0:
        for k in range(len(liste)):
            if k%n == n-1:
                l.append(liste[k-(n-1):k+1])  #decoupe la liste en (len(liste)/n) morceaux
        #return l
    if reste >0:
        listereste.append(liste[-reste:]) 
    return(l+listereste)# retourne la liste composée des mêmes notes que celles entrées en argument
                        # ainsi que de leur temps respectif mais coupée en n morceaux réguliers


def decoupe_temps(n,liste):  #le n est le modulo c'est à dire le nombre de pacquets de notes rattachées à leur temps respectifs 
    lcouple_note_temps = []  #que l'on fait.La liste entrée en argument est une liste qui a été transformée par le programme 
    liste_convertie = []     #de la main gauche
    lsomme = []              
    LTEMPS = []             
    liste = decoupe_liste(n,liste)
    
    for k in range(len(liste)):
        lsomme.append(temps_pistes(liste[k])) 
                                             
    for x in range(len(lsomme)):             
        liste_convertie.append(trouve_temps(lsomme[x]))
        lcouple_note_temps.append([ liste[x][0][0] , liste_convertie[x]])
        
    return(lcouple_note_temps)# retourne une liste de notes jouées à temps réguliers 
                              #de la forme [[note,temps],[note,temps],...,[note,temps]]



#######################################  le temps irrégulier ####################################################################




def liste_variable(liste):# cette fonction retourne la liste des temps possibles par rapport à la longueur d'une liste en entrée         
    tempspossible = [6,12,18,24]
    lon = len(liste)
    for k in range(len(tempspossible)):
        if tempspossible[k] >= lon and lon > tempspossible[0]:
            l = (tempspossible[:k])
            return(l)
        else:
            if lon > tempspossible[-1]:
                return(tempspossible) #si la longueur de la liste est supérieur à 24 on peut au moin stocker 24 notes dans une        
            if lon <= tempspossible[0] and lon >= 6:     #certaine sous liste
                return([2,4,6])
            if lon < 6 and lon >= 4:
                return([2,4])    
            if lon < 4 and lon >1:
                return([2])
            if lon == 1:
                return([1]) #lorsque la longueur de la liste est 1 on ne peut pas découper plus que l'élément restant


def decoupe_en_n(liste): #le programme prend en argument une liste composée de notes et de leurs temps respectifs
    n = var_dec_temps(liste)
    lprov1 = (liste[:n])
    lprov2 = (liste[n:]) 
    return(lprov1,lprov2)    # il retourne 2 listes l'une composée des n premiers éléments et l'autre du reste


def var_dec_temps(liste):#Le programme prend en argument une liste de notes et de leur temps respectifs
    listen = liste_variable(liste)
    n = listen[randint(0,len(listen)-1)]   
    return(n)         # ce programme retourne le modulo aléatoire parmis la liste des temps possibles (cest un entier n)



def decoupe_var(liste):
    lf = []
    l = []
    temp = [0,liste]
    for k in range (len(liste)):
        if len(temp[1]) != 0:
            temp = decoupe_en_n(temp[1])  #on découpe la liste jusqu'à ce qu'elle soit vide
            l.append(temp[0])
    return(l) # retourne la liste composée des mêmes notes que celles entrées en argument
              # ainsi que de leur temps respectif mais coupée en n morceaux irréguliers
              


def decoupe_temps_irregulier(liste): #cette fonction prend en argument une liste composée de notes et de leur temps respectifs
    n = var_dec_temps(liste)
    lcouple_note_temps = []
    liste_convertie = []     
    lsomme = []             
    LTEMPS = []
    liste = decoupe_var(liste)
    
    for k in range(len(liste)):
        lsomme.append(temps_pistes(liste[k]))#lsomme est la liste des temps de chaque couple 
    for x in range(len(lsomme)):             #elle forme par exemple la liste des temps suivante[0.375, 0.75, 1.0, 1.625, 0.375, 2.5]
        liste_convertie.append(trouve_temps(lsomme[x]))
        lcouple_note_temps.append([ liste[x][0][0] , liste_convertie[x]])
    return(lcouple_note_temps)    # la fonction retourne une liste de temps irréguliers de la 
                                  #forme [[note,temps],[note,temps],...,[note,temps]]


#################################################### programme main droite ###################################################

from __future__ import division
from random import randint
#import pysynth

listenote1 = ['a0','a#0','b0',
              'c1','c#1','d1','d#1','e1','f1','f#1','g1','g#1','a1','a#1','b1',
              'c2','c#2','d2','d#2','e2','f2','f#2','g2','g#2','a2','a#2','b2',
              'c3','c#3','d3','d#3','e3','f3','f#3','g3','g#3','a3','a#3','b3',
              'c4','c#4','d4','d#4','e4','f4','f#4','g4','g#4','a4','a#4','b4',
              'c5','c#5','d5','d#5','e5','f5','f#5','g5','g#5','a5','a#5','b5',
              'c6','c#6','d6','d#6','e6','f6','f#6','g6','g#6','a6','a#6','b6',
              'c7']

listenote2 = ['a1','a#1','b1',
              'c2','c#2','d2','d#2','e2','f2','f#2','g2','g#2','a2','a#2','b2',
              'c3','c#3','d3','d#3','e3','f3','f#3','g3','g#3','a3','a#3','b3',
              'c4','c#4','d4','d#4','e4','f4','f#4','g4','g#4','a4','a#4','b4',
              'c5','c#5','d5','d#5','e5','f5','f#5','g5','g#5','a5','a#5','b5',
              'c6','c#6','d6','d#6','e6','f6','f#6','g6','g#6','a6','a#6','b6',
              'c7','c#7','d7','d#7','e7','f7','f#7','g7','g#7','a7','a#7','b7',
              'c8']
def uneoctaveplushaut(liste):
    for k in range (len(liste)):
        a=liste[k][0]
        i=listenote1.index(a)
        liste[k][0]=listenote2[i]

def uneoctaveplusbasse(liste):
    for k in range (len(liste)):
        a=liste[k][0]
        i=listenote2.index(a)
        liste[k][0]=listenote1[i]
        
def deuxfoisplusrapide(liste):
    for k in range(len(liste)):
        liste[k][1]*=2

def deuxfoispluslente(liste):
    for k in range(len(liste)):
        liste[k][1]*=0.5

def liste_des_notes(liste):
    res=[]
    for k in liste:
        res.append(k[0])
    return(res)

def compare(l,p):
    res1=[]
    res2=[]
    
    for x in l:
        if x in p :
            res1.append(x)
            if x not in res2:
                res2.append(x)
                
    return(len(res1),len(res2))


def fullrandom(liste,n):
    res=[]
    for k in range (n):
        i=randint(0,len(liste)-1)
        j=randint(0,len(liste[i])-1)
        res+=[liste[i][j]]
    return(res)
        
def compniveau1(liste,n):                                                         
    i=randint(0,len(liste)-1)
    j=randint(0,len(liste[i])-1)
    
    a0=liste[i][j]
    res=[a0]
    for k in range (n):
        l=[]
        for i in range(len(liste)):
            for j in range(len(liste[i])-1):
                if liste[i][j][0]==a0[0]:
                     l+=[[i,j]]
        if len(l)==0:
            return(res)

        else:
            m=randint(0,len(l)-1)
            p=l[m]
            i=p[0]
            j=p[1]
            a0=liste[i][j+1]
            res+=[a0]
            if liste[i][j+1][0]=='r':
                    a0=liste[i][j+2]
                    res+=[a0]
    return(res)

def compniveau2(liste,n):
    i=randint(0,len(liste)-1)
    j=randint(0,len(liste[i])-2)
    a0=liste[i][j]
    a1=liste[i][j+1]
    res=[a0,a1]
    for k in range (n):
        l=[]
        for i in range(len(liste)):
            for j in range(len(liste[i])-2):
                if liste[i][j][0]==a0[0] and liste[i][j+1][0]==a1[0]:
                    l+=[[i,j+1]]
        if len(l)==0:
            return(res)

        else:
            m=randint(0,len(l)-1)
            p=l[m]
            i=p[0]
            j=p[1]
            a0=a1
            a1=liste[i][j+1]
            res+=[a1]
    return(res)


def proceduren(l1,l2,n):
    l=[]
    for i in range(len(l1)):
            for j in range(len(l1[i])-n):
                temoin=True
                for k in range (n):
                    if l1[i][j+k][0]!=l2[-n+k][0]:
                        temoin=False
                if temoin:
                    l+=[[i,j+n]]
    return(l)

def compniveaun(liste,n,m):
    i=randint(0,len(liste)-1)
    j=randint(0,len(liste[i])-n)
    res=[]
    for k in range (n):
        res.append(liste[i][j+k])
    for k in range (m):
        n0=n
        l=proceduren(liste,res,n0)
        while len(l)<2:
            n0+=-1
            if n0==0:
                return(res)
            l=proceduren(liste,res,n0)
        h=randint(0,len(l)-1)
        p=l[h]
        i=p[0]
        j=p[1]
        a0=liste[i][j]
        res+=[a0]
    return(res)
        
    
                    
                        
def proceduren0(l1,l2,n):
    l=[]
    for i in range(len(l1)):
            for j in range(len(l1[i])-n):
                temoin=True
                for k in range (n):
                    if l1[i][j+k]!=l2[-n+k]:
                        temoin=False
                if temoin:
                    l+=[[i,j]]
    return(l)

def compniveaun0(liste,n,m):
    i=randint(0,len(liste)-1)
    j=randint(0,len(liste[i])-n)
    res=[]
    for k in range (n):
        res.append(liste[i][j+k])
    for k in range (m):
        n0=n
        l=proceduren0(liste,res,n0)
        while len(l)<2:
            n0+=-1
            if n0==0:
                return(res)
            l=proceduren0(liste,res,n0)
        h=randint(0,len(l)-1)
        p=l[h]
        i=p[0]
        j=p[1]
        a0=liste[i][j+n]
        res+=[a0]
        memoire=[i,j]
    return(res)                    
                    
    
def compositioniveaun(liste,n,m):
    i=randint(0,len(liste)-1)
    j=randint(0,len(liste[i])-n)
    memoire=[i,j]
    res=[]
    for k in range (n):
        res.append(liste[i][j+k])
    for k in range (m):
        n0=n+1
        l=[]
        while len(l)<1:
            n0+=-1
            l=[]
            if n0==0:
                return(res)
            for i in range(len(liste)):
                for j in range(len(liste[i])-n0):
                    temoin=True
                    if i==memoire[0] and j==memoire[1]:
                        temoin=False
                        print('false',liste[i][j],liste[i][j+n0],i,j)
                        
                        print
                    for k in range (n0):
                        if liste[i][j+k][0]!=res[-n0+k][0]:
                            temoin=False
                    if temoin:
                        l+=[[i,j]]
            memoire[1]+=1      
        h=randint(0,len(l)-1)
        p=l[h]
        i=p[0]
        j=p[1]
        a0=liste[i][j+n0]
        res+=[a0]
        r=max(0,j+1+n0-n)
        memoire=[i,r]
    return(res)     
    

def comp2(liste,n):
    i=randint(0,len(liste)-1)
    j=randint(0,len(liste[i])-1)
    
    a0=liste[i][j]
    res=[a0]
    for k in range (n):
        l=[]
        for i in range(len(liste)):
            for j in range(len(liste[i])-1):
                if liste[i][j]==a0:
                     l+=[[i,j]]
        if len(l)==0:
            return(res)

        else:
            m=randint(0,len(l)-1)
            p=l[m]
            i=p[0]
            j=p[1]
            a0=liste[i][j+1]
            res+=[a0]
            if liste[i][j+1][0]=='r':
                    a0=liste[i][j+2]
                    res+=[a0]                                                   
    return(res)

"""a  b  c  d  e  f  g """  
"""la si do re mi fa sol""" 
boisperdus=[['f3',4],['a3',4],['b3',2],['f3',4],['a3',4],['b3',2],['f3',4],['a3',4],['b3',4],['e4',4],['d4',2],
   ['b3',4],['c4',4],['b3',4],['g3',4],['e3',2],['r',4],['d3',4],['e3',4],['g3',4],['e3',2],['r',2],
   ['f3',4],['a3',4],['b3',2],['f3',4],['a3',4],['b3',2],['f3',4],['a3',4],['b3',4],['e4',4],['d4',2],
   ['b3',4],['c4',4],['e4',4],['b3',4],['g3',2],['r',4],['b3',4],['g3',4],['d3',4],['e3',2],['r',2],
   ['d3',4],['e3',4],['f3',2],['g3',4],['a3',4],['b3',2],['c4',4],['b3',4],['e3',2],['r',1],
   ['d3',4],['e3',4],['f3',2],['g3',4],['a3',4],['b3',2],['c4',4],['d4',4],['e4',2],['r',1],
   ['d3',4],['e3',4],['f3',2],['g3',4],['a3',4],['b3',2],['c4',4],['b3',4],['e3',2],['r',1],
   ['e3',4],['d3',4],['g3',4],['f3',4],['a3',4],['g3',4],['b3',4],['a3',4],['c4',4],['b3',4],['d4',4],['c4',4],['e4',4],['d4',4],['b3',8],['c4',8],['a3',8],['b3',2]]
notebp= liste_des_notes(boisperdus)  

chantdestempetes=[['d3',4],['f3',4],['d4',2],['r',4],['d3',4],['f3',4],['d4',2],['r',4],
    ['e4',2],['r',4],['f4',4],['e4',4],['f4',4],['e4',4],['c4',4],['a3',2],['r',4],
    ['a3',2],['d3',2],['f3',4],['g3',4],['a3',2],['r',1],
    ['a3',2],['d3',2],['f3',4],['g3',4],['e3',2],['r',1],
    ['d3',4],['f3',4],['d4',2],['r',4],['d3',4],['f3',4],['d4',2],['r',4],
    ['e4',2],['r',4],['f4',4],['e4',4],['f4',4],['e4',4],['c4',4],['a3',2],['r',4],
    ['a3',2],['d3',2],['f3',4],['g3',4],['a3',2],['r',2],['a3',2],
    ['d3',1]]
notecdt=liste_des_notes(chantdestempetes)
berseusezelda=[['b3',2],['d4',4],['a3',2],['g3',8],['a3',8],['b3',2],['d4',4],['a3',2],
    ['b3',2],['d4',4],['b4',2],['a4',4],['d4',2],['c4',8],['b3',8],['a3',2],
    ['b3',2],['d4',4],['a3',2],['g3',8],['a3',8],['b3',2],['d4',4],['a3',2],
    ['b3',2],['d4',4],['b4',2],['a4',4],['d5',1],['r',2],
    ['d5',2],['c5',8],['b4',8],['c5',8],['b4',8],['g4',2],
    ['c5',2],['b4',8],['a4',8],['b4',8],['a4',8],['e4',2],
    ['d5',2],['c5',8],['b4',8],['c5',8],['b4',8],['g4',4],['c5',4],['g5',1]]

chant_de_l_apaisemnet=[['b4',2],['a4',2],['f4',2],['b4',2],['a4',2],['f4',2],['b4',2],['a4',2],['e4',4],['d4',4],['e4',1],['r',2],
       ['b4',2],['a4',2],['f4',2],['b4',2],['a4',2],['f4',2],['b4',2],['a4',2],['e4',4],['d4',4],['e4',1],['r',2],
       ['f4',2],['c4',2],['b3',2],['f4',2],['c4',2],['b3',2],['f4',2],['e4',2],['b3',4],['a3',4],['b3',1],['r',2],
       ['f4',2],['c4',2],['b3',2],['f4',2],['c4',2],['b3',2],['f4',2],['e4',2],['b4',2],['g4',1],['r',2],
       ['a4',2],['a4',2],['a4',2],['d5',2],['d5',2],['d5',2],['g4',2],['g4',2],['g4',2],['c5',2],['g4',1],
       ['f4',2],['f4',2],['f4',2],['a#4',2],['a#4',2],['a#4',2],['e4',2],['d4',2],['a4',2],['e4',1],
       ['a4',2],['a4',2],['a4',2],['d5',2],['d5',2],['d5',2],['g4',2],['g4',2],['g4',2],['c5',2],['g4',1],
       ['f4',2],['g4',2],['a4',2],['a#4',2],['c5',2],['d5',2],['a4',2],['b4',2],['d5',2],['e5',1]]

"""a  b  c  d  e  f  g """  
"""la si do re mi fa sol"""


deuxfoisplusrapide(chant_de_l_apaisemnet)
deuxfoisplusrapide(boisperdus)
deuxfoisplusrapide(chantdestempetes)
deuxfoisplusrapide(berseusezelda)


liste=[boisperdus,chantdestempetes,berseusezelda,chant_de_l_apaisemnet]
    
        
l1=[[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],[12,1],[13,1],[14,1],[15,1],[16,1],[17,1],[18,1],[19,1],[20,1],[1,1]]
l2=[[1,2],[2,2],[4,2],[6,2],[8,2],[10,2],[12,2],[14,2],[16,2],[18,2],[20,2],[1,2]]
l3=[[1,3],[2,3],[4,3],[6,3],[7,3],[8,3],[10,3],[12,3],[13,3],[14,3],[16,3],[18,3],[19,3],[20,3],[1,3]]
l=[l1,l2,l3]


######################################## programmes finaux ###################################################################

def retouche(liste): # permetr de retoucher la piste avant la création pour éliminer les temps bizarres
    listeFin = []
    for i in range(len(liste)):
        listeFin.append([liste[i][0][0],liste[i][1]])
    return(listeFin)
    
         

def jouer_regulier(liste,n,nom_piste,nombre_de_pistes):#prend en argument une liste composée de notes et de leur temps respectifs
                                                              #un entier n ,une chaine de caractère pour nommer la musique,et un autre
                                                              #entier pour le nombre de pistes de la main gauche désirées

    pysynth.make_wav(liste, fn = nom_piste + 'droite' + ".wav") #création de la musique jouée par la main droite
    print(liste)
    for k in range(nombre_de_pistes):                             
        liste_fantome = transforme(liste)   
        piste = main_gauche(liste_fantome)
        newPiste = retouche(piste)
        pistefinale = decoupe_temps(n,newPiste)
        a = str(k)
        print(pistefinale)
        pysynth.make_wav(pistefinale, fn = nom_piste + 'gauche' + a + ".wav")#création (de la/des) musique(s) jouée(s) par la main gauche
    
def jouer_irregulier(liste,nom_piste,nombre_de_pistes):  #même principe que le programme précédant mais pour les temps irrégulier.
    pysynth.make_wav(liste, fn = nom_piste + 'droite' + ".wav") #Il n'est donc pas nécessaire de rentrer n en argument c'est le programme
    print(liste)
    for k in range(nombre_de_pistes):                           #qui le chisit
        liste_fantome = transforme(liste)   
        piste = main_gauche(liste_fantome)
        newPiste = retouche(piste)
        pistefinale = decoupe_temps_irregulier(newPiste)
        a = str(k)
        print(pistefinale)
        pysynth.make_wav(pistefinale, fn = nom_piste + 'gauche' + a + ".wav")


        



    
    
