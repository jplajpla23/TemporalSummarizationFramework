
from collections import Counter, namedtuple
from urllib.parse import urlparse
from multiprocessing import Pool
from itertools import repeat
from datetime import datetime
import requests, json, re, time
from dateutil import parser
import numpy as np
import random
import time

#ResultHeadLine = namedtuple('ResultHeadLine', ['headline', 'datetime', 'domain', 'url'])


class RoundTripEncoder(json.JSONEncoder):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%s %s" % (self.DATE_FORMAT, self.TIME_FORMAT))
        return super(RoundTripEncoder, self).default(obj)

class ResultHeadLine(object):
	def __init__(self, headline, datetime, domain, url):
		self.headline = headline
		self.datetime = datetime
		self.domain = domain
		self.url = url
	@classmethod
	def decoder(cls, json_str):
		json_obj = json.loads(json_str)
		return cls(headline = json_obj['headline'], datetime=datetime.strptime(json_obj['datetime'], "%s %s" % (RoundTripEncoder.DATE_FORMAT, RoundTripEncoder.TIME_FORMAT)), domain = json_obj['domain'], url = json_obj['url'])
	def encoder(self):
		return json.dumps(self.__dict__, cls=RoundTripEncoder)

# list_of_headlines_str = list(map(lambda obj: obj.encoder(), list_of_headlines_obj))
# list_of_headlines_obj = [ engines.ResultHeadLine.decoder(x) for x in list_of_headlines_str ]
class SearchEngine(object):
	def __init__(self, name):
		self.name = name
	def getResult(self, query, **kwargs):
		raise NotImplementedError('getResult on ' + self.name + ' not implemented yet!')
	def toStr(self, list_of_headlines_obj):
		return json.dumps(list(map(lambda obj: obj.encoder(), list_of_headlines_obj)))
	def toObj(self, list_of_headlines_str):
		return [ ResultHeadLine.decoder(x) for x in json.loads(list_of_headlines_str) ]

class ArquivoPT(SearchEngine):
	URL_REQUEST = 'http://arquivo.pt/textsearch'
	INPUT_FORMAT = '%Y%m%d%H%M%S'

	REPLC_DICT =  dict([
		(u"Ã¡", u"á"), (u"Ã ", u"à"),(u"Ã£", u"ã"), (u'Ã¢',u'â'), (u'Ã',u'Á'),# a
		(u"Ã©", u"é"), (u'Ãª', u'ê'),
		(u"Ã³", u"ó"), (u"Ãµ", u"õ"), (u'Ã´',u'ô'),
		(u"Ãº", u"ú"), (u'Ã', u'Ú'),
		(u'Ã§',u'ç'),
		(u"Ã", u"í")])

	def __init__(self, maxItemsPerSite=500, domains_by_request=2, processes=2, qtd_docs_per_query=1000):
		SearchEngine.__init__(self, 'ArquivoPT')
		self.maxItemsPerSite = maxItemsPerSite
		self.domains_by_request = domains_by_request
		self.processes = processes
		self.qtd_docs_per_query = qtd_docs_per_query
	
	def multiple_replace(self, string):
		pattern = re.compile("|".join([re.escape(k) for k in ArquivoPT.REPLC_DICT.keys()]), re.M)
		return pattern.sub(lambda x: ArquivoPT.REPLC_DICT[x.group(0)], string)

	def getResult(self, query, **kwargs):
		domains = kwargs['domains']
		random.shuffle(domains)
		interval = ( kwargs['from'].strftime(ArquivoPT.INPUT_FORMAT), kwargs['to'].strftime(ArquivoPT.INPUT_FORMAT) )

		domains_chunks = [domains[i:i + min(self.domains_by_request, len(domains))] for i in range(0, len(domains), min(self.domains_by_request, len(domains)))]
		
		#query = self.build_query(query)

		with Pool(processes=self.processes) as pool:
			dominio_chunk_result = pool.starmap(self.get_individual_result, zip(domains_chunks, repeat(query), repeat(interval)))
			#dominio_chunk_result = pool.map_async(self.get_individual_result, zip(domains_chunks, repeat(query), repeat(interval)))

		#dominio_chunk_result = dominio_chunk_result.get(50)

		all_results = []
		for dominio_list in [ dominio_list for dominio_list in dominio_chunk_result if dominio_list is not None ]:
			all_results.extend( dominio_list )
		return all_results
	def build_query(self, query):
		import unicodedata
		search_query = ''.join((c for c in unicodedata.normalize('NFD', query) if unicodedata.category(c) != 'Mn'))
		if search_query != query:
			query = '((%s) OR (%s))' % (query, search_query)
			print(query)
		return query
	
	def get_individual_result(self, domains, query, interval):
		params = {
		'q':query,
		'from':interval[0],
		'to':interval[1],
		'siteSearch':','.join([urlparse(d).netloc for d in domains]),
		'maxItems':self.qtd_docs_per_query,
		'itemsPerSite':min( self.maxItemsPerSite , int(2000/len(domains))),
		'type':'html',
		'fields': 'originalURL,title,tstamp,encoding,linkToArchive'
		}

		print("##########################################################")
		print("Requesting news from Arquivo.pt API",self.URL_REQUEST)
		print('Starting thread with domains =', domains)
		print("request params",params)

		try:
			arquivopt_query_time = time.time()
			response = requests.get(ArquivoPT.URL_REQUEST, params=params, timeout=45)
			print("request.url",response.url)
			arquivopt_query_time = time.time() - arquivopt_query_time
			print("tempo de resposta",arquivopt_query_time)
		except:
			print('Timeout domains =', domains)
			return None
		print('End thread with domains =', domains)
		if response.status_code != 200:
			return None
		json_obj = response.json()
		results = {}
		
		for item in json_obj['response_items']:
			if not (interval[0] < item['tstamp'] < interval[1]):
				continue
			domain_url = urlparse(item['originalURL']).netloc

			if 'Ã' in item['title']:
				item['title'] = self.multiple_replace(item['title'])
			try:
				item_result = ResultHeadLine(headline=item['title'], datetime=datetime.strptime(item['tstamp'], ArquivoPT.INPUT_FORMAT), domain=domain_url, url=item['linkToArchive'])
			except:
				pass
			if domain_url not in results:
				results[domain_url] = {}
			
			if item_result.url not in results[domain_url] or results[domain_url][item_result.url].datetime > item_result.datetime:
				results[domain_url][item_result.url] = item_result
		result_array = []
		for domain in results.values():
			result_array.extend( list(domain.values()) )
		return result_array

