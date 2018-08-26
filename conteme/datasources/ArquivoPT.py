from .SearchEngine import *

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
		
		with Pool(processes=self.processes) as pool:
			dominio_chunk_result = pool.starmap(self.get_individual_result, zip(domains_chunks, repeat(query), repeat(interval)))
	
	
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