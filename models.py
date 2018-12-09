from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

import geocoder
# import urllib2    pyhton2
# import urllib.request  # no need to install - comes built in pythn 3
import requests
import json
import os


db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))

  # when new user fills details signup form
  # routes.py makes this call
  # form = SignupForm()  <--  form object contains all data on form in dict format after a 'POST'
  # newuser = User(form.first_name.data, form.last_name.data,form.email.data, form.password.data)
  #    db.session.add(newuser)
  #    db.session.commit()

  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  # /login route would kame this call to check user supplies password during login
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
  
  # https://developers.google.com/places/web-service/search
  # https://console.cloud.google.com/apis/library?project=my-project-1478600845464
  def address_to_latlng(self, address):
    g = geocoder.google(address)
    print("Address is = {}, g  = {}, lat = {}, long = {}".format(address, g, g.lat,g.lng ))
    # g =  <[OVER_QUERY_LIMIT] Google - Geocode [empty]>   !!!ahaaaa <-- this is what prints
    # If you exceed the usage limits you will get an OVER_QUERY_LIMIT status code as a response
    # well this was my 1st query !! in a long time...
    return (g.lat, g.lng)

  def query(self, address):

    print("address is", address)
    lat, lng = self.address_to_latlng(address)
    # lat,lng = (-27.570278, 153.008056)
    print("lat, lng",lat, "\t",lng)
    # lat, lng None    None  <-- prints none for both

    payload = { "format":"json", "action":"query", "list":"geosearch", "gsradius":5000,"gslimit":20}
    payload["gscoord"] = '{0}%7C{1}'.format(lat, lng)
    API_KEY = os.environ['GOOGLE_API_KEY']
    payload['key'] =  API_KEY
    # we set our key in .bashrc file - it works ...
    # https://stackoverflow.com/questions/45336763/using-my-google-geocoding-api-key-with-python-geocoder
    # https://console.cloud.google.com/apis/credentials?project=my-project-1478600845464
    # This API key can be used in this project and with any API that supports it. 
    # To use this key in your application, pass it with the key=API_KEY parameter.

    # params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
    qs = "&".join("%s=%s" % (k, v)  for k, v in payload.items())
    query_url = "http://en.wikipedia.org/w/api.php?%s" % qs
    print("URL is", query_url)
    # <-- this is what prints - looks good i.e params query join working well except lat lng wrong
    # URL is http://en.wikipedia.org/w/api.php?\ 
    # format=json&action=query&list=geosearch&gsradius=5000&gslimit=20&gscoord=None%7CNone

    # query_url = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(lat, lng)
    # g = urllib2.urlopen(query_url)
    # g = urllib.request.Request(query_url)
    resp = requests.get("http://en.wikipedia.org/w/api.php", params=payload)
    # see https://stackoverflow.com/questions/39861782/parsing-json-string-from-url-with-python-3-5-2

    # results = g.read()
    # AttributeError: 'Response' object has no attribute 'read'
    #results  = urllib.request.urlopen(g).read()
    #results  = g.text()
    #g.close()
    ####results = g.content()
    #TypeError: 'bytes' object is not callable

    ####data = json.loads(results)
    # TypeError: the JSON object must be str, bytes or bytearray, not 'Response'
    resp.raise_for_status()
    results = resp.json()

    #res = results['results'][0]
    #address = res['formatted_address']
    #lat = res['geometry']['location']['lat']
    #lng = res['geometry']['location']['lng']

    places = []
    for place in results['query']['geosearch']:
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
