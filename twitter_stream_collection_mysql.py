#!/usr/bin/env python

import os,sys,re
from dateutil import parser
import json
import tweepy
import MySQLdb
from helper_functions import _get_config, _logger

parser          = _get_config()
CONSUMER_KEY    = parser.get('Keys', 'consumer_key')
CONSUMER_SERECT = parser.get('Keys', 'consumer_serect')
ACCESS_TOKEN    = parser.get('Keys', 'access_token')
ACCESS_SERECT   = parser.get('Keys', 'access_secret')
SOUTH           = parser.getfloat('Area', 'south')
WEST            = parser.getfloat('Area', 'west')
NORTH           = parser.getfloat('Area', 'north')
EAST            = parser.getfloat('Area', 'east')
HOST            = "localhost"                 # Use "localhost" to store data into local compuetr
USER            = "root"                      # Use "root" if you connect to mysql as superuser root
PASSWD          = "abc123488526"              # Use your root password
DATABASE        = "twitter"                   # In our example it's "twitter"
LOCATIONS       = [WEST, SOUTH, EAST, NORTH]  # the coordinates of the bounding area

def mysql_store(created_at, text, id_str, user_id, user_name, lat, lon, lang):
    db=MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8")
    cursor = db.cursor()
    insert_query = "INSERT INTO twitter_stream_collect (created_at, text, id_str, user_id, user_name, lat, lon, lang) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (created_at, text, id_str, user_id, user_name, lat, lon, lang))
    db.commit()
    cursor.close()
    db.close()
    return

class MyStreamListener(tweepy.StreamListener):
    '''
    This class inherits from tweepy.StreamListener to connect to Twitter Streaming API.
    '''
    def on_connect(self):
        print '......Connected to Twitter Streaming API...... \n'

    def on_data(self, raw_data):
        try:
            data = json.loads(raw_data)                      #decode the json object from twitter
            if data['coordinates'] or data['geo']:           #collect geo-tagged tweet
                created_at = parser.parse(data['created_at'],ignoretz=True)          #tweet posted at UTC time
                text = data['text']
                id_str = data['id_str']
                user_id = data['user']['id_str']
                user_name = data['user']['screen_name']
                lat = str(data['coordinates']['coordinates'][1])
                lon = str(data['coordinates']['coordinates'][0])
                lang = data['user']['lang']
                if float(lat) > SOUTH and float(lat) < NORTH and float(lon) > WEST and float(lon) < EAST:
                    print '@%s' % user_name
                    print 'Tweeted at %s UTC' % created_at
                    print text
                    print 'Lat: %s' % lat
                    print 'Lon: %s \n' % lon
                    mysql_store(created_at, text, id_str, user_id, user_name, lat, lon, lang)
        except Exception as e:
            print e

    def on_error(self, status_code):
        if status_code == 420:         #returning False in on_data disconnects the stream
            return False
        else:                          #continue listening if other errors occur
            print 'An Error has occurred: ' + repr(status_code)
            return True

if __name__ == '__main__':
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SERECT)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SERECT)
    api = tweepy.API(wait_on_rate_limit_notify=True)
    listener = MyStreamListener(api=api)
    streamer = tweepy.Stream(auth=auth, listener=listener)
    print '......Collecting geo-tagged tweets......'
    streamer.filter(locations=LOCATIONS)
