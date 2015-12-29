import webapp2
import jinja2
import query as q

from urllib import urlopen
from os import path
from google.appengine.ext import ndb
from time import sleep
from xml.dom.minidom import parse

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

admin_template = env.get_template('templates/admin.html')
import_template = env.get_template('templates/import.html')
query_template = env.get_template('templates/query.html')

class Admin(webapp2.RequestHandler):
    # Display admin page with list of games currently in the datastore
    def get(self):
        games = q.game_query.fetch()
        self.response.write(admin_template.render(games=games))
        
    # Add new entry (game) to the datastore and refresh the page
    def post(self):
        entry = q.Game(parent=q.db_key())
        entry.name = self.request.get('name')
        entry.minplayers = int(self.request.get('minplayers'))
        entry.maxplayers = int(self.request.get('maxplayers'))
        entry.mintime = int(self.request.get('mintime'))
        entry.maxtime = int(self.request.get('maxtime'))
        entry.rating = float(self.request.get('rating'))
        entry.put()
        self.redirect('/admin')

# Handler for modifying game entries
class ModGame(webapp2.RequestHandler):
    # Write page with values of datastore entry to be modified
    def get(self):
        key_url = self.request.get('key')
        game = q.query_game(key_url)
        self.response.write(query_template.render(game=game))

    # Modify game entity
    def post(self):
        entry = q.Game(parent=q.db_key())
        entry.name = self.request.get('name')
        entry.minplayers = int(self.request.get('minplayers'))
        entry.maxplayers = int(self.request.get('maxplayers'))
        entry.mintime = int(self.request.get('mintime'))
        entry.maxtime = int(self.request.get('maxtime'))
        entry.rating = float(self.request.get('rating'))
        if (self.request.get('bgg_id')):
            entry.bgg_id = int(self.request.get('bgg_id'))
        entry.key = q.return_key(self.request.get('key'))
        entry.put()
        self.redirect('/admin')
        
        
# Remove entry (game) from the datastore and refresh page
class DelGame(webapp2.RequestHandler):
    def post(self):
        key_url = self.request.get('key')
        q.delete_game(key_url)
        self.redirect('/admin')

# Import database from BGG using their API
class ImportDB(webapp2.RequestHandler):
    # Write query landing page
    def get(self):
        self.response.write(import_template.render())

    # Query BGG API for a collection of owned games and import into datastore
    def post(self):
        BGGUserName = self.request.get('BGGUserName')
        url = 'http://www.boardgamegeek.com/xmlapi/collection/' + BGGUserName + '?own=1'
        prep = urlopen(url)
        prep.close()
        sleep(10)
        dom = parse(urlopen(url))
        for item in dom.getElementsByTagName("item"):
            entry = q.Game(parent=q.db_key())
            entry.bgg_id = int(item.getAttribute("objectid"))
            for game in item.getElementsByTagName("name"):
                entry.name = game.firstChild.data
            for stats in item.getElementsByTagName("stats"):
                if (stats.getAttribute("minplayers")):
                    entry.minplayers = int(stats.getAttribute("minplayers"))
                if (stats.getAttribute("maxplayers")):
                    entry.maxplayers = int(stats.getAttribute("maxplayers"))
                if (stats.getAttribute("minplaytime")):
                    entry.mintime = int(stats.getAttribute("minplaytime"))
                if (stats.getAttribute("maxplaytime")):
                    entry.maxtime = int(stats.getAttribute("maxplaytime"))
                for rating in stats.getElementsByTagName("rating"):
                    for average in rating.getElementsByTagName("average"):
                        entry.rating = float(average.getAttribute("value"))
                        
            entry.put()
            
        self.redirect('/admin')

app = webapp2.WSGIApplication([
    ('/admin', Admin),
    ('/admin/mod', ModGame),
    ('/admin/del', DelGame),
    ('/admin/import', ImportDB)
])
