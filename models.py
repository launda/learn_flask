from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

import geocoder
# import urllib2    pyhton2
import urllib.request  # no need to install 
import json


db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))

  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)


# see this guy - parses same url but using XML
# https://scraperwiki.com/2011/12/how-to-scrape-and-parse-wikipedia/

# p = Place()
# places = p.query("1600 Amphitheater Parkway Mountain View CA")
class Place(object):
  def meters_to_walking_time(self, meters):
    # 80 meters is one minute walking time
    return int(meters / 80)  

  # https://en.wikipedia.org/wiki/Oxley,_Queensland
  # https://en.wikipedia.org/wiki/Oxley,_New_South_Wales

  def wiki_path(self, slug):
    url = urllib.request.urlparse.urljoin("http://en.wikipedia.org/wiki/", slug.replace(' ', '_'))
    return url
    # return urllib.request.urlparse.urljoin("http://en.wikipedia.org/wiki/", slug.replace(' ', '_'))
    # return urllib2.urlparse.urljoin("http://en.wikipedia.org/wiki/", slug.replace(' ', '_'))
  
  def address_to_latlng(self, address):
    g = geocoder.google(address)
    print("g = ", g )
    # g =  <[OVER_QUERY_LIMIT] Google - Geocode [empty]>   !!!ahaaaa <-- this is what prints
    return (g.lat, g.lng)

  def query(self, address):

    print("address is", address)
    lat, lng = self.address_to_latlng(address)
    print("lat, lng",lat, "\t",lng)
    # lat, lng None    None  <-- this is what prints

    params = { "format":"json", "action":"query", "list":"geosearch", "gsradius":5000,"gslimit":20}
    params["gscoord"] = '{0}%7C{1}'.format(lat, lng)
    # params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
    qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
    query_url = "http://en.wikipedia.org/w/api.php?%s" % qs
    print("URL is", query_url)
    # <-- this is what prints - looks good i.e params query join working well except lat lng wrong
    # URL is http://en.wikipedia.org/w/api.php?\ 
    # format=json&action=query&list=geosearch&gsradius=5000&gslimit=20&gscoord=None%7CNone

    # query_url = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(lat, lng)
    # g = urllib2.urlopen(query_url)
    g = urllib.request.Request(query_url)
    # see https://stackoverflow.com/questions/39861782/parsing-json-string-from-url-with-python-3-5-2

    #results = g.read()
    results  = urllib.request.urlopen(g).read()
    #g.close()

    data = json.loads(results)
    
    places = []
    for place in data['query']['geosearch']:
      name = place['title']
      meters = place['dist']
      lat = place['lat']
      lng = place['lon']

      wiki_url = self.wiki_path(name)
      walking_time = self.meters_to_walking_time(meters)

      d = {
        'name': name,
        'url': wiki_url,
        'time': walking_time,
        'lat': lat,
        'lng': lng
      }

      places.append(d)

    return places
