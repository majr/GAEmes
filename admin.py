import webapp2
import jinja2
import query as q

from os import path
from google.appengine.ext import ndb

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

admin_template = env.get_template('admin.html')

# Display admin page with list of games currently in the datastore
class Admin(webapp2.RequestHandler):
    def get(self):
        games = q.game_query.fetch()
        self.response.write(admin_template.render(games=games))

# Add new entry (game) to the datastore and refresh the page
class AddGame(webapp2.RequestHandler):
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

app = webapp2.WSGIApplication([
    ('/admin', Admin),
    ('/admin/add', AddGame),
    ('/admin/del', DelGame),
])