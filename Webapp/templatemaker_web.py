import tkinter as tk
from tkinter import ttk
import requests, json
from bs4 import BeautifulSoup


# テンプレート出力
def output(gametitle, tweetType, tag, stURL, time):
    ## リストボックスの値を取得して辞書を探す
    with open("./data/schedule.json","r") as f:
        dic = json.load(f)

    bookmark = 0
    for i in range(len(dic)):
        counter = str(i)
        search = str(gametitle) in dic[counter].values()
        if search == True:
            bookmark = counter
            break
        else:
            pass
    print(bookmark)

    hashtag = tag
    streamURL = stURL
    cleartime = time

    ## 複数人対応処理：lengthが変化しないのでカンマの置き換えで対応
    runrep = dic[bookmark]["走者"].replace(",","さん,")
    commentrep = dic[bookmark]["解説者"].replace(",","さん,")
    ## ラジオボタンに対応してテンプレートを変更する
    if tweetType == "1":
        if dic[bookmark]["解説者"] == "":
            content = "次のゲームは「" + dic[bookmark]["ゲームタイトル（日本語用）"] + "」\nカテゴリーは「"+ dic[bookmark]["カテゴリ"] + "」\n走者は" + runrep + "さん\n" +"\n" + hashtag + "\n\n配信チャンネルはこちら\n" + streamURL
        else:
            content = "次のゲームは「" + dic[bookmark]["ゲームタイトル（日本語用）"] + "」\nカテゴリーは「"+ dic[bookmark]["カテゴリ"] + "」\n走者は" + runrep + "さん\n日本語解説は"+ commentrep +"さんです！\n\n" + hashtag + "\n\n配信チャンネルはこちら\n" + streamURL
    elif tweetType == "2":
        content = "現在進行中のゲームは「" + dic[bookmark]["ゲームタイトル（日本語用）"] + "」\n\n"+ hashtag + "\n\n配信チャンネルはこちら\n" + streamURL
    else:
        if time == "":
            content = "警告:クリアタイムが記入されていません！\nもう一度やり直してください"
            return content
        else:
            if dic[bookmark]["解説者"] == "":
                content = "「" + dic[bookmark]["ゲームタイトル（日本語用）"] + "」\nカテゴリー「"+ dic[bookmark]["カテゴリ"] + "」\nクリアタイムは"+ cleartime + "でした！\n" +"\n" + hashtag + "\n\n配信チャンネルはこちら\n" + streamURL
            else:
                content = "「" + dic[bookmark]["ゲームタイトル（日本語用）"] + "」\nカテゴリー「"+ dic[bookmark]["カテゴリ"] + "」\nクリアタイムは"+ cleartime + "でした！\n" +"解説の" + commentrep + "さんありがとうございました！\n" + hashtag + "\n\n配信チャンネルはこちら\n" + streamURL
    
    return content


def checker(url):
    # 公開用スケジュールからデータを取得する
    dic ={}
    html=requests.get(url)
    soup=BeautifulSoup(html.content,"html.parser")
    table = soup.find('table')
    
    mat = []
    trs = table.find_all('tr')

    # ヘッダーの解析
    r = []  # 保存先の行
    tr = trs[0]
    for td in tr.find_all('th'):  # thタグを走査する
        r.append(td.text)

    mat.append(r)

    # ボディの解析
    for tr in trs[1:]:  # 最初の行を飛ばしてfor文で回す
        r = []  # 保存先の行
        for td in tr.find_all('td'):  # tdタグを走査する
            r.append(td.text)
        mat.append(r)

    # 公開用スケジュールのリストを整形
    del mat[0:5]

    # 辞書を作成
    keys = ["Url","時間(JST)","ゲームタイトル（日本語用）","ダミー","カテゴリ","走者","解説者","RTA経験","予定時間","準備時間","機種","Game title","bidwar"]

    for i in range(len(mat)):
        d = dict(zip(keys, mat[i]))
        del d["ダミー"]
        del d["Url"]
        dic[i] = d
    
    with open("./data/schedule.json","w") as f:
        f.write(json.dumps(dic, indent=4))



def intro_fix(text):
    text = text
    t = text.strip()
    t = t.replace("\"", "")
    t = t.replace("　　　,","")
    t = t.replace("　　","　")
    t = t.replace("　","\n")
    t = t.replace("1人目：", "\n") 
    t = t.replace("2人目：","\n")
    return t


