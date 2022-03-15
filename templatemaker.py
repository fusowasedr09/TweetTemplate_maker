import tkinter as tk
from tkinter import ttk
import requests, json
from bs4 import BeautifulSoup

# 設定ファイルをロードする
path = "TBset.json"
f = open(path,"r")
setting_data = json.load(f)
f.close()

defaultSchedule = setting_data["scheduleURL"]
defaulttag = setting_data["hashtag"]
defaultURL = setting_data["streamURL"]

dic = {}
bookmark = 0

# テンプレート出力
def output():
    ## リストボックスの値を取得して辞書を探す
    n = listbox.curselection()
    selectValue = listbox.get(n)
    for i in range(len(dic)):
        search = selectValue in dic[i].values()
        if search == True:
            bookmark = i
            break
        else:
            pass

    ## テキストボックスの処理
    TextBox1.delete("1.0", tk.END)
    TextBox2.delete("1.0", tk.END)
    hashtag = EditBox2.get()
    streamURL = EditBox3.get()
    cleartime = EditBox4.get()

    ## 複数人対応処理：lengthが変化しないのでカンマの置き換えで対応
    runrep = dic[bookmark]["走者"].replace(",","さん,")
    commentrep = dic[bookmark]["解説者"].replace(",","さん,")
    ##ラジオボタンの値を取得してテンプレートを変更する
    radio_num = Radio_value.get()
    if radio_num == 0:
        if dic[bookmark]["解説者"] == "":
            content = "次のゲームは「" + dic[bookmark]["ゲームタイトル（日本語用）"] + "」\nカテゴリーは「"+ dic[bookmark]["カテゴリ"] + "」\n走者は" + runrep + "さん\n" +"\n" + hashtag + "\n\n配信チャンネルはこちら\n" + streamURL
        else:
            content = "次のゲームは「" + dic[bookmark]["ゲームタイトル（日本語用）"] + "」\nカテゴリーは「"+ dic[bookmark]["カテゴリ"] + "」\n走者は" + runrep + "さん\n日本語解説は"+ commentrep +"さんです！\n\n" + hashtag + "\n\n配信チャンネルはこちら\n" + streamURL
    elif radio_num == 1:
        content = "現在進行中のゲームは「" + dic[bookmark]["ゲームタイトル（日本語用）"] + "」\n\n"+ hashtag + "\n\n配信チャンネルはこちら\n" + streamURL
    else:
        if cleartime == "":
            TextBox2.insert("1.0","警告:クリアタイムが記入されていません！\nクリアタイムを入力してからもう一度出力してください")
            return
        else:
            if dic[bookmark]["解説者"] == "":
                content = "「" + dic[bookmark]["ゲームタイトル（日本語用）"] + "」\nカテゴリー「"+ dic[bookmark]["カテゴリ"] + "」\nクリアタイムは"+ cleartime + "でした！\n" +"\n" + hashtag + "\n\n配信チャンネルはこちら\n" + streamURL
            else:
                content = "「" + dic[bookmark]["ゲームタイトル（日本語用）"] + "」\nカテゴリー「"+ dic[bookmark]["カテゴリ"] + "」\nクリアタイムは"+ cleartime + "でした！\n" +"解説の" + commentrep + "さんありがとうございました！\n" + hashtag + "\n\n配信チャンネルはこちら\n" + streamURL
    

    ## bidwarがあったら追加情報欄に記載する
    if dic[bookmark]["bidwar"] == "":
        pass
    else:
        content2 = "※「" + dic[bookmark]["ゲームタイトル（日本語用）"] + "」にはBidwarが設定されています。"
        TextBox2.insert(tk.END, content2)

    TextBox1.insert(tk.END, content)
    EditBox4.delete(0,tk.END)
    setting_data["hashtag"] = hashtag
    setting_data["streamURL"] =streamURL
    with open(path,"w") as f:
        f.write(json.dumps(setting_data, indent=4))



def checker():
    url = EditBox1.get()
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
    
    listbox.delete(0,tk.END)
    for i in range(len(mat)):
        listbox.insert(tk.END, dic[i]["ゲームタイトル（日本語用）"])
    
    setting_data["scheduleURL"] = url
    with open(path, "w")as f:
        f.write(json.dumps(setting_data, indent=4))

def intro_fix():
    text = TextBox3.get("1.0",tk.END)
    t = text.strip()
    t = t.replace("\"", "")
    t = t.replace("　　　,","")
    t = t.replace("　　","　")
    t = t.replace("　","\n")
    t = t.replace("1人目：", "\n") 
    t = t.replace("2人目：","\n")
    TextBox3.delete("1.0",tk.END)
    TextBox3.insert(tk.END, t)




# GUIの構成
root = tk.Tk()
root.geometry("1200x500")

list_value=tk.StringVar()
list_value.set([])
Radio_value = tk.IntVar()
Radio_value.set(0)

## 公開スケジュール設定用のGUI作成
label1 = tk.Label(root,text="公開スケジュールURL：")
label1.place(x = 20, y = 20)
EditBox1 = tk.Entry(width = 90)
EditBox1.insert(tk.END, defaultSchedule)
EditBox1.place(x = 140, y = 20)
Button1 = tk.Button(text=u"検索", command=checker)
Button1.place(x = 690, y = 20)

## 公開スケジュールゲーム選択ボックスの配置
frame_gs =tk.LabelFrame(root,text="ゲームタイトル一覧")
frame_gs.place(x=20, y=90)
scroll1 = tk.Scrollbar(frame_gs)
scroll1.pack(side=tk.RIGHT, fill="y")
listbox = tk.Listbox(frame_gs, width = 50, height = 10, listvariable=list_value, selectmode="single", yscrollcommand=scroll1.set)
listbox.pack()
scroll1["command"]=listbox.yview

## 入力用テキストボックスの配置
label3 =tk.Label(root,text="テンプレート")
label3.place(x = 430, y = 90)
TextBox1 = tk.Text(width = 50, height = 20)
TextBox1.place(x = 430, y = 110)
#Button2 = tk.Button(text=u"ツイート文出力", width = 50, command=output)
#Button2.place(x = 430, y = 250)

## ハッシュタグ用ボックスの配置
label4 = tk.Label(root,text="ハッシュタグ：")
label4.place(x = 110, y = 290)
EditBox2 = tk.Entry(width = 30)
EditBox2.insert(tk.END, defaulttag)
EditBox2.place(x = 180, y = 290)

## 配信URL用ボックスの配置
label5 = tk.Label(root,text="配信URL：")
label5.place(x = 118, y = 320)
EditBox3 = tk.Entry(width = 40)
EditBox3.insert(tk.END,defaultURL)
EditBox3.place(x = 180, y = 320)

## クリアタイム入力用ボックスの配置
label6 = tk.Label(root,text="クリアタイム：")
label6.place(x = 110, y = 350)
EditBox4 = tk.Entry(width = 30)
EditBox4.place(x = 180, y = 350)
label7 = tk.Label(root,text="※クリアタイムはゲーム終了ツイートにのみ反映されます")
label7.place(x = 110, y = 370)

## ステータスを出すためのテキストボックスの配置
label6 =tk.Label(root,text="情報")
label6.place(x = 430, y = 400)
TextBox2 = tk.Text(width = 50, height = 3)
TextBox2.place(x = 430, y = 420)

## ツイートの種類を選択するラジオボタンの配置
frame_ts =tk.LabelFrame(root,text = "ツイートの種類",relief="groove", bd= 2)
frame_ts.place(x = 20, y = 280)
rdo1 = tk.Radiobutton(frame_ts, variable=Radio_value,value=0, text="ゲーム開始")
rdo1.pack(anchor=tk.W)
rdo2 = tk.Radiobutton(frame_ts, variable=Radio_value,value=1, text="ゲーム中")
rdo2.pack(anchor=tk.W,pady=3)
rdo3 = tk.Radiobutton(frame_ts, variable=Radio_value,value=2, text="ゲーム終了")
rdo3.pack(anchor=tk.W,pady=3)

## テンプレート生成ボタン
Button3 = tk.Button(root,text=u"テンプレート出力", width = 50, command=output)
Button3.place(x = 20, y = 400)

## おまけ
frame_omake = tk.LabelFrame(root,text="おまけ：解説者紹介用のやつをいい感じにしてくれるやつ", relief="groove", bd = 2)
frame_omake.place(x = 800, y = 100)
TextBox3 = tk.Text(frame_omake,width = 50, height=10)
TextBox3.pack()
Button4 = tk.Button(frame_omake,text=u"いい感じにする", command=intro_fix)
Button4.pack()

## 使い方ガイド
frame_htu = tk.LabelFrame(root,text="このアプリの使い方", relief = "groove", bd = 2)
frame_htu.place(x = 800, y = 350)
label_htu1 = tk.Label(frame_htu, text="1.「公開スケジュールURL」のテキストボックスにpublicのスケジュールURLを入力")
label_htu1.pack(anchor=tk.W)
label_htu2 = tk.Label(frame_htu, text="2.「検索」ボタンをクリック")
label_htu2.pack(anchor=tk.W)
label_htu3 = tk.Label(frame_htu, text="3.ゲームタイトル一覧からツイートするゲームを選択")
label_htu3.pack(anchor=tk.W)
label_htu4 = tk.Label(frame_htu, text="4.ツイートの種別を選択、ハッシュタグや配信URLを入力\n（ゲーム終了ツイートの場合はクリアタイムも埋める）")
label_htu4.pack(anchor=tk.W)
label_htu5 = tk.Label(frame_htu, text="5.「テンプレート出力」のボタンをクリックするとテンプレート欄に文章が出力される")
label_htu5.pack(anchor=tk.W)
label_htu6 = tk.Label(frame_omake, text="使い方:\nスプシの「解説者紹介ツイート」をコピーしてテキストボックスに貼り付け。\nその後「いい感じにする」を押すといい感じになります（たぶん）")
label_htu6.pack(anchor=tk.W)
label_htu6.option_add("*jsutify",("left"))
root.mainloop()
