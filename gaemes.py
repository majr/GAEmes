from google.appengine.api import users
import webapp2
import google.appengine.ext
import cgi
import query as q

MAIN_PAGE_HTML = """\
<html>
<head>
<title>My GAEmes Database</title>
</head>
<body bgcolor="white" text="black">
<center><h1><a href="/">My GAEmes Database</a></h1></center>
<center>
<form action="query" method="get">
Max Time (minutes): <input type="number" name="timelimit">
Number of Players: <select name="playerlimit">
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
        <option value="5">5</option>
        <option value="6">6</option>
        <option value="7">7</option>
        <option value="8">8</option>
        <option value="9">9</option>
        <option value="10">10</option>
        <option value="11">11</option>
        <option value="12">11</option>
        </select>
<input type="submit">
</form>
<a href="/">View All Games</a><br>
  <table border="1" align="center">
    <tr>
      <td>Game</td>
      <td>Min Players</td>
      <td>Max Players</td>
      <td>Max Time</td>
      <td>Difficulty</td>
    </tr>
"""

# Display landing page with full game list
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.write(MAIN_PAGE_HTML)

        game_query = q.Game.query(ancestor=q.db_key()).order(q.Game.name)
        games = game_query.fetch()
        gamecount = 0

        for item in games:
            self.response.write('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' %
                                 (cgi.escape(item.name),
                                 item.minplayers,
                                 item.maxplayers,
                                 item.maxtime,
                                 item.difficulty))
            gamecount += 1

        self.response.write('</table></br>Total Games: %s</body></html>' % gamecount)

# Display page with results filtered by user input
class Query(webapp2.RequestHandler):
    def get(self):
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.write(MAIN_PAGE_HTML)
            try:
                playercount = int(self.request.get("playerlimit"))
            except ValueError:
                playercount = 2
            try:
                timelimit = int(self.request.get("timelimit"))
            except ValueError:
                timelimit = 999999
            gamecount = 0

            # game_query = q.Game.query(q.Game.maxtime <= timelimit, ancestor=q.db_key())
            game_query = q.Game.query(ancestor=q.db_key()).order(q.Game.name)
            games = game_query.fetch()

            for item in games:
                if (item.maxplayers >= playercount >= item.minplayers) and (item.maxtime <= timelimit):
                    self.response.write('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' %
                                    (cgi.escape(item.name),
                                    item.minplayers,
                                    item.maxplayers,
                                    item.maxtime,
                                    item.difficulty))
                    gamecount += 1

            self.response.write('</table></br>Total Games: %s</body></html>' % gamecount)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/query', Query),
], debug=True)