class NYTimesSolr(SearchEngine):
	URL_REQUEST = 'http://ec2-34-203-227-243.compute-1.amazonaws.com:8983/solr/core1/select'
	INPUT_FORMAT = '%Y%m%dT%H%M%S'
	ITEM_DATE_FIELD_NAME = "Publication_Date"

	def __init__(self, processes=4):
		SearchEngine.__init__(self, 'NYTimesSolr')
		self.processes = processes

	def getResult(self, query, **kwargs):
		
		#+ ' AND Publication_Year:[' + 2015 + ' TO *]
		
		"""
		'Body_str':'',
		'Headline':'',
		'Lead_Paragraph':'',
		'Body':'',
		"""
		params = {
		'q':'Headline:(%s) OR Body_str:(%s) OR Body:(%s) OR Lead_Paragraph:(%s)' % (query, query, query, query),
		#'q':'Body:(%s) OR Headline:(%s)' % (query,query),
		'rows':2000,		
		'fl': 'Publication_Date,Lead_Paragraph,Headline,Publication_Year,Online_Section_str,Url'
		}
		print(params)
		response = requests.get(NYTimesSolr.URL_REQUEST, params=params)
		if response.status_code != 200:
			return None

		json_obj = response.json()
		results = []

		for item in json_obj['response']['docs']:

			if not (item['Headline'][0]):
				continue
			
			domain_url = "nytimes.com"
			pubdate = datetime.strptime(item[NYTimesSolr.ITEM_DATE_FIELD_NAME][0], NYTimesSolr.INPUT_FORMAT)
			
			item_result = ResultHeadLine(headline=item['Headline'][0], datetime=pubdate, domain=domain_url, url=item['Url'][0])
			
			results.append( item_result)

		return results

class BingNewsSearchAPI(SearchEngine):
	URL_REQUEST = 'https://api.cognitive.microsoft.com/bing/v7.0/news/search'
	#INPUT_FORMAT = '%Y-%m-%dT%H%M%S.0000000Z'
	INPUT_FORMAT = '%Y-%m-%dT%H:%M:%S'
	#2018-05-22T11:20:00.0000000Z
	ITEM_DATE_FIELD_NAME = "datePublished"
	API_KEY="2c85bccab9fc45f6b94f77ab95446e3f"
	
	def __init__(self, processes=4):
		SearchEngine.__init__(self, 'BingNewsSearchAPI')
		self.processes = processes
		self.headers = {"Ocp-Apim-Subscription-Key" : BingNewsSearchAPI.API_KEY}

	def parse_news_article(self, item):
		
		pubdate = datetime.strptime(item[BingNewsSearchAPI.ITEM_DATE_FIELD_NAME].replace('.0000000Z',''), BingNewsSearchAPI.INPUT_FORMAT)
		domain_name = item["provider"][0]["name"]

		result_item = ResultHeadLine(headline=item['name'], datetime=pubdate, domain=domain_name, url=item['url'])
		#mentions 
		return result_item

	def getResult(self, query, **kwargs):
		
		params  = {"q": query, "count":"100", "mkt":"en-US"}
		response = requests.get(BingNewsSearchAPI.URL_REQUEST, headers=self.headers, params=params)
		response.raise_for_status()
		search_results = response.json()

		#if response.status_code != 200:
		#	return None

		base_search_query_url = search_results["readLink"]
		print(base_search_query_url)

		num_pages = int(search_results["totalEstimatedMatches"] / 100)
		print("num_pages",num_pages)
		page_size = 100

		#first page rows
		results = []		
		
		for article in search_results["value"]:
			results.append(self.parse_news_article(article))

		#next pages if available
		for page in range(0, num_pages + 1)[:200]:
			offset = page * page_size
			params["offset"] = offset
		
			#response = requests.get(search_url, headers=headers, params=params)
			print (base_search_query_url,"offset:"+str(offset))
		
			if(page % 3 == 0):
				print("sleep")
				time.sleep(1)
		
			response = requests.get(BingNewsSearchAPI.URL_REQUEST, headers=self.headers, params=params)
			response.raise_for_status()
			search_results = response.json()
			print('TESTING',response.url, params)
			for article in search_results["value"]:
				results.append(self.parse_news_article(article))

		return results

class ElasticSearchFacebook(SearchEngine):
	URL_REQUEST = 'https://nabu.dcc.fc.up.pt/es/post/_search'
	#INPUT_FORMAT = '%d/%m/%Y'
	INPUT_FORMAT = '%Y-%m-%d %H:%M:%S'
	#INPUT_FORMAT = '%Y'
	#2018-05-22T11:20:00.0000000Z
	ITEM_DATE_FIELD_NAME = "post_published"
	
	def __init__(self):
		SearchEngine.__init__(self, 'ElasticSearchFacebook')
	
	def getResult(self, query, **kwargs):
		
		params = {"_source":"post_message,post_link,post_published,page_name","q":query,"size":"2000"}

		#params  = {"q": query, "count":"100", "mkt":"en-US"}
		response = requests.request("GET", ElasticSearchFacebook.URL_REQUEST, params=params)
		
		search_results = json.loads(response.text)

		result = []
		#print(search_results)
		for item in search_results["hits"]["hits"]:
		#	print(item.keys())
			item = item["_source"]
		#	print(item.keys())
		#	print(type(item[ElasticSearchFacebook.ITEM_DATE_FIELD_NAME]))
		#	print(item[ElasticSearchFacebook.ITEM_DATE_FIELD_NAME])
			if(type(item[ElasticSearchFacebook.ITEM_DATE_FIELD_NAME]) == int):
				pubdate = datetime.datetime.fromtimestamp(item[ElasticSearchFacebook.ITEM_DATE_FIELD_NAME]/1000)
			else:
				pubdate = datetime.datetime.strptime(item[ElasticSearchFacebook.ITEM_DATE_FIELD_NAME], ElasticSearchFacebook.INPUT_FORMAT)
			#pubdate = item[ElasticSearchFacebook.ITEM_DATE_FIELD_NAME]
			domain_name = item["page_name"]
			title = item["post_message"]
			if(title):
				#ignora textos muitos grandes
				if(len(title.split()) <= 150):
					title = title.replace("[","").replace("]","")

					result_item = ResultHeadLine(headline=title, datetime=pubdate, domain=domain_name, url=item["post_link"])
					result.append(result_item)

		return result


class ElasticSearchPubMed(SearchEngine):
	URL_REQUEST = 'https://nabu.dcc.fc.up.pt/es/pubmed/_search'
	#INPUT_FORMAT = '%Y-%m-%dT%H%M%S.0000000Z'
	INPUT_FORMAT = '%Y'
	#2018-05-22T11:20:00.0000000Z
	ITEM_DATE_FIELD_NAME = "pubdate"
	
	def __init__(self):
		SearchEngine.__init__(self, 'ElasticSearchPubMed')
	
	def getResult(self, query, **kwargs):
		
		params = {"_source":"title,language,date_available,journal,pubdate","q":query,"size":"2000"}

		#params  = {"q": query, "count":"100", "mkt":"en-US"}
		response = requests.request("GET", ElasticSearchPubMed.URL_REQUEST, params=params)
		
		search_results = json.loads(response.text)

		result = []
		print(search_results)
		for item in search_results["hits"]["hits"]:
			print(item.keys())
			item = item["_source"]
			print(item.keys())
			pubdate = datetime.strptime(item[ElasticSearchPubMed.ITEM_DATE_FIELD_NAME], ElasticSearchPubMed.INPUT_FORMAT)
			domain_name = item["journal"]
			title = item["title"]
			title = title.replace("[","").replace("]","")

			result_item = ResultHeadLine(headline=title, datetime=pubdate, domain=domain_name, url="")
			result.append(result_item)

		return result

