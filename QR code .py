# TIPE : DUGUEY Martin
# 2019
# 
# on souhaite créer un QR code de version 1 avec une qualité de correction M. D'après les données fournies par Denso Wave, il nous faut 16 octets de données à transmettre et 10 octets de correction
# lien utile pour génerer le polynôme générateur en fonction du nombre d'octets de correction nécessaires:
#
# https://www.thonky.com/qr-code-tutorial/generator-polynomial-tool?degree=17


############# Fonctions
import matplotlib.pyplot as plt
import numpy as np
import string

alpha=list(string.ascii_lowercase)

def iso18004(cara):
    if cara in list(range(10)):
        valeur=cara
    elif cara in alpha:
        x=alpha.index(cara)
        valeur=10+x
    elif cara==" ":
        valeur=36
    elif cara=="$":
        valeur=37
    elif cara=="%":
        valeur=38
    elif cara=="*":
        valeur=39
    elif cara=="+":
        valeur=40
    elif cara=="-":
        valeur=41
    elif cara==".":
        valeur=42
    elif cara=="/":
        valeur=43
    elif cara==":":
        valeur=44
    return(valeur)

def binaire(d):
    r=[]
    f=[]
    a=d
    while a!=0:
        if a%2==0:
            r.append(0)
            a=a//2
        if a%2==1:
            r.append(1)
            a=a//2
    if d>=45 and len(r)<11:
        r.append(0)
    if d<16 and len(r)<6:
        r.append(0)
        r.append(0)
    if d<45 and d>16 and len(r)<6:
        r.append(0)
    for i in range(len(r)):
        f.append(r[len(r)-1-i])
    final="".join(map(str, f))
    return(final)
    
def binaire2(d):
    r=[]
    f=[]
    a=d
    while a!=0:
        if a%2==0:
            r.append(0)
            a=a//2
        if a%2==1:
            r.append(1)
            a=a//2
    if len(r)<9:
        while len(r)!=9:
            r.append(0)
    for i in range(len(r)):
        f.append(r[len(r)-1-i])
    cci="".join(map(str, f))
    return(cci)
    
def binaire3(d):
    r=[]
    f=[]
    a=d
    while a!=0:
        if a%2==0:
            r.append(0)
            a=a//2
        if a%2==1:
            r.append(1)
            a=a//2
    for i in range(len(r)):
        f.append(r[len(r)-1-i])
    cci="".join(map(str, f))
    return(cci)   
  
def enc(data):
    tr1=[]
    tr2=[]
    tr3=[]
    tr3.append('0010') #on s'intéresse ici qu'à des données alpha numériques
    tr3.append(binaire2(len(data)))
    i=0
    if len(data)%2==0:
        
        while i< len(data)-1:
            tr1.append([data[i], data[i+1]])
            i=i+2
            
        for k in range(len(tr1)):
            tr2.append((iso18004(tr1[k][0])*45)+iso18004(tr1[k][1]))
        
        for p in range(len(tr2)):
            tr3.append(binaire(tr2[p]))
            
    elif len(data)%2==1:
        
        while i< len(data)-2:
            tr1.append([data[i], data[i+1]])
            i=i+2
        if i==len(data)-1:
            tr1.append([data[i]])
            
        for k in range(len(tr1)-1):
            tr2.append((iso18004(tr1[k][0])*45)+iso18004(tr1[k][1]))
        tr2.append(iso18004(tr1[len(tr1)-1][0]))
        
        for p in range(len(tr2)-1):
            tr3.append(binaire(tr2[p]))
        tr3.append(binaire(tr2[len(tr2)-1]))
    
    encod="".join(map(str, tr3)) #pour faciliter la mise en place des octets je ne laisse volontairement aucun espace lors de la jonction 
    
    
# On ajoute des 0 de manière à avoir une chaine de caractère d'une longueur multiple de 8

    final=[]
    a=len(encod)//8
    compteur=0
    k=8
    while compteur<a:
        final.append(encod[k-8:k])
        k=k+8
        compteur=compteur+1
    if len(encod)%8!=0:
        L=[]
        r=len(encod)%8
        for p in range(r):
            L.append(encod[len(encod)-1-(r-1)+p])
        while len(L)<8:
            L.append(0)
        Lf="".join(map(str, L))
    final.append(Lf)
    codeword="".join(map(str, final))
    

# On complète la chaîne
    n=len(codeword)//8
    p=16-n
    add=[]
    while p>0:
        add.append('11101100')
        p=p-1
        if p!=0:
            add.append('00010001')
            p=p-1
    fof=codeword+"".join(map(str, add))
    
    return(fof)

# 1 = module noir et 0 = module blanc
# programme pour v1 21x21

def mask(c,i,j):
    if (i+j)%3==0:
        if c[i][j]==1:
            c[i][j]=0
        elif c[i][j]==0:
            c[i][j]=1
    
def mat_img(chaine):
    
    
    # qc lié à la correction (donc M) et au masque appliqué
    qc='101101101001011'
    # transformation de la liste corr (decimale à binaire). La liste lc est obtenue en effectuant la division polynomiale comme expliquée sur: https://www.thonky.com/qr-code-tutorial/error-correction-coding 
    # La liste lc est propre à 'hello world'
    
    lc=[196,35,39,119,235,215,231,226,93,23]
    fin=[]
    for i in range(len(lc)):
        t=format(lc[i],"#010b")
        r=t.replace('b','0')
        r=t[2:]
        fin.append(r)
    corr="".join(map(str, fin))
    print(chaine+corr)
    
    
    I=[]
    for i in range(21):
        L=[]
        for k in range(21):
            L.append(1)
        I.append(L)
    # creation des patterns de détection
    # pattern haut/gauche
    
    for h in range(5): 
        I[1][h+1]=0
    for h in range(5):
        I[5][h+1]=0
    for v in range(3):
        I[v+2][1]=0
    for v in range(3):
        I[v+2][5]=0
    
    # pattern bas/gauche
    
    for h in range(5): 
        I[15][h+1]=0
    for h in range(5):
        I[19][h+1]=0
    for v in range(3):
        I[v+16][1]=0
    for v in range(3):
        I[v+16][5]=0
        
    #pattern haut/droite
    
    for h in range(5): 
        I[1][h+15]=0
    for h in range(5):
        I[5][h+15]=0
    for v in range(3):
        I[v+2][15]=0
    for v in range(3):
        I[v+2][19]=0
    
    # creation des séparateurs
    
    #separateur haut/gauche
    for h in range(8):
        I[7][h]=0
    for v in range(7):
        I[v][7]=0
        
    #separateut bas/gauche   
    for h in range(8):
        I[13][h]=0
    for v in range(7):
        I[v+14][7]=0
        
    #separateur haut/droite
    for h in range(8):
        I[7][h+13]=0
    for v in range(7):
        I[v][13]=0
    
    #création des timings patterns
    for t in range(2,7,2):
        I[6][t+7]=0
    for t in range(2,7,2):
        I[t+7][6]=0
    
    #remplissage 
    p=20
    f=9
    j=0

    
    #1ere colonne
    
    
    for k in range(12):
        I[p-k][20]=int(chaine[j])
        mask(I,p-k,20)
        I[p-k][19]=int(chaine[j+1])
        mask(I,p-k,19)
        j=j+2
    
    #2eme colonne
    
    j=24
    for k in range(12):
        I[f+k][18]=int(chaine[j])
        mask(I,f+k,18)
        I[f+k][17]=int(chaine[j+1])
        mask(I,f+k,17)
        j=j+2
    #3eme colonne
    
    j=48
    for k in range(12):
        I[p-k][16]=int(chaine[j])
        mask(I,p-k,16)
        I[p-k][15]=int(chaine[j+1])
        mask(I,p-k,15)
        j=j+2
    
    #4eme colonne
    
    j=72
    for k in range(12):
        I[f+k][14]=int(chaine[j])
        mask(I,f+k,14)
        I[f+k][13]=int(chaine[j+1])
        mask(I,f+k,13)
        j=j+2
    
    #5eme colonne
    
    j=96
    for k in range(14):
        I[p-k][12]=int(chaine[j])
        mask(I,p-k,12)
        I[p-k][11]=int(chaine[j+1])
        mask(I,p-k,11)
        j=j+2
        
        
    
    j=124
    for k in range(15,17):
        I[p-k][12]=int(chaine[j])
        mask(I,p-k,12)
        I[p-k][11]=int(chaine[j+1])
        mask(I,p-k,11)
        j=j+2
        
    # début de l'encodage de la correction
    # l'algorithme sur https://www.thonky.com/qr-code-tutorial/error-correction-coding , nous donne:
    
    h=0
    for d in range(4):
        I[3-d][12]=int(corr[h])
        mask(I,3-d,12)
        I[3-d][11]=int(corr[h+1])
        mask(I,3-d,11)
        h=h+2
    
    h=8
    for d in range(6):
        I[d][10]=int(corr[h])
        mask(I,d,10)
        I[d][9]=int(corr[h+1])
        mask(I,d,9)
        h=h+2
    
    h=20
    for d in range(14):
        I[7+d][10]=int(corr[h])
        mask(I,7+d,10)
        I[7+d][9]=int(corr[h+1])
        mask(I,7+d,9)
        h=h+2
    
    h=48
    I[12][8]=int(corr[h])
    mask(I,12,8)
    I[12][7]=int(corr[h+1])
    mask(I,12,7)
    I[11][8]=int(corr[h+2])
    mask(I,11,8)
    I[11][7]=int(corr[h+3])
    mask(I,11,7)
    I[10][8]=int(corr[h+4])
    mask(I,10,8)
    I[10][7]=int(corr[h+5])
    mask(I,10,7)
    I[9][8]=int(corr[h+6])
    mask(I,9,8)
    I[9][7]=int(corr[h+7])
    mask(I,9,7)
    
    h=56
    for d in range(4):
        I[d+9][5]=int(corr[h])
        mask(I,d+9,5)
        I[d+9][4]=int(corr[h+1])
        mask(I,d+9,4)
        h=h+2
    
    h=64
    for d in range(4):
        I[12-d][3]=int(corr[h])
        mask(I,12-d,3)
        I[12-d][2]=int(corr[h+1])
        mask(I,12-d,2)
        h=h+2
    
    h=72
    for d in range(4):
        I[d+9][1]=int(corr[h])
        mask(I,d+9,1)
        I[d+9][0]=int(corr[h+1])
        mask(I,d+9,0)
        h=h+2
        
    
    I[13][8]=1

    
    #facteur de correction
    
    for x in range(6):
        I[8][x]=int(qc[x])
        
    
    I[8][7]=int(qc[6])
    I[8][8]=int(qc[7])
    
    
    for x in range(8):
        I[8][13+x]=int(qc[7+x])
    
    for y in range(7):
        I[20-y][8]=int(qc[y])
    
    I[7][8]=int(qc[8])
    
    for y in range(6):
        I[5-y][8]=int(qc[9+y])
        
        
    # pour pallier le problème d'affichage
    
    for i in range(21):
        for k in range(21):
            if I[i][k]==0:
                I[i][k]=1
            elif I[i][k]==1:
                I[i][k]=0
    

    A = np.array( I, dtype=np.int)

    ax=plt.imshow(A, interpolation='none', cmap=plt.gray() )
 
    nb = 21
    plt.xticks( np.arange(nb))
    plt.yticks( np.arange(nb))
 
    couleur = ['black','white']
    plt.axis("off")
    plt.show()



############# Affichage du QRCODE 'hello world'

data = enc('hello world')
mat_img(data)