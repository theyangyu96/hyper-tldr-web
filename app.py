import web
import json
import requests
import urllib

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
		greeting = web.ctx.query
		form = web.input(url="",lines="")
		temp_url = urllib.quote(form.url.encode('UTF-8'))
		url = 'https://api.aylien.com/api/v1/summarize?url=%s&sentences_number=%s' %(temp_url ,form.lines)
		payload = {}
		head = { "X-AYLIEN-TextAPI-Application-Key": "68188d3a9d107b0f84480d7429a463f5","X-AYLIEN-TextAPI-Application-ID": "d974775d"}
		r = requests.post(url, data=json.dumps(payload), headers=head)
		try:
			smry = r.json()["sentences"]
		except:
			return render.index(body="an error occurred while getting TL;DR",title="",date="",author="")
		val = ""
		for s in smry:
			val+=(s+"\n");
		if (val == None or val ==""):
			val = "Hyper-TLDR had trouble fetching the summary. You gotta read it yourself this time :<"
		url = 'https://api.aylien.com/api/v1/extract?url=%s' %(temp_url)
		payload = {}
		head = { "X-AYLIEN-TextAPI-Application-Key": "68188d3a9d107b0f84480d7429a463f5","X-AYLIEN-TextAPI-Application-ID": "d974775d"}
		r = requests.post(url, data=json.dumps(payload), headers=head)
		title = r.json()["title"]
		author = r.json()["author"]
		date = r.json()["publishDate"]
		return render.index(body = val,title = title, author = author, date= date)
	def POST(self):
		form = web.input()
		if(form.url == None or form.lines == None or form.url == "" or form.lines == ""):
			return render.index(body="",title="",date="",author="")
		temp_url = urllib.quote(form.url.encode('UTF-8'))
		url = 'https://api.aylien.com/api/v1/summarize?url=%s&sentences_number=%s' %(temp_url ,form.lines)
		payload = {}
		head = { "X-AYLIEN-TextAPI-Application-Key": "68188d3a9d107b0f84480d7429a463f5","X-AYLIEN-TextAPI-Application-ID": "d974775d"}
		r = requests.post(url, data=json.dumps(payload), headers=head)
		try:
			smry = r.json()["sentences"]
		except :
			return render.index(body="error",title="",date="",author="")
		val = ""
		for s in smry:
			val+=(s+"\n");
		if (val == None or val ==""):
			val = "Hyper-TLDR had trouble fetching the summary. You gotta read it yourself this time :<"
		url = 'https://api.aylien.com/api/v1/extract?url=%s' %(temp_url)
		payload = {}
		head = { "X-AYLIEN-TextAPI-Application-Key": "68188d3a9d107b0f84480d7429a463f5","X-AYLIEN-TextAPI-Application-ID": "d974775d"}
		r = requests.post(url, data=json.dumps(payload), headers=head)
		title = r.json()["title"]
		author = r.json()["author"]
		date = r.json()["publishDate"]
		return render.index(body = val,title = title, author = author, date= date)
if __name__ == "__main__":
	app.run()