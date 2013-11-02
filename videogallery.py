from flask import Flask
import ConfigParser
import urllib2
import json

app = Flask(__name__)
app.debug = True



@app.route("/")
def main():
    return "<html><head></head><body><a href='/tf2videos'>go here</a></body></html>"

@app.route("/tf2videos")
def tf2videos():
    videos = get_videos()
    return str(videos)

def get_videos():
    url = 'https://www.googleapis.com/youtube/v3/playlistItems?key=%s&playlistId=%s&maxResults=50&part=snippet' % (apiKey, playlistId)
    res = urllib2.urlopen(url).read()

    youtubePrefix = 'http://www.youtube.com/watch?v='
    videos = [] # items: [title, description, url]
    data = json.loads(res)
    for i in data['items']:
        title = i['snippet']['title']
        desc = i['snippet']['description']
        videoId = i['snippet']['resourceId']['videoId']
        url = youtubePrefix + videoId
        videos.append([title, desc, url])
    return videos

if __name__ == "__main__":
    cfg = ConfigParser.ConfigParser()
    cfg.readfp(open('VideoGallery.cfg'))

    apiKey = cfg.get('IDs', 'api_key')
    playlistId = cfg.get('IDs', 'playlist_id')

    app.run()

