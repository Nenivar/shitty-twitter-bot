import tweepy
import json
import pickle

"""
    read in auth data
"""

auth_data = None
with open('auth.json') as f:
    auth_data = json.load(f)
    f.close()

handle = auth_data['twitter_handle']
cons_key = auth_data['consumer_key']
cons_sec = auth_data['consumer_secret']
acc_tok = auth_data['access_token']
acc_tok_sec = auth_data['access_token_secret']

OPT_IN = '@{}, I would like to opt-in!'.format(handle)
OPT_OUT = '@{}, I would like to opt-out!'.format(handle)

"""
    get opt-in from user
    & opt-out
"""
users = []

# read in existing users
with open('users.txt', 'r') as f:
    for x in f.readlines():
        users.append(x.strip())
    f.close()

def addUserToFile(userId):
    with open('users.txt', 'a') as f:
        f.write('\n{}'.format(userId))
        f.close()

def removeUserFromFile(userId):
    new = []
    with open('users.txt', 'r') as f:
        lines = f.readlines()
        new = list(filter(lambda x: x != userId, users))
        f.close()
    with open('users.txt', 'w') as f:
        f.writelines(new)
        f.close()

def addUser(userId):
    if userId not in users:
        addUserToFile(userId)
        users.append(userId)

def removeUser(userId):
    if userId in users:
        removeUserFromFile(userId)
        users.remove(userId)

"""
    tweepy stuff
"""

auth = tweepy.OAuthHandler(cons_key, cons_sec)
auth.set_access_token(acc_tok, acc_tok_sec)
api = tweepy.API(auth)

user = api.me()
print('Bot running on {}'.format(user.name))

# on any user tweeting @
class StreamAuth(tweepy.StreamListener):
    def on_status(self, status):
        """ if status == OPT_IN:
            print('opt in!') """
        print(status.user['id_str'])

# on user tweeting anything
# add/remove them to users list
class StreamReply(tweepy.StreamListener):
    def on_status(self, status):
        #addUser(status.user.id_str)
        user = status.user.id_str
        if status.text == OPT_IN:
            print('{} opted in!'.format(status.user.name))
            addUser(user)
        elif status.text == OPT_OUT:
            print('{} opted out!'.format(status.user.name))
            removeUser(user)

def startStream():
    sr = StreamReply()
    s2 = tweepy.Stream(auth = api.auth, listener=sr)
    s2.filter(track='nenivar', is_async=True)
    s2.disconnect()

    """sa = StreamAuth()
    s1 = tweepy.Stream(auth = api.auth, listener=sa)
    s1.filter(follow=['2286822205'], is_async=True) """

startStream()