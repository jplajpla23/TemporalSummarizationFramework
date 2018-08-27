from .SearchEngine import *

class BingNewsSearchAPI(SearchEngine):
	URL_REQUEST = 'https://api.cognitive.microsoft.com/bing/v7.0/news/search'
	INPUT_FORMAT = '%Y-%m-%dT%H:%M:%S'
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
		return result_item

	def getResult(self, query, **kwargs):
		
		params  = {"q": query, "count":"100", "mkt":"en-US"}
		
		
		response = requests.get(BingNewsSearchAPI.URL_REQUEST, headers=self.headers, params=params)
		response.raise_for_status()
		search_results = response.json()

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
			for article in search_results["value"]:
				results.append(self.parse_news_article(article))

		return results