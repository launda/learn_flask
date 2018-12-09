import requests
import urllib

r = requests.get('https://api.github.com/events')  

# fetch the content of the home page of our website and print out the resultin HTML data
# prints the response in an encoded form.
# print(r.content) 

#  to see the actual text result of the HTML page
# requests will decode the raw content and show you the result.
# print(r.text)  
print(r.status_code)  

#Access-Control-Allow-Credentials	true
#Access-Control-Allow-Origin	 *
#Connection	 keep-alive
#Content-Length	 497
#Content-Type	 application/json
#Date	 Fri, 07 Dec 2018 03:44:30 GMT
#Server	 gunicorn/19.9.0
#Via	 1.1 vegur

r = requests.get('http://httpbin.org/get') 
print(r.headers['Access-Control-Allow-Credentials'])  
print(r.headers['Access-Control-Allow-Origin'])  
print(r.headers['Connection'])  
print(r.headers['Content-Length'])  
print(r.headers['Content-Type'])  
print(r.headers['Date'])  
print(r.headers['Server'])  
print(r.headers['Via'])  

r = requests.get('http://httpbin.org/get')
response = r.json()  
print(r.json())  
print(response['args'])  
print(response['headers'])  
print(response['headers']['Accept'])  
print(response['headers']['Accept-Encoding'])  
print(response['headers']['Connection'])  
print(response['headers']['Host'])  
print(response['headers']['User-Agent'])  
print(response['origin'])  
print(response['url'])  


import requests

payload = {'user_name': 'admin', 'password': 'password'}  
r = requests.get('http://httpbin.org/get', params=payload)

print(r.url)  
print(r.text)  

payload = { "format":"json", "action":"query", "list":"geosearch", "gsradius":5000,"gslimit":20}
payload["gscoord"] = '{0}%7C{1}'.format(-27.570278, 153.008056)

# params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
qs = "&".join("%s=%s" % (k, v)  for k, v in payload.items())
query_url = "https://en.wikipedia.org/w/api.php?%s" % qs
print("URL is", query_url)

# <-- this is what prints - looks good i.e params query join working well except lat lng wrong
# URL is http://en.wikipedia.org/w/api.php?\ 
# format=json&action=query&list=geosearch&gsradius=5000&gslimit=20&gscoord=None%7CNone
# query_url = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(lat, lng)
# g = urllib2.urlopen(query_url)
# g2 = urllib.request.Request(query_url)
g2 = requests.get("https://en.wikipedia.org/w/api.php", params=payload)

print(g2.url)  
print(g2.text)  
print(g2.json)  

# the Reqeusts library automatically turned our dictionary of parameters to a query string and attached it to the URL.

#URL is 
#https://en.wikipedia.org/w/api.php?format=json&action=query&list=geosearch&gsradius=5000&gslimit=20&gscoord=-27.570278%7C153.008056
#https://en.wikipedia.org/w/api.php?format=json&action=query&list=geosearch&gsradius=5000&gslimit=20&gscoord=-27.570278%257C153.008056
# {"error":{"code":"invalid-coord","info":"Invalid coordinate provided","*":"See https://en.wikipedia.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/mailman/listinfo/mediawiki-api-announce&gt; for notice of API deprecations and breaking changes."},"servedby":"mw1312"}
