import re
import string
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import multiprocess as mp
class CvSpider:
    def __init__(self,save_folder,keywords):
        self.save_folder=save_folder
        self.keywords=keywords
        self.root_url='http://openaccess.thecvf.com/'
        with open((save_folder / 'title').with_suffix(".md"), 'w') as handler:
            handler.writelines(f"Keywords: {keywords}\n")

    def _pdf(self,url, title):
        with open((self.save_folder / title).with_suffix(".pdf"), 'wb') as handler:
            handler.write(requests.get(url).content)
    def _md(self,url,title):
        with open((self.save_folder / 'title').with_suffix(".md"), 'a') as handler:
            handler.writelines(f"- [{title}]({url})\n")
    def saveonce(self,arg):
        name, year, format=arg
        keywords = sum([[i, i.capitalize()] for i in self.keywords], [])
        savefunc = {'pdf': self._pdf, 'md': self._md}[format]
        def parser(element):
            try:
                url = self.root_url + \
                      re.findall(r"(?<=href=\").+?pdf(?=\">pdf)|(?<=href=\').+?pdf(?=\">pdf)", str(element))[0]
                bibref_strs = re.findall('<div class="bibref">[\s\S]*?</div>', str(element))
                title = re.findall('\ntitle = {[\s\S]*?<br/>', bibref_strs[0], re.I)[0]
                title = re.findall('{[\s\S]*?}', title, re.I)[0][1:-1]
                title = " " + title.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
                for word in keywords:
                    if word in title: title = f"[{word}]" + title
                if title[0] == '[':
                    savefunc(url,  + "[{name}{year}]"+title)
                    return 1
                return 0
            except:
                return 0
        link_list = [str(div) for div in BeautifulSoup(requests.get(f'{self.root_url}{name}{year}.py').content, "html.parser").find_all('dd')]
        num=0
        t=tqdm(link_list,desc=f'{name}-{year}')
        for element in t:
            num+=parser(element)
            t.set_description(f'{name}{year}|Found:{num}')
    def save(self,format):
        conference = [['CVPR', i,format] for i in [x for x in range(2014, 2020)]] + \
                     [['ICCV', i,format] for i in [x for x in range(2013, 2019, 2)]] + \
		     ["ECCV2018"]
        with mp.Pool(len(conference)) as pool:
            pool.imap(self.saveonce, conference)
            pool.close()
            pool.join()

if __name__ == "__main__":
    keywords=['egoc','gaze','first']
    save_folder=Path(__file__).parent








    print(f"Keywords: {keywords}")
    downloader=CvSpider(save_folder,keywords)
    downloader.save('pdf')



