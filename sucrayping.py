from bs4 import BeautifulSoup
import pandas as pd
from pandas import Series, DataFrame
import re
import datetime

def scrayping():

    name = [] #マンション名
    address = [] #住所
    location = []#最寄駅
    dummy =[]#駅変数
    age = [] #築年数
    floor = [] #階
    rent = [] #賃料
    area = [] #専有面積
    detail_url = [] #詳細URL

    soup = BeautifulSoup(open('./html_file/room_file{}.html'.format(1)), 'lxml')
    body = soup.find('body')
    pages = body.find_all('div', {'class':'pagination pagination_set-nav'})
    pages_text = str(pages)
    pages_split = pages_text.split('</a></li>\n</ol>')
    pages_split_1 = pages_split[0]
    pages_split_2 = pages_split_1[-3:]
    pages_split_3 = pages_split_2.replace('>', '')
    max_page = int(pages_split_3)
    bukken_num = 0

    #htmlファイルを読み込み
    for k in range(1, max_page + 1):
        url_page = './html_file/room_file{}.html'.format(k)
        soup = BeautifulSoup(open(url_page), 'lxml')
        body = soup.find('body').text
        bukken_list = soup.find('div',{'id':'js-bukkenList'})

        #1ページあたりの物件個数を計算、または追加
        bukken_num += body.count('詳細を見る')

        #マンション名、住所、立地（最寄駅/徒歩~分）、築年数、建物高さが入っているcassetteitemを全て抜き出し
        cassetteitems = bukken_list.find_all('div', {'class':'cassetteitem'})

        #各cassetteitemsに対し、以下の動作をループ
        for i in range(len(cassetteitems)):
            tbodies = cassetteitems[i].find_all('tbody')
            #マンション名
            name_m = cassetteitems[i].find_all("div",{'class':'cassetteitem_content-title'})
            name_m = str(name_m)
            name_rep = name_m.replace('[<div class="cassetteitem_content-title">', '')
            name_rep_2 = name_rep.replace('</div>]', '')

            #住所
            address_1 = cassetteitems[i].find_all("li",{'class':'cassetteitem_detail-col1'})
            address_1 = str(address_1)
            address_rep_1 = address_1.replace('[<li class="cassetteitem_detail-col1">', '')
            address_rep_2 = address_rep_1.replace('</li>]', '')

            #部屋数だけ、マンション名と住所を繰り返しリストに格納（部屋情報と数を合致させるため）
            for y in range(len(tbodies)):
                name.append(name_rep_2)
                address.append(address_rep_2)

            #立地は特定の駅名だけ集計
            #分析に使う指標として、ダミー変数を設定

            location_box = cassetteitems[i].find_all('li', {'class':'cassetteitem_detail-col2'})
            location_box = str(location_box)
            if '大和駅' in location_box:
                loc_text = '大和駅'
                text_mark = 0
            elif '中央林間駅' in location_box:
                loc_text = '中央林間駅'
                text_mark = 0
            elif '本厚木駅' in location_box:
                loc_text = '本厚木駅'
                text_mark = 1
            for y in range(len(tbodies)):
                location.append(loc_text)
                dummy.append(text_mark)

        #各cassetteitemsに対し、以下の動作をループ
        #先ほどと同じ文だが、これがないと下記データがうまく合わない

        for i in range(len(cassetteitems)):

            #各建物から売りに出ている部屋数を取得

            tbodies = cassetteitems[i].find_all('tbody')

            #築年数と建物高さ

            col3 = cassetteitems[i].find_all('li', {'class':'cassetteitem_detail-col3'})

            for x in col3:
                cols = x.find_all('div')
                for i in range(len(cols)):
                    text = cols[i].find(text=True)
                    for y in range (len(tbodies)):
                        if i == 0:
                            if text == '新築':
                                text = text.replace('新築', '0')
                            else: 
                                text = text.strip('築')
                                text = text.strip('年')
                            age.append(text)


        #賃料、専有面積、詳細URL

        tables = bukken_list.find_all('table')

        rows = []
        for i in range(len(tables)):
            rows.append(tables[i].find_all('tr'))

        #各部屋に対して、tableに入っているtext情報を取得し、data_listに格納
        data_list = []

        #階
        for row in rows:       
            for tr in row:
                cols = tr.find_all('td')
                if len(cols) != 0:
                    floor0 = cols[2].text
                    floor0 = re.sub('[\r\n\t]', '', floor0)
                    if floor0 == '-':
                        floor_main = '1'
                    else:
                        split_fl = floor0.split('-')
                        floor_main = floor0[0].strip('階')

                    #賃料

                    rent_cell = cols[3].find('ul').find_all('li')
                    rent_main = rent_cell[0].find('span').text
                    rent_main = rent_main.replace('万円', '')
                    rent_main = float(rent_main) * 10000
                    rent_main = int(rent_main)

                     #専有面積

                    floor_cell = cols[5].find('ul').find_all('li')
                    area_main= floor_cell[1].find('span').text
                    area_main = area_main.replace('m2', '')

                     #詳細URL

                    detail_url_main = cols[8].find('a')['href']
                    detail_url_main = 'https://suumo.jp' + detail_url_main

                    text = [floor_main, rent_main, area_main, detail_url_main]
                    data_list.append(text)

        #data_listに格納 
        for row in data_list:
            floor.append(row[0])
            rent.append(row[1])
            area.append(row[2])
            detail_url.append(row[3]) 

        #現場でのページ数、掲載されていた物件数
        if k % 10 == 0:
            print(str(k) + 'ページ目完了')
            print('現在までの掲載物件数:' + str(bukken_num))
        elif k == max_page :
            print(str(k) + 'ページ目完了')
            print('掲載物件総数:' + str(bukken_num))

    #各リストをシリーズ化
    name = Series(name)
    address = Series(address)
    location = Series(location)
    dummy = Series(dummy)
    age = Series(age)
    floor = Series(floor)
    rent = Series(rent)
    area = Series(area)
    detail_url = Series(detail_url)

    #各シリーズをデータフレーム化
    suumo_df = pd.concat([name, address, location, dummy, age, floor, rent, area, detail_url], axis=1)

    #カラム名
    suumo_df.columns=['マンション名', '住所', '立地', '立地変数', '築年数', '階', '賃料', '専有面積', '詳細url']

    #csvファイルとして保存

    with open('data_frame.csv', mode = 'w', encoding = 'shift-jis', errors='ignore')as f:
        suumo_df.to_csv(f)

if __name__ == '__main__':
    date_now = datetime.datetime.now()
    print('スクレイピング開始:', date_now)
    scrayping()
    df = pd.read_csv('data_frame.csv', encoding = 'shift-jis')
    date_now = datetime.datetime.now()   
    print('スクレイピング完了:', date_now)
    print('検収された物件数:' + str(len(df)))         