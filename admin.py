import webapp2
import jinja2
import query as q

from os import path
from google.appengine.ext import ndb
from time import sleep

from xml.dom.minidom import parse
from xml.dom import minidom
import urllib

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

admin_template = env.get_template('templates/admin.html')
query_template = env.get_template('templates/import.html')

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
        entry.difficulty = int(self.request.get('difficulty'))
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
        self.response.write(query_template.render())

    # Query BGG API for a collection of owned games and import into datastore
    def post(self):
        BGGUserName = self.request.get('BGGUserName')
        url = 'http://www.boardgamegeek.com/xmlapi/collection/' + BGGUserName + '?own=1'
        dom = minidom.parse(urllib.urlopen(url))
        for item in dom.getElementsByTagName("item"):
            entry = q.Game(parent=q.db_key())
            for game in item.getElementsByTagName("name"):
                entry.name = game.firstChild.data
            for stats in item.getElementsByTagName("stats"):
                entry.minplayers = int(stats.getAttribute("minplayers"))
                entry.maxplayers = int(stats.getAttribute("maxplayers"))
                entry.mintime = int(stats.getAttribute("minplaytime"))
                entry.maxtime = int(stats.getAttribute("maxplaytime"))
            
            entry.put()
            # Sleep because ancestor queries are restricted to one write per second
            sleep(1)
        self.redirect('/admin')

app = webapp2.WSGIApplication([
    ('/admin', Admin),
    ('/admin/del', DelGame),
    ('/admin/import', ImportDB)
])
