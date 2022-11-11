from flask import Flask,render_template,request,url_for,redirect,session,send_file
from pytube import YouTube
from io import BytesIO
app = Flask(__name__,template_folder="website",static_folder="module")
app.config["SECRET_KEY"] = "abdjeownrnoekm3oodjdnnroktrkle"

@app.route("/",methods=["GET","POST"])
def home():
    return render_template("index.html",info="Youtube to mp3")

@app.route("/ytDownload",methods=["GET","POST"])
def ytDownload():
    try:
        if request.method == "POST":
            session["choose"] = request.form.get("choose")
            session["url"] = request.form.get("url")
            if session["choose"] == "ytmp3":
                audio = YouTube(session["url"])
                session["title"] = audio.title
                return render_template("ytmp3.html",info="Youtube to mp3",title=session["title"])

            
            elif session["choose"] == "ytmp4":
                vid = YouTube(session["url"])
                session["vid_title"] = vid.title
                return render_template("ytmp4.html",info="Youtube to mp4",id=vid.video_id,vid=vid)

            else:
                return redirect(url_for("home"))

        return redirect(url_for('home'))

    except:
        return render_template("error.html")


@app.route("/mp3",methods=["GET","POST"])
def mp3():
    if request.method == "POST":
        try:
            audio = YouTube(session["url"]).streams.filter(only_video=True)[4]
            buffer = BytesIO()
            audio.stream_to_buffer(buffer)
            buffer.seek(0)
            return send_file(buffer,as_attachment=True,download_name=session["title"]+".mp3",mimetype="audio/mpeg")

        except:
            return render_template("error.html")

    return redirect(url_for("home"))



@app.route("/mp4",methods=["GET","POST"])
def mp4():
    if request.method == "POST":
        try:
            res = request.form.get("itag")
            vid = YouTube(session["url"]).streams.get_by_itag(itag=res)
            buffer = BytesIO()
            vid.stream_to_buffer(buffer)
            buffer.seek(0)
            title = str(session["vid_title"]+".mp4")
            return send_file(buffer,as_attachment=True,download_name=title,mimetype="video/mp4")
        except:
            return render_template("error.html")


    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
