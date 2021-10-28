import requests
import time
from bs4 import BeautifulSoup
import os
import datetime

def crawling():
    dirname = './html_file'
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?shkr1=03&shkr3=03&cb=0.0&rn=0245&rn=0255&shkr2=03&mt=9999999&sngz=&ar=030&bs=040&shkr4=03&ct=9999999&ra=014&cn=9999999&ek=024535270&ek=025524340&ek=025540370&mb=0&et=9999999&page={}'
    target_url = url.format(1)
    result = requests.get(target_url)
    soup = BeautifulSoup(result.text, 'lxml')
    
    body = soup.find('body')
    pages = body.find_all("div", {'class':'pagination pagination_set-nav'})
    pages_text = str(pages)
    pages_split = pages_text.split('</a></li>\n</ol>')
    pages_split_1 = pages_split[0]
    pages_split_2 = pages_split_1[-3:]
    pages_split_3 = pages_split_2.replace('>', '')
    max_page = int(pages_split_3)

    print('総ページ数:' + str(max_page))

    time.sleep(3)

    for i in range(1, max_page + 1):
        target_url = url.format(i)
        result = requests.get(target_url, timeout = 9.0)
        time.sleep(3)
        with open('./html_file/room_file{}.html'.format(i), 'w', encoding='utf-8') as f:
            f.write(result.text)
        if i % 10 == 0 or i == max_page:
            print(str(i) + 'ページ目完了')


if __name__ == '__main__':
    date_now = datetime.datetime.now()
    print('クローリング開始:', date_now)
    crawling()
    date_now = datetime.datetime.now()   
    print('クローリング完了:', date_now)