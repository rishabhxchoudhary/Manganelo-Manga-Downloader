import requests
from bs4 import BeautifulSoup
import urllib.parse
import requests
import threading
from PIL import Image
import os
import shutil
from fpdf import FPDF
from PyPDF2 import PdfFileMerger

DIR = os.getcwd()

def send_request_image(url: str):
    domain = urllib.parse.urlparse(url).netloc
    header = {
        'Accept': 'image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
        'Host': domain, 'Accept-Language': 'en-ca', 'Referer': 'https://manganelo.com/',
        'Connection': 'keep-alive'
    }
    r = requests.get(url, stream=True, headers=header)
    return r

def page_links(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    div = str(soup.find("div", {"class": "container-chapter-reader"}))
    imgs = BeautifulSoup(div, 'html.parser').find_all('img')
    page_urls = []
    for img in imgs:
        page_urls.append(img['src'])
    return page_urls

def down_all(urls):

    def download(name,url):
        r = send_request_image(url)
        f = open(name,"wb")
        f.write(r.content)
        f.close()
        inputimg = Image.open(name).convert("RGBA")
        image = Image.new("RGB", inputimg.size, "WHITE")
        image.paste(inputimg, (0, 0), inputimg)
        os.remove(name)
        image.save(name)

    threads = []
    for i in range(len(urls)):
        t=threading.Thread(target=download,args=[f'{i+1}.jpg',urls[i]])
        threads.append(t)
        t.start()
    for i in threads:
        i.join()

def chapter_links(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    chapters = soup.find_all("a", {"class": "chapter-name text-nowrap"})
    links = dict()
    for chapter in chapters:
        links[ chapter.text ] = chapter['href']
    return links

def download_manga(name,url):
    print("DOWNLOADING ",name.upper())
    pages = page_links(url)
    num = len(pages)
    print("Number of pages : ",num)

    print("Making Folder.....",end="")
    path = os.path.join(DIR,name)
    try:
        os.mkdir(path)
    except:
        pass

    os.chdir(path)
    down_all(pages)
    imgs = [str(i+1)+".jpg" for i in range(num)]
    pdfs = [str(i+1)+".pdf" for i in range(num)]
    i=0
    for img in imgs:
        i+=1
        cover = Image.open(img)
        width, height = cover.size
        # convert pixel in mm with 1px=0.264583 mm
        width, height = float(width * 0.264583), float(height * 0.264583)
        pdf = FPDF('P','mm',[width,height])
        pdf.add_page()
        pdf.image(img,0,0,width,height)
        pdf.output(str(i)+".pdf", "F")
        os.remove(img)
    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(name+'.pdf')
    merger.close()
    os.rename(os.path.join(path,name+".pdf"), os.path.join(DIR,name+".pdf"))
    shutil.rmtree(path)
    print("Done")

def main():
    URL = input("Enter Manganelo URL : ")
    chapters = chapter_links(URL)
    x = dict(reversed(list(chapters.items())))
    # for i in chapters:
    for i in x:
        print(i)
        y = input("Download ? (y/n) : ")
        if y.lower() == "y":
            download_manga(i,x[i])
            break
main()
