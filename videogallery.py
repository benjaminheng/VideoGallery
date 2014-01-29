from flask import Flask, render_template
import ConfigParser
import urllib2
import json
import locale

app = Flask(__name__, static_folder='static', static_url_path='')
app.debug = True



@app.route("/tf2videos")
def tf2videos():
    videos = get_videos()
    return render_template('tf2videos.html', videos=videos)

def word_truncate(content, length=300, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix

def get_videos():
    url = 'https://www.googleapis.com/youtube/v3/playlistItems?key=%s&playlistId=%s&maxResults=50&part=snippet' % (apiKey, playlistId)
    res = urllib2.urlopen(url).read()

    youtubePrefix = 'http://www.youtube.com/watch?v='
    videos = [] 
    data = json.loads(res)
    for i in data['items']:
        tmp = {}
        tmp['title'] = i['snippet']['title']
        tmp['desc'] = word_truncate(i['snippet']['description'])
        tmp['id'] = i['snippet']['resourceId']['videoId']
        videos.append(tmp)

    # get info of videos
    videoIds = [i['id'] for i in videos]
    url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics,contentDetails&id=%s&key=%s' % (','.join(videoIds), apiKey)
    res = urllib2.urlopen(url).read()
    data = json.loads(res)

    
    for video in videos:
        for i in data['items']:
            if i['id'] == video['id']:
                tmpDuration = i['contentDetails']['duration'] 
                #format: PT1M30S for a 1:30 video, PT30S for a 0:30 video
                # parse duration without regex
                tmpDuration = tmpDuration.strip('PT').strip('S')
                duration = ''
                if 'M' in tmpDuration: 
                    tmp = tmpDuration.split('M')
                    duration = '%s:%s' % (tmp[0].zfill(2), tmp[1].zfill(2))
                else:
                    duration = '00:%s' % tmpDuration.zfill(2)

                video['duration'] = duration
                video['views'] = locale.format('%d', int(i['statistics']['viewCount']), grouping=True)
                video['likes'] = i['statistics']['likeCount']
                video['dislikes'] = i['statistics']['dislikeCount']
                break

    return videos

cfg = ConfigParser.ConfigParser()
cfg.readfp(open('VideoGallery.cfg'))

apiKey = cfg.get('IDs', 'api_key')
playlistId = cfg.get('IDs', 'playlist_id')

locale.setlocale(locale.LC_ALL, '')

if __name__ == "__main__":
    app.run()

