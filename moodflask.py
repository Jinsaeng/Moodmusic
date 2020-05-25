from flask import Flask, redirect, render_template, url_for
import output_mood_v2 as output_mood
import os

app = Flask(__name__, static_folder='')
@app.route("/")
def hello():
    return render_template('home_page.html')

@app.route("/smartplay") #includes smartplay
def smartplay():
    os.system("pkill mpg123")
    output_mood.main()
    return render_template('home_page.html')

#playlist stuff
@app.route("/playlist")
def playlist():
    return render_template("playlist.html")

@app.route("/display")
def display():
    curr_song = output_mood.get_song_name()
    mp3_file = output_mood.get_mp3() #this is for the audio addon 
    mood = output_mood.get_curr_mood()
    return render_template('display.html',mood = mood, song = curr_song, src = mp3_file)

@app.route("/change_mood")
def change_mood():
        #restart the smartplaylist? or force a playlist
    return render_template("home_page.html")

#this is good to find out the current playlist playing
@app.route("/mood", methods=["GET"])
def mood():
    mood = output_mood.get_curr_mood()
    direc = '/home/pi/app/'+ mood + '/'
    lines = os.listdir(direc)
    file =  mood + ".html"
    return render_template(file, playlist = lines)

@app.route("/upbeat", methods=["GET"])
def upbeat():
    #directory = "~/moodmusic/mellow.txt" #txt file with all the songs
    lines = os.listdir('/home/pi/app/upbeat')
    return render_template("upbeat.html", playlist = lines)
    
@app.route("/sad")
def sad():
    #directory = "~/moodmusic/mellow.txt" #txt file with all the songs
    lines = os.listdir('/home/pi/app/sad/')
    return render_template("sad.html", playlist = lines)

@app.route("/relax")
def mellow():
    #directory = "~/moodmusic/mellow.txt" #txt file with all the songs
    lines = os.listdir('/home/pi//app/relax/')
    return render_template("relax.html", playlist = lines)

@app.route("/fun")
def fun():
    #directory = "~/moodmusic/mellow.txt" #txt file with all the songs
    lines = os.listdir('/home/pi/app/happy/')
    return render_template("happy.html", playlist = lines)

#/endof playlist stuff
@app.route("/settings")
def settings():
        #pass a list of the thresholds
        #parse the list in the html and show to user
    mood = output_mood.current_mood
    threshold_dict = output_mood.read_mood_from_file("config.txt")
    for key in threshold_dict:
        print(key, mood)
        if int(key) == mood:
            threshold_lst = threshold_dict.get(key)
            return render_template("settings.html", mood_setting = threshold_lst)
#the list goes (accel min-max, light min-max, tempint min-max, tempext min-max)

@app.route("/add_music")
def add_music():
    return render_template("add_music.html")



if __name__ =="__main__":
    flag = False
    if flag:
        output_mood.main()
    app.run(host='172.20.10.3', port=8989, debug=True, threaded=True)
