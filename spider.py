#-*- coding: UTF-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re


# 连接mongodb
client = MongoClient('127.0.0.1', 27017)
client.drop_database('neteasemusicdata')
db = client.neteasemusicdata
db_data = db.data

# 获取个最热门歌手的主页链接


def get_singer_url(accessurl):
    singerurls = []
    driver = webdriver.PhantomJS()
    driver.get(accessurl)
    driver.switch_to.frame(driver.find_element_by_name('contentFrame'))
    html = driver.page_source
    obj = BeautifulSoup(html, 'lxml')
    urlists = obj.findAll('a', {'class': 'msk'})
    for urlist in urlists:
        singerurl = 'https://music.163.com/#' + urlist['href']
        singerurls.append(singerurl)
    driver.quit()
    return singerurls


# 对于某个歌手爬取出热门五十首的名字，专辑名，专辑图像和外链地址
def get_singer_data(url):
    # 利用selenium+webdriver解决ajax加载
    # 网易云音乐的部分链接数据放在一个iframe里面
    # 解析完成后转为bs对象
    driver = webdriver.PhantomJS()
    driver.get(url)
    driver.switch_to.frame(driver.find_element_by_name('contentFrame'))
    html = driver.page_source
    obj = BeautifulSoup(html, 'lxml')

    # 利用正则表达式取出歌手名字
    singerpattern = re.compile(r'[^( -)]*')
    singertitle = obj.find(id='artist-name')['title']
    singer_name = singerpattern.match(singertitle).group()

    # 获得歌手的图片
    singer_pic = obj.find('div', {'class': 'btm'}
                          ).find_next_sibling('img')['src']

    # 热门歌曲获取
    songs = []
    idpattern = re.compile(r'\d*$')
    urlists = obj.findAll('tr')
    for urlist in urlists:
        song_name = urlist.b['title']  # 歌曲名字
        album_name = urlist.find(
            'a', href=re.compile(r'/album'))['title']  # 专辑名称
        song_url = urlist.b.parent['href']
        id = idpattern.search(song_url).group()
        out_chain = '//music.163.com/outchain/player?type=2&id=' + id + '&auto=1'  # 歌曲外链地址
        songurl = 'https://music.163.com/#' + song_url
        driver.get(songurl)
        driver.switch_to.frame(driver.find_element_by_name("contentFrame"))
        html = driver.page_source
        song_obj = BeautifulSoup(html, 'lxml')
        album_img = song_obj.find('img', {'class': 'j-img'})['src']  # 歌曲专辑图片
        songs.append(
            {'songname': song_name, 'outerchain': out_chain, 'img': album_img, 'albumname': album_name})
        i = i + 1
    driver.quit()
    return (singer_name, singer_pic, songs)


# 写入数据到mongdodb
singer_urls_head = 12 * ['https://music.163.com/#/discover/artist/cat?id=']
singer_urls_id = ['1001', '1002', '1003', '2001', '2002',
                  '2003', '6001', '6002', '6003', '7001', '7002', '7003']
singer_category = ['华语男歌手', '华语女歌手', '华语组合/乐队', '欧美男歌手',
                   '欧美女歌手', '欧美组合/乐队', '日本男歌手', '日本女歌手', '日本组合/乐队', '韩国男歌手', '韩国女歌手', '韩国组合/乐队']
singer_urls = [''.join(x) for x in zip(singer_urls_head, singer_urls_id)]
conunt = 0  # 计数器援引歌手分类下标
for singer_url in singer_urls:
    singers_url = get_singer_url(singer_url)
    for url in singers_url:
        print(url, '\n')
        (singer_name, singer_pic, songs) = get_singer_data(url)
        db_data.insert(
            {'singer': singer_name, 'category': singer_category[conunt], 'singerpic': singer_pic, 'song': songs})

        print(db_data.inserted_id)
    conunt += 1
