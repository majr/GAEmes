from google.appengine.ext import ndb

dbname = 'gamesdb'

def db_key():
    return ndb.Key('dbname', dbname)
    
def delete_game(key_url):
    ndb.Key(urlsafe=key_url).delete()

def return_key(key_url):
    return ndb.Key(urlsafe=key_url)

def query_game(key_url):
    return ndb.Key(urlsafe=key_url).get()

# NDB Model for a Game
class Game(ndb.Model):
    name = ndb.StringProperty()
    minplayers = ndb.IntegerProperty()
    maxplayers = ndb.IntegerProperty()
    mintime = ndb.IntegerProperty()
    maxtime = ndb.IntegerProperty()
    bgg_id = ndb.IntegerProperty()
    rating = ndb.FloatProperty()
    date = ndb.DateProperty(auto_now_add=True)

game_query = Game.query(ancestor=db_key()).order(Game.name)
