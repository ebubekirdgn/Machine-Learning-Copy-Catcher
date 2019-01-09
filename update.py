# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
from tkinter import*
from tkinter import filedialog
from tkinter import messagebox
import codecs
from sklearn.neighbors import NearestNeighbors
import re
import os
from sklearn.feature_extraction.text import CountVectorizer
from TurkishStemmer import TurkishStemmer
from nltk.corpus import stopwords
stemmer = TurkishStemmer()
vectorizer = CountVectorizer()
from sklearn.decomposition import PCA
# %% Methodlar baslangic
x= None
dizi=[]
testSayisi = None
testingFiles=[]
tutorialFiles=[]
# %% Methodlar

def cleanStopWords(words):
    stop_words = set(stopwords.words('turkish'))
    cleanList = []
    for word in words:
        if word not in stop_words:
            cleanList.append(word)
    return cleanList

def testingObject():
    global x,cleanContent, testSayisi,cleanList,testingFiles
    #Encoding yapılacak
    testingFiles = filedialog.askopenfilenames(initialdir="/", title="Select file",filetypes=(("Text files", "*.txt"),("Doc files", "*.doc"),("Doc files", "*.docx"), ("Doc files", "*.docx"),("All Files", "*.*")))
    i = 1
    
    print(testingFiles)
    
    for file in testingFiles:
        LbFile.insert(END,"Test Verisi : " + os.path.basename(file))
        file_content = codecs.open(file,'r',encoding='utf8').read()
        content = file_content.lower()
        words = re.findall(r'\w+', content)
        cleanList = cleanStopWords(words)         
        cleanContent =' '.join(cleanList)
        #print(cleanContent)
        dizi.append(cleanContent)        
        testSayisi = len(dizi)
 
def tutorialObject():
        global x,cleanContent,tutorialFiles,cleanList
        tutorialFiles = filedialog.askopenfilenames(initialdir="/", title="Select file",filetypes=(("Text files", "*.txt"),("Doc files", "*.doc"),("Doc files", "*.docx"), ("Doc files", "*.docx"),("All Files", "*.*")))
        for file in tutorialFiles:
            LbFile.insert(END, "Eğitim Verisi : " + os.path.basename(file))
            file_content = codecs.open(file,'r',encoding='utf8').read()
            content = file_content.lower()
            words = re.findall(r'\w+', content)
            cleanList = cleanStopWords(words)
            cleanContent=' '.join(cleanList)
            #print(cleanContent)
            dizi.append(cleanContent)
    
        x = vectorizer.fit_transform(dizi).toarray()
        print(x)
        
        
def resultFunction():
    LblResult.delete(0,END)
    global x, testSayisi,dizi
    x = PCA().fit_transform(x)
    number = int(e1.get())
    print(number)
    if len(tutorialFiles) >= number:
        nbrs = NearestNeighbors(n_neighbors=number, algorithm='auto', metric='cosine').fit(x[testSayisi:])
        distances, indices = nbrs.kneighbors(x[0:testSayisi])
        i = 0
        for distance in distances:
            j = 0
            for indice in indices:
                if i == j:
                    distance = distance -1
                    distance *= -1
                    distance *= 100
                    z=0
                    for k in indice:
                            print()
                            LblResult.insert(END,os.path.basename(testingFiles[i]) + " dosyası " + os.path.basename(tutorialFiles[k])+" dosyasına "+" % "+str(abs(distance[z])) + " benziyor.")
                            z+=1
                    LblResult.insert(END,"\n")
                j += 1
            i += 1
    else:
        messagebox.showinfo("Hata Mesajı", "K değeri ; Eğitim verisi sayısından küçük ya da eşit olmalıdır.")
     
# %% Form çizme
pencere = Tk()
pencere.title("Text Similarity 1.0")
pencere.geometry("700x320")
# grid form çizdirme
uygulama = Frame(pencere)
uygulama.grid()
# %% 1.Bolme
L1 = Label(uygulama, text="Dosyalar")
L1.grid(row=0,column=0)

LbFile = Listbox(uygulama, width = 40)
LbFile.grid(row=1,column=0,padx=20)

btnFileTest = Button(uygulama, text="Test Verileri Yükle", width=20, command=testingObject)
btnFileTest.grid(row=2,column=0,padx=20,pady=15)
# %%  2.Bolme
L2 = Label(uygulama, text="Test Sonuçlari")
L2.grid(row=0,column=1)

LblResult = Listbox(uygulama, width = 55)
LblResult.grid(row=1,column=1,padx=60)

btnResult = Button(uygulama, text=" Sonuçları Göster ", width=20, command=resultFunction)
btnResult.grid(row=2,column=1,padx=20,pady=15)

L3 = Label(uygulama, text="K Değerini Giriniz :")
L3.grid(row=3,column=1)

e1 = Entry(uygulama)
e1.grid(row=4, column=1)

btnTutorial = Button(uygulama, text="Eğitim Verileri Yükle", width=20, command=tutorialObject)
btnTutorial.grid(row=3,column=0,padx=10,pady=5)
# %% formu çiz
pencere.mainloop()
