import requests
from operator import itemgetter

numarticles = 10
numoutput = 3


# Add error check for exceeded limit on usage
# r.text
# u'{\r\n    "status": "ERROR",\r\n    "statusInfo": "daily-transaction-limit-exceeded"\r\n}\r\n'

API_KEY = ''  #redacted

#get sentiment, title, and url -- get 500 most recent articles


def getNews(sentiment):
	str_sent = '%s' %sentiment
	if sentiment > 0:
		sign = 'positive'
		eq = '%3D%3E'
	else:
		sign = 'negative'
		eq = '%3C%3D'

	# if sentiment is positive, we get 100 most recent articles with score above sentiment parameter
	# if sentiment is negative, we get 100 most recent articles with score below sentiment parameter 
	r = requests.get('https://gateway-a.watsonplatform.net/calls/data/GetNews?outputMode=json&start=now-1d&end=now&count='+ '%d' %numarticles + '10&q.enriched.url.enrichedTitle.docSentiment=%7Ctype%3D' + '%s' %sign + '%2Cscore' + '%s' %eq + '%s' %str_sent + '%7C&return=enriched.url.url%2Cenriched.url.enrichedTitle.docSentiment%2Cenriched.url.title&apikey='+'%s' % API_KEY )
	
	scores = {}

	# keep all scores in a dictionary
	for i in range (0,numarticles):
		score = r.json()['result']['docs'][i]['source']['enriched']['url']['enrichedTitle']['docSentiment']['score']
		scores[i]= score

	#make a sorted list of scores, then a list of top scores / lowest scores 

	# in high sentiment case, get top scores
	if sentiment > 0:
		sorted_scores = sorted(scores.items(), key=itemgetter(1), reverse=True)
		top_scores = sorted_scores[0:numoutput]
	# in low sentiment case, get lowest scores
	else:
		sorted_scores = sorted(scores.items(), key=itemgetter(1))
		low_scores = sorted_scores[0:numoutput]


	#makes an array to store title and url of top sentiment
	articlesarr = []
	for i in range (0,numoutput):
		#get indices for top/low scoring articles
		if sentiment > 0:
			j = top_scores[i][0]
		else:
			j = low_scores[i][0]

		title = r.json()['result']['docs'][j]['source']['enriched']['url']['title']
		url = r.json()['result']['docs'][j]['source']['enriched']['url']['url']
		articlesarr.append([title,url])

	return articlesarr


goodNews = getNews(.8)
#badNews = getNews(-.8)

print goodNews
#print badNews

# test for badnews
# r = requests.get('https://gateway-a.watsonplatform.net/calls/data/GetNews?outputMode=json&start=now-1d&end=now&count=5&q.enriched.url.enrichedTitle.docSentiment=%7Ctype%3Dnegative%2Cscore%3C%3D0.5%7C&return=enriched.url.enrichedTitle.docSentiment&apikey='+'%s' % API_KEY )


