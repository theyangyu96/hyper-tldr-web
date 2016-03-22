import web
import json
import requests

urls = (
	'/', 'index', 
	"/summary", "summary"
)

app = web.application(urls, globals())

render = web.template.render('templates/')

class index:
	def GET(self):
		return render.index(body="",title="",date="",author="")

class summary:
	def GET(self):
		greeting = "Summary"
		return render.index(body="",title="",date="",author="")
	def POST(self):
		form = web.input()
		url = 'https://api.aylien.com/api/v1/summarize?url=%s&sentences_number=%s' %(form.url,form.lines)
		payload = {}
		head = { "X-AYLIEN-TextAPI-Application-Key": "INSERT KEY HERE","X-AYLIEN-TextAPI-Application-ID": "INSERT ID HERE"}
		r = requests.post(url, data=json.dumps(payload), headers=head)
		smry = r.json()["sentences"]
		val = ""
		for s in smry:
			val+=(s+" ");
		url = 'https://api.aylien.com/api/v1/extract?url=%s' %(form.url)
		payload = {}
		head = { "X-AYLIEN-TextAPI-Application-Key": "INSERT KEY HERE","X-AYLIEN-TextAPI-Application-ID": "INSERT ID HERE"}
		r = requests.post(url, data=json.dumps(payload), headers=head)
		title = r.json()["title"]
		author = r.json()["author"]
		date = r.json()["publishDate"]
		return render.index(body = val,title = title, author = author, date= date)
if __name__ == "__main__":
	app.run()