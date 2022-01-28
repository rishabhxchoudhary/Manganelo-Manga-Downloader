import os
from PyPDF2 import PdfFileMerger
import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

def pdfs():    #returns a list of all images in a folder
    l=[]
    for j in os.listdir():
        l.append(j)
    t=[]
    for i in l:
        if i.endswith('pdf'):
            i=i.split('.')
            if len(i)==3:  
                i=int(i[1])
            else:
                i=float(i[1]+'.'+i[2])
            t.append(i)
    t.sort()
    pdflist=[]
    for i in t:
        pdflist.append('Ch.'+str(i)+'.pdf')
    return pdflist
    
def pdfmerger(name):
    pdfs1=[
      'Vol.1 Chapter 1: I Want To Be Invited To A Movie.pdf',
       'Vol.1 Chapter 2: I Want To Play Old Maid.pdf', 
       'Vol.1 Chapter 3: Kaguya Doesn T Know Much.pdf', 
     'Vol.1 Chapter 4: Miyuki Shirogane Wants To Answer.pdf',
       'Vol.1 Chapter 5: Kaguya Wants To Eat.pdf', 
      'Vol.1 Chapter 5.5: Extra Chapter.pdf',
       'Vol.1 Chapter 6: Miyuki Shirogane Wants To Hide.pdf', 
        'Vol.1 Chapter 7: Fujiwara Wants To Go On A Trip.pdf', 
       'Vol.1 Chapter 8: Kaguya Wants To Be Answered.pdf', 
       'Vol.1 Chapter 9: Kaguya Wants To Walk.pdf',
        'Vol.1 Chapter 10: The Student Council Wants To Play A Prank.pdf', 
        'Vol.1 Chapter 10.5: Volume 1 Extras.pdf', 
        ]
    merger = PdfFileMerger()
    for pdf in pdfs1:
        merger.append(pdf)
    merger.write(name+'.pdf')
    merger.close()
# print(os.listdir())
name=input('Enter name of final pdf :')
pdfmerger(name)
