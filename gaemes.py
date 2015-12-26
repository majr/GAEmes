import webapp2
import jinja2
import google.appengine.ext

from os import path
import query as q

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

index_template = env.get_template('templates/index.html')

# Display landing page with full game list
class MainPage(webapp2.RequestHandler):
    def get(self):
        games = q.game_query.fetch()
        self.response.write(index_template.render(games=games))

# Display page with results filtered by user input
class Query(webapp2.RequestHandler):
    def get(self):
        try:
            playercount = int(self.request.get("playerlimit"))
        except ValueError:
            playercount = 0
        try:
            timelimit = int(self.request.get("timelimit"))
        except ValueError:
            timelimit = 999999

        games = q.game_query.fetch()
        filterlist = []
            
        for item in games:
            if (playercount == 0):
                if (item.maxtime <= timelimit):
                    filterlist.append(item)
            else:
                if (item.maxplayers >= playercount >= item.minplayers) and (item.maxtime <= timelimit):
                    filterlist.append(item)
                
        self.response.write(index_template.render(games=filterlist))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/query', Query),
])
