from flask import Flask, render_template, request
import templatemaker_web as tmw
import json

app = Flask(__name__)

@app.route("/")
def index () -> str:
    return render_template("index.html")


@app.route("/workbench", methods=["POST"])
def workbench () -> str:
    schedule = str(request.form["scheduleURL"])
    tmw.checker(schedule)
    with open("./data/schedule.json") as f:
        dict_data = json.load(f)
    return render_template("workbench.html", dict_data=dict_data)


@app.route("/result", methods=["POST"])
def result () -> str:
    gametitle = str(request.form["gametitle"])
    tweettype = request.form["tweettype"]
    hashtag = str(request.form["hashtag"])
    streamingURL = str(request.form["streamingURL"])
    fintime = str(request.form["cleartime"])

    content = tmw.output(gametitle,tweettype,hashtag,streamingURL,fintime)
    return render_template("result.html", result=content)

@app.route("/textfix", methods=["POST"])
def textfix () -> str:
    result = str(request.form["result"])
    text = str(request.form["com_text"])
    introtext = tmw.intro_fix(text)
    print(introtext)
    return render_template("result.html", result=result, fixtext=introtext)

if __name__ == "__main__" :
    app.run(debug=True)