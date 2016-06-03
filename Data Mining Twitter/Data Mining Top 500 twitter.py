import tweepy
from tweepy import api

cKey = 'RiUMHjdVtji816MWT3D345ams'
cSecret = 'ss3CwPBi9QpkUb8ZHhOM5aV6yjwKDvTA5keffwVGdj2smgQZ2m'
AccToken = '547147064-IW2wWeYRNjw5yVLXer3dOlTo9eNfvkyLWnN6FeZx'
AccSecret = 'J91L6eW3s4z0MxA0HdZvSjrMBf0Q6LEyw2DjDCUcSFWdC'

auth = tweepy.OAuthHandler(cKey,cSecret)
auth.set_access_token(AccToken,AccSecret)
