# coding: utf-8
from flask import Flask, render_template, request, redirect, url_for, make_response
from pytube import YouTube
from flask_cors import CORS
import os
import cv2
import glob
import hashlib
import datetime
import requests
import json
import threading
import time

app = Flask(__name__)
CORS(app)

percent = 0

def calc_hash(string):
    hash = hashlib.sha256(string.encode('utf-8')).hexdigest()
    return hash

def getMovieThumbnail(movie_path):
    frame = None
    target = movie_path
    movie = cv2.VideoCapture(target)
    # 最初の1フレームを読み込む
    if movie.isOpened() == True:
        ret, frame = movie.read()
    else:
        ret = False
    #resized_frame = cv2.resize(frame, (320, 180))
    now = datetime.datetime.now()
    hash = calc_hash(str(now))
    filepath = os.path.join('static/img', str(hash) + ".jpg")
    cv2.imwrite(filepath, frame)

def progress_Check(stream = None, chunk = None, file_handle = None, remaining = None):
    #Gets the percentage of the file that has been downloaded.
    global percent
    global file_size
    percent = (100*(file_size-remaining))/file_size
    print ("{:00.0f}% downloaded".format(percent))

def movieDownload(url, download_path):
    global movie_title
    global file_size
    yt = YouTube(url,  on_progress_callback=progress_Check)
    movie_title = yt.title
    video_type = yt.streams.filter(file_extension='mp4', progressive=True).first()
    file_size = video_type.filesize
    video_type.download(download_path)
    print ("Convert Complete")

    # Movie be renamed to hashed name
    movie_search_path = 'static/movie/*.mp4'
    files = []
    files = glob.glob(movie_search_path)
    now_movie_path = files[0]
    new_movie_path = renamedToHash(now_movie_path)
    new_movie_title = os.path.split(new_movie_path)[1]
    
    # Get and Save movie thumbnail
    getMovieThumbnail(new_movie_path)

    # Thumbnail be renamed to hashed name
    #thumbnail_search_path = 'static/img/*.jpg'
    #files = []
    #files = glob.glob(thumbnail_search_path)
    #thumbnail_path = files[0]

    #thumnail_area_html = "<img id='thumbnail' src='" + str(thumbnail_path) + "' width='320' height='180' alt='Movie Thumbnail'/>"
    #download_file_html = "<a href='" + str(new_movie_path) + "' download='" + new_movie_title + ".mp4' >Download to your computer</a>"
    #return render_template('home.html', movie_title = movie_title, thumnail_area_html=thumnail_area_html, download_file_html=download_file_html)

def renamedToHash(file_path):
    dir, title = os.path.split(file_path)
    title, ext = os.path.splitext(title)
    hashed_title = calc_hash(str(title))
    new_path = os.path.join(dir, hashed_title+ext)
    os.rename(file_path, new_path)
    return new_path

@app.route("/", methods=['GET', 'POST'])
def home():
    convert_button = "<button id='convert'>Convert</button>"
    thumnail_area_html = "<h3>Movie Thumbnail</h3>"
    return render_template('home.html', convert_button=convert_button, thumnail_area_html=thumnail_area_html)

@app.route("/convert", methods=['GET', 'POST'])
def convert():
    global movie_title
    if request.method == 'POST':
        # downloadedフォルダにファイルがないことを確認
        # youtubeのURLが正しいことを確認
        
        url = request.form['youtubeUrl']
        t = threading.Thread(target=movieDownload, args=(url, 'static/movie/'))
        t.start()
        
        """
        # Movie be renamed to hashed name
        movie_search_path = 'static/movie/*.mp4'
        files = []
        files = glob.glob(movie_search_path)
        now_movie_path = files[0]
        new_movie_path = renamedToHash(now_movie_path)
        new_movie_title = os.path.split(new_movie_path)[1]
        
        # Get and Save movie thumbnail
        getMovieThumbnail(new_movie_path)

        # Thumbnail be renamed to hashed name
        thumbnail_search_path = 'static/img/*.jpg'
        files = []
        files = glob.glob(thumbnail_search_path)
        thumbnail_path = files[0]

        thumnail_area_html = "<img id='thumbnail' src='" + str(thumbnail_path) + "' width='320' height='180' alt='Movie Thumbnail'/>"
        download_file_html = "<a href='" + str(new_movie_path) + "' download='" + new_movie_title + ".mp4' >Download to your computer</a>"
        return render_template('home.html', movie_title = movie_title,
            thumnail_area_html=thumnail_area_html, download_file_html=download_file_html)
        """
        url_box_text = url
        convert_button = "<button id='convert' disabled>Converting...</button>"
        convert_stop_html = "<button>Convert Stop</button>"
        return render_template('home.html', url_box_text=url_box_text, convert_button=convert_button, convert_stop_html=convert_stop_html)
    else:
        return render_template('home.html')

@app.route("/reset", methods=['GET', 'POST'])
def reset():
    path = 'static/img/*.jpg'
    files = []
    files = glob.glob(path)
    for f in files:
        os.remove(f)

    path = 'static/movie/*.mp4'
    files = []
    files = glob.glob(path)
    for f in files:
        os.remove(f)
    return redirect(url_for('home'))

@app.route("/progress", methods=['GET', 'POST'])
def progress():
    global percent
    percent = int(percent)
    return json.dumps({'percent':percent})

if __name__ == "__main__":
    app.run(threaded=True)