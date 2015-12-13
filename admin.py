import cgi
import urllib
import webapp2
import query as q
from google.appengine.api import users
from google.appengine.ext import ndb

ADMIN_PAGE_HEADER_TEMPLATE = """\
    <form action="/admin/add" method="post">
      <table align="center"s>
        <tr>
          <td>Name</td>
          <td>Min Players</td>
          <td>Max Players</td>
          <td>Min Time</td>
          <td>Max Time</td>
          <td>Difficulty</td>
        </tr>
        <tr>
          <td><input type="text" name="name"></td>
          <td><input type="text" name="minplayers"></td>
          <td><input type="text" name="maxplayers"></td>
          <td><input type="text" name="mintime"></td>
          <td><input type="text" name="maxtime"></td>
          <td><input type="text" name="difficulty"></td>
          <td><input type="submit" value="Add Game"></td>
        </tr>
      </table
    </form>
    <hr>
"""

ADMIN_TABLE_TEMPLATE = """\
    <table border="1" align="center">
    <tr>
    <td>Game</td>
    <td>Min Players</td>
    <td>Max Players</td>
    <td>Difficulty</td>
    <td>Date Added</td>
    </tr>
"""

# Display admin page with list of games currently in the datastore
class Admin(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        self.response.write(ADMIN_PAGE_HEADER_TEMPLATE)
        self.response.write(ADMIN_TABLE_TEMPLATE)

        game_query = q.Game.query(ancestor=q.db_key()).order(-q.Game.date)
        games = game_query.fetch()

        for item in games:
            self.response.write('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' %
                                 (cgi.escape(item.name),
                                 item.minplayers,
                                 item.maxplayers,
                                 item.difficulty,
                                 item.date))
        self.response.write('</table></br></body></html>')

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

app = webapp2.WSGIApplication([
    ('/admin', Admin),
    ('/admin/add', AddGame),
], debug=True)
