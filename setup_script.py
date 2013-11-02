#!/usr/bin/python

import urllib
import json
import sys
import ConfigParser

"""
Sets up the configuration file for the application.
"""

def check_error(data):
    if data.get('error') != None:
        reason = ','.join(i['reason'] for i in data['error']['errors'])
        print '[Error] Reason: %s' % reason
        raw_input('Press any key to exit.')
        sys.exit(0)

USERNAME = ''
PLAYLIST = ''
API_KEY = ''
CHANNEL_ID = ''
PLAYLIST_ID = ''
CONFIG_FILENAME = 'VideoGallery.cfg'

searchUrl = 'https://www.googleapis.com/youtube/v3/search'
channelUrl = 'https://www.googleapis.com/youtube/v3/channels'
playlistUrl = 'https://www.googleapis.com/youtube/v3/playlists'
playlistItemsUrl = 'https://www.googleapis.com/youtube/v3/playlistItems'

# get variables from user first
if USERNAME == '':
    USERNAME = raw_input('Enter your YouTube username: ')
if PLAYLIST == '':
    PLAYLIST = raw_input('Enter the playlist you want to use: ')
if API_KEY == '':
    API_KEY = raw_input('''Enter your Google API key: ''')
print '---\n'

# get the channel id from username
params = {'q': USERNAME, 'key': API_KEY, 
          'part': 'snippet', 'type': 'channel'}
url = '%s?%s' % (searchUrl, urllib.urlencode(params))
response = urllib.urlopen(url).read()

data = json.loads(response)
check_error(data)

for i in data['items']:
    if i['snippet']['channelTitle'].lower() == USERNAME.lower():
        CHANNEL_ID = i['snippet']['channelId']
        print 'Channel id initialized: %s' % CHANNEL_ID
        break
if CHANNEL_ID == '':
    print 'Channel id not found. Please verify that the username is correct.'
    print 'Press any key to exit.'
    raw_input()
    sys.exit(0)


# get playlist id
params = {'key': API_KEY, 
          'part': 'snippet', 'channelId': CHANNEL_ID}
url = '%s?%s' % (playlistUrl, urllib.urlencode(params))
response = urllib.urlopen(url).read()
data = json.loads(response)

for i in data['items']:
    if i['snippet']['title'].lower() == PLAYLIST.lower():
        PLAYLIST_ID = i['id']
        print 'Playlist id initialized: %s' % PLAYLIST_ID 
        break
if PLAYLIST_ID == '':
    print 'Playlist id not found. Please verify that the playlist is correct.'
    print 'Press any key to exit.'
    raw_input()
    sys.exit(0)

# write ids to file
cfg = ConfigParser.ConfigParser()
f = open(CONFIG_FILENAME, 'w')
cfg.add_section('IDs')
cfg.set('IDs', 'api_key', API_KEY)
cfg.set('IDs', 'channel_id', CHANNEL_ID)
cfg.set('IDs', 'playlist_id', PLAYLIST_ID)
cfg.write(f)
