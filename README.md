# GAEmes

GAEmes is a simple web database built on top of [Google App Engine ](https://cloud.google.com/appengine/docs)(the 'GAE' in GAEmes). It is designed as a quick, easy, and _free_ way to publish a list of board games that can be queried based on number of players and amount of game time.

## History

GAEmes was born out of a practical problem. I have intimate knowledge of the games in my collection but others don't. When hosting games nights time is always wasted trying to determine what games are playable in the time remaining and with the players present. GAEmes allows anyone to load up the database and query for titles that meet those criteria. It was originally built as a mysql database with a php/html front end but I got tired of having to maintain the equipment it ran on.

## Prerequisites

1. A Google account
2. A computer that will run the Google App Engine Python SDK (Linux, Mac OS X, Windows)

## Setup

Deploying to Google App Engine is free given your app doesn't exceed the [daily quota](https://cloud.google.com/appengine/docs/quotas). GAEmes is trivially small and I don't expect you'll encounter quota issues. However, I recommend you do not set your app up with a billing account. This way there is no chance you'll be charged should there be an extreme influx of traffic.

1. Clone or Download the GAEmes github repo
2. [Download](https://cloud.google.com/appengine/downloads?hl=en#Google_App_Engine_SDK_for_Python) the Python SDK
3. [Create](https://cloud.google.com/appengine/docs/python/gettingstartedpython27/uploading) a Google Cloud application and deploy GAEmes.

## Usage

There are two main components to GAEmes.

Landing page:
This page is publicly viewable. It initially displays the full contents of your collection and offers the ability to filter by amount of time and player count.

Admin page:
This page is accessible only to administrators of the app by appending 'admin' to the base URL (e.g. mycoolapp.appspot.com/admin). This is where you can easily add items to your collection.

Note: In this initial version only adding items is supported through the admin page. To modify/remove an item you'll need to do it via the [datastore interface](https://console.developers.google.com/datastore).

## Example

You can view my personal collection at [games.mattjriley.com](http://games.mattjriley.com/).

## License

GAEmes is released under the MIT license. See the [LICENSE](LICENSE.md) file for full details.
