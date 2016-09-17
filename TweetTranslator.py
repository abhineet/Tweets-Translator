from twython import Twython
from langdetect import detect
import requests
import urllib
import json

TWITTER_APP_KEY = 'XXXXXXXXX' #Your Twitter App Key
TWITTER_APP_KEY_SECRET =  'XXXXXXXXXXX' #Your Twitter App Key Secret
TWITTER_ACCESS_TOKEN =   'XXXXXXXXXX' #Your Twitter Access Token
TWITTER_ACCESS_TOKEN_SECRET =  'XXXXXXXXXXXXX' #Your Twitter Access Token Secret

twitter_screen_name='XXXXXX' # Your twitter screen name here 

t = Twython(app_key=TWITTER_APP_KEY, 
    app_secret=TWITTER_APP_KEY_SECRET, 
    oauth_token=TWITTER_ACCESS_TOKEN, 
    oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
try:
    #Get first 10 tweets from user.
    #tweets = t.get_user_timeline(screen_name=twitter_screen_name, count=10 ,lang='en')
    tweets = t.get_user_timeline(screen_name=twitter_screen_name, count=10)
except Exception,e:
  print ('Error while fetching the tweet' + str(e))
  
args = {
      'client_id':'YYYYYYYYYYY',#your client id here 
      'client_secret':'YYYYYYYY',#your azure secret here
      'scope': 'http://api.microsofttranslator.com',
      'grant_type': 'client_credentials'
    	}
oauth_url = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'

oauth_junk = json.loads(requests.post(oauth_url,data=urllib.urlencode(args)).content)

for tweet in tweets:
  try:
    #Check the lang , if its non-english then only call Bing Translation Api.
    language_code = detect(tweet['text'].encode('ascii','ignore'))
    tweet_date = tweet['created_at']
    #print(language_code)
    if (language_code != 'en'):
      translation_args = {
      'text': tweet['text'].encode('ascii','ignore'),
      'to': 'en',
      'from': language_code, # 'from' is optionl paramter. 
      }
      headers={'Authorization': 'Bearer '+ oauth_junk['access_token']}
      translation_url = 'http://api.microsofttranslator.com/V2/Ajax.svc/Translate?'
      translation_result = requests.get(translation_url+urllib.urlencode(translation_args),headers=headers)
      print (translation_result.content , tweet_date)
    else:
      print (tweet['text'] , tweet_date)
  except Exception,e:
    print ('Something Went Wrong' + str(e))