class ElasticSearchUPorto(SearchEngine):
	URL_REQUEST = 'https://nabu.dcc.fc.up.pt/google-asn-search/_search'
	#INPUT_FORMAT = '%Y-%m-%dT%H%M%S.0000000Z'
	INPUT_FORMAT = '%Y-%m-%dT%H:%M:%S'
	#2018-05-22T11:20:00.0000000Z
	ITEM_DATE_FIELD_NAME = "date_available"
	
	def __init__(self):
		SearchEngine.__init__(self, 'ElasticSearchUPorto')
	
	def getResult(self, query, **kwargs):
		
		params = {"_source":"title,language,date_available","q":query,"size":"2000"}

		#params  = {"q": query, "count":"100", "mkt":"en-US"}
		response = requests.request("GET", ElasticSearchUPorto.URL_REQUEST, params=params)
		print(response.text)
		search_results = json.loads(response.text)

		result = []
		print(search_results)
		for item in search_results["hits"]["hits"]:
			print(item.keys())
			item = item["_source"]
			print(item.keys())
			if(ElasticSearchUPorto.ITEM_DATE_FIELD_NAME in item.keys()):
				pubdate = datetime.strptime(item[ElasticSearchUPorto.ITEM_DATE_FIELD_NAME], ElasticSearchUPorto.INPUT_FORMAT)
			
				#domain_name = item["journal"]
				domain_name = "Univesidade do Porto"
				title = item["title"]
				title = title.replace("[","").replace("]","")
				result_item = ResultHeadLine(headline=title, datetime=pubdate, domain=domain_name, url="")
				result.append(result_item)
		return result

class IRLabMediaVizSearch(SearchEngine):
	URL_REQUEST = 'http://irlab.fe.up.pt/p/mediaviz/api/items'
	#INPUT_FORMAT = '%Y-%m-%dT%H%M%S.0000000Z'
	INPUT_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
	#2018-05-22T11:20:00.0000000Z
	ITEM_DATE_FIELD_NAME = "pub_date"
	#title,source_name,url,pub_date
	def __init__(self):
		SearchEngine.__init__(self, 'IRLabMediaVizSearch')
	
	def getResult(self, query, **kwargs):
		
		params = {"q":query,"source_acronym":"nyt","rows":"2000","since":"2014-01-01","until":"2018-05-25"}
		#http://irlab.fe.up.pt/p/mediaviz/api/items?source_name=Folha%20de%20S%C3%A3o%20Paulo&q=dilma&since=2017-05-25&until=2018-05-25&rows=50&offset=100&fl=title,source_name,url,pub_date

		#params  = {"q": query, "count":"100", "mkt":"en-US"}
		response = requests.request("GET", IRLabMediaVizSearch.URL_REQUEST, params=params)
		print(response.url)
		print(response.text)
		search_results = json.loads(response.text)

		result = []
		print(search_results)
		for item in search_results:
			print(item.keys())
			#item = item["_source"]
			print(item.keys())
			pubdate = None
			try:
				pubdate = datetime.strptime(item[IRLabMediaVizSearch.ITEM_DATE_FIELD_NAME], IRLabMediaVizSearch.INPUT_FORMAT)
			except:				
				pubdate = datetime.strptime(item[IRLabMediaVizSearch.ITEM_DATE_FIELD_NAME], "%Y-%m-%dT%H:%M:%S.%fZ")
			
			if(pubdate):
				domain_name = item["source_name"]
				title = item["title"]
				title = title.replace("[","").replace("]","")

				result_item = ResultHeadLine(headline=title, datetime=pubdate, domain=domain_name, url=item["url"])
				result.append(result_item)

		return result	

import mediacloud, json, datetime

import time

from .source_domains import *
sources_ids = [x["media_id"] for x in mediacloud_news_domains_PT]
sources_ids = list(set(sources_ids))

