from pymongo import MongoClient
from flask import Flask, jsonify
from random import randint

# 连接数据库
client = MongoClient('127.0.0.1', 27017)
db = client.neteasemusicdata
data = db.data
categoryList = ['华语男歌手', '华语女歌手', '华语组合/乐队', '欧美男歌手',
                '欧美女歌手', '欧美组合/乐队', '日本男歌手', '日本女歌手', '日本组合/乐队']

slider = {
    "code": 0,
    "data": {
        "slider": [{
            "linkUrl": "https://y.qq.com/m/digitalbum/gold/index.html?_video=true&id=2575698&g_f=shoujijiaodian",
            "picUrl": "http://y.gtimg.cn/music/photo_new/T003R720x288M000002dc6Cg1ko17b.jpg"
        },
            {
            "linkUrl": "https://c.y.qq.com/node/m/client/music_headline/index.html?_hidehd=1&_button=2&zid=359642",
            "picUrl": "http://y.gtimg.cn/music/common/upload/t_focus_info_iphone/207288.jpg"
        },
            {
            "linkUrl": "https://y.qq.com/m/digitalbum/gold/index.html?_video=true&id=2326850&g_f=shoujijiaodian",
            "picUrl": "http://y.gtimg.cn/music/photo_new/T003R720x288M00000286pBl1azeXA.jpg"
        },
            {
            "linkUrl": "https://c.y.qq.com/node/m/client/music_headline/index.html?_hidehd=1&_button=2&zid=370645",
            "picUrl": "http://y.gtimg.cn/music/photo_new/T003R720x288M000002bsERj1487M5.jpg"
        },
            {
            "linkUrl": "https://c.y.qq.com/node/m/client/music_headline/index.html?_hidehd=1&_button=2&zid=375078",
            "picUrl": "http://y.gtimg.cn/music/photo_new/T003R720x288M000001AoTo22ycJWH.jpg"
        }
        ]
    }
}

special = {
    "code":0,
    "list":[
        {
            "singer": "Taylor",
            "songname": "I Knew You Were Trouble.",
            "img": "http://p1.music.126.net/Yeg_GixeLycn_ce92D84WQ==/837827860408793.jpg?param=130y130",
            "albumname": "I Knew You Were Trouble.",
            "url": "http://musicres-zhoudailin.oss-cn-beijing.aliyuncs.com/special/Taylor%20Swift%20-%20I%20Knew%20You%20Were%20Trouble.mp3"
        },
        {
            "singer": "Justin",
            "songname": "What Do You Mean",
            "img": "http://p1.music.126.net/SmaGv_bQTYy5_uOmnAz4Mw==/3285340746015046.jpg?param=130y130",
            "albumname": "Purpose",
            "url": "http://musicres-zhoudailin.oss-cn-beijing.aliyuncs.com/special/Justin%20Bieber%20-%20Purpose.mp3"
        },
        {
            "singer": "KOKIA",
            "songname": "夢追人",
            "img": "http://p1.music.126.net/3t5JIxQKohR5gk_cZqjLGw==/2275989069517444.jpg?param=130y130",
            "albumname": "夢追人",
            "url": "http://musicres-zhoudailin.oss-cn-beijing.aliyuncs.com/special/KOKIA%20-%20%E5%A4%A2%E8%BF%BD%E4%BA%BA.mp3"
        },
        {
            "singer": "花たん",
            "songname": "歌に形はないけれど",
            "img": "http://p1.music.126.net/sK2Rsvagw2iHFG6_jTqb3Q==/5752644836589495.jpg?param=130y130",
            "albumname": "Flower",
            "url": "http://musicres-zhoudailin.oss-cn-beijing.aliyuncs.com/special/%E8%8A%B1%E3%81%9F%E3%82%93%20-%20%E6%AD%8C%E3%81%AB%E5%BD%A2%E3%81%AF%E3%81%AA%E3%81%84%E3%81%91%E3%82%8C%E3%81%A9.flac"
        },
        {
            "singer": "周杰伦",
            "songname": "告白气球",
            "img": "http://p1.music.126.net/cUTk0ewrQtYGP2YpPZoUng==/3265549553028224.jpg?param=130y130",
            "albumname": "周杰伦的床边故事",
            "url": "http://musicres-zhoudailin.oss-cn-beijing.aliyuncs.com/special/%E5%91%A8%E6%9D%B0%E4%BC%A6%20-%20%E5%91%8A%E7%99%BD%E6%B0%94%E7%90%83.mp3"
        },
        {
            "singer": "陈奕迅",
            "songname": "落花流水",
            "img": "http://p1.music.126.net/sqczK3-OMzRHWrDgvOF2fg==/80264348833269.jpg?param=130y130",
            "albumname": "Solidays 新曲+精选",
            "url": "http://musicres-zhoudailin.oss-cn-beijing.aliyuncs.com/special/%E9%99%88%E5%A5%95%E8%BF%85%20-%20%E8%90%BD%E8%8A%B1%E6%B5%81%E6%B0%B4.mp3"
        }
    ]
}

# 接口
app = Flask(__name__)

# slider数据获取


@app.route("/api/slider")
def get_slider():
    return jsonify(slider)

# special推荐


@app.route("/api/special")
def get_special():
    return jsonify(special)


# 歌手列表
@app.route("/api/singer/<int:category>")
def singer_category(category):
    singerlist = data.aggregate(
        [
            {"$match": {"category": categoryList[category]}},
            {"$project": {"singer": 1, "singerpic": 1, "id": 1, "_id": 0}}
        ]
    )
    list = []
    for item in singerlist:
        list.append(item)
    return jsonify({"code": 0, "category": "0", "singerList": list})

# 歌手歌曲列表


@app.route("/api/songs/<int:singerid>")
def songs_of_singer(singerid):
    songs = data.aggregate(
        [
            {"$match": {"id": str(singerid).zfill(4)}},
            {"$project": {"song": 1, "_id": 0}}
        ]
    )
    for song in songs:
        return jsonify({"code": 0, "id": str(singerid).zfill(4), "song": song['song']})


if __name__ == '__main__':
    app.run(debug=None)