class MediaCloudSearch(SearchEngine):
	URL_REQUEST = 'http://irlab.fe.up.pt/p/mediaviz/api/items'
	#INPUT_FORMAT = '%Y-%m-%dT%H%M%S.0000000Z'
	INPUT_FORMAT = '%Y-%m-%d %H:%M:%S'
	#2018-05-22T11:20:00.0000000Z
	ITEM_DATE_FIELD_NAME = "pub_date"
	#title,source_name,url,pub_date
	def __init__(self):
		SearchEngine.__init__(self, 'MediaCloudSearch')
		self.mc = mediacloud.api.MediaCloud('4135c5c7812fabbcf5020568e6dc81f39e58613080b32e1855bd4a8aeccced1f')

	def create_custom_query_by_ids(self, field_name, ids):
	    return "(" + field_name+":" + (" OR " + field_name + ":").join(map(str, list(ids))) + ")"

	def create_custom_query(self, field_name, range_size):
		return "(" + field_name+":" + (" OR " + field_name + ":").join(list(map(str, list(range(1,range_size)))) ) + ")"

	def getResult(self, query, **kwargs):
		
		fetch_size = 500
		stories = []
		last_processed_stories_id = 0
		media_id_query = self.create_custom_query_by_ids("media_id",sources_ids)
		#params = {"q":query,"source_acronym":"nyt","rows":"2000","since":"2014-01-01","until":"2018-05-25"}
		#http://irlab.fe.up.pt/p/mediaviz/api/items?source_name=Folha%20de%20S%C3%A3o%20Paulo&q=dilma&since=2017-05-25&until=2018-05-25&rows=50&offset=100&fl=title,source_name,url,pub_date

		#params  = {"q": query, "count":"100", "mkt":"en-US"}
		#response = requests.request("GET", MediaCloudSearch.URL_REQUEST, params=params)
		#print(response.url)
		#print(response.text)
		
		#search_results = json.loads(response.text)
		while len(stories) < 5000:
			fetched_stories = self.mc.storyList(query +' AND (language:pt AND ' + media_id_query + ")", 
										solr_filter=self.mc.publish_date_query(datetime.date(2017,1,1), datetime.datetime.now().date()),
										last_processed_stories_id=last_processed_stories_id, 
										rows= fetch_size)

			stories.extend(fetched_stories)
			if len( fetched_stories) < fetch_size:
				break
			last_processed_stories_id = stories[-1]['processed_stories_id']
		
		result = []
		for item in stories:
			print(item["publish_date"],item["language"],item["title"],item["media_url"],item["url"])

			domain_name = item["media_url"]
			title = item["title"]
			title = title.replace("[","").replace("]","").replace("&quot;","").replace("\""," ")

			
			pubdate = datetime.datetime.strptime(item["publish_date"], MediaCloudSearch.INPUT_FORMAT)
			print(type(pubdate))
			result_item = ResultHeadLine(headline=title, datetime=pubdate, domain=domain_name, url=item["url"])
			result.append(result_item)

		
		return result			

#http://irlab.fe.up.pt/p/mediaviz/api/items?source_name=Folha%20de%20S%C3%A3o%20Paulo&q=dilma&since=2017-05-25&until=2018-05-25&rows=50
#http://irlab.fe.up.pt/p/mediaviz/api/items?until=2018-05-25&since=2014-01-01&source_name=New+York+Times&rows=2000&q=Donald+Trumo

#domains = [ 'http://publico.pt/', 'http://www.dn.pt/', 'http://www.rtp.pt/', 'http://www.cmjornal.xl.pt/', 'http://www.iol.pt/', 'http://www.tvi24.iol.pt/', 'http://noticias.sapo.pt/', 'http://expresso.sapo.pt/', 'http://sol.sapo.pt/', 'http://www.jornaldenegocios.pt/', 'http://abola.pt/', 'http://www.jn.pt/', 'http://sicnoticias.sapo.pt/', 'http://www.lux.iol.pt/', 'http://www.ionline.pt/', 'http://news.google.pt/', 'http://www.dinheirovivo.pt/', 'http://www.aeiou.pt/', 'http://www.tsf.pt/', 'http://meiosepublicidade.pt/', 'http://www.sabado.pt/', 'http://dnoticias.pt/', 'http://economico.sapo.pt/' ]
#params = { 'domains':domains, 'from':datetime(year=2000, month=3, day=1), 'to':datetime(year=2018, month=1, day=10) }
#apt = ArquivoPT()
#rr = apt.getResult(query='Dilma Rousseff', **params)
#print(params, len(rr))
#for r in rr:
#	print(r.headline)

# query = 'president bush'
# importlib.reload(engines)
# nyt = engines.NYTimesSolr()
# resultset_nyt = nyt.getResult(query)
# 
# cont = conteme.Conteme(2)
# cont.build_intervals(resultset_nyt, 'en', query)
# 
# #