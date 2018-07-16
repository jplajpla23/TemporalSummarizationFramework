from .engines import SearchEngine
from .datacore import DataCore
from .nlp import NLPallLanguages

from itertools import repeat
from collections import Counter, namedtuple
from os import path
from scipy import signal
from glob import glob
import Levenshtein, time
import numpy as np

ProcessedHeadline = namedtuple('ProcessedHeadline', ['info', 'candidates', 'ner', 'sent', 'terms'])
Keyphrase = namedtuple('Keyphrase', ['kw', 'cand_obj', 'headlines', 'sent'])

#from recordclass import recordclass
#NER = recordclass('NER', ['id', 'names', 'co_occur', 'freq'])

class Conteme(object):
	def __init__(self, windowsSize=2, top=20, thres=0.8):
		self.windowsSize = windowsSize
		self.stopwords = {}
		self.nlp_pluggins = NLPallLanguages.getInstance()
		self.top = top
		self.thres = thres

	def get_index_of(self, t, intervals):
		for (i,(min_i, max_i)) in enumerate(intervals):
			if min_i <= t < max_i:
				return i
		return None
	def get_chunk(self, sorted_resultset, qtd_intervals_param = 60, order = 2, percent=0.05):
		if len(sorted_resultset) < 2:
			return []
		times = [ x.info.datetime for x in sorted_resultset ]
		
		interval_in_days = (times[-1]-times[0]).days
		qtd_intervals = min(qtd_intervals_param, interval_in_days)
		size_time_interval = (times[-1]-times[0])/qtd_intervals

		intervals = [ (i*size_time_interval+times[0], (i+1)*size_time_interval+times[0]) for i in range(qtd_intervals) ]
		interval_index = [ self.get_index_of(t, intervals) for t in times ]

		cnt = Counter(interval_index)

		array_counted = []
		for virtual_index in range(order):
			array_counted.append( cnt[0]/((order-virtual_index)+1) )
		array_counted.extend([ cnt[c] for c in range(qtd_intervals) ])
		for virtual_index in range(order):
			array_counted.append( cnt[qtd_intervals-1]/(virtual_index+2) )

		indexes, = signal.argrelextrema(np.array(array_counted),comparator=np.greater,order=order)
		
		centers = []
		for i, c in enumerate(indexes[1:]):
			idx_break = indexes[i] + np.argmin(array_counted[indexes[i]:c])
			centers.append(intervals[idx_break-order][1])
		
		idx_chunk = 0
		chunks = []
		atual_chunk = []
		for idx_proc, time_proc in enumerate(times):
			if idx_chunk == len(centers): break
			if time_proc > centers[idx_chunk]:
				idx_chunk += 1
				chunks.append(atual_chunk)
				atual_chunk = []
			atual_chunk.append(sorted_resultset[idx_proc])
		for idx_proc, time_proc in list(enumerate(times))[idx_proc:]:
			atual_chunk.append(sorted_resultset[idx_proc])
		chunks.append(atual_chunk)
		
		min_size_chunk = max(50, percent * max([ len(chunk) for chunk in chunks ]), percent * len(sorted_resultset) )
		final_chunks = []
		atual_chunk = []
		for chunk in chunks:
			atual_chunk.extend(chunk)
			if len(atual_chunk) > min_size_chunk:
				final_chunks.append(atual_chunk)
				atual_chunk = []
		if len(atual_chunk) > 0:
			if len(atual_chunk) > min_size_chunk:
				final_chunks.append(atual_chunk)
			elif len(final_chunks) > 0:
				final_chunks[-1].extend(atual_chunk)
		return final_chunks
	def build_intervals(self, resultset, lan, query):
		
		time_preproc = time.time()
		sorted_resultset = sorted(resultset, key=lambda x: x.datetime)
		sorted_resultset = self.preprocessing(sorted_resultset)
		stopwords = self.getStopword(lan)
		time_preproc = time.time() - time_preproc
		

		time_extract = time.time()
		dc = DataCore(windowsSize=self.windowsSize, stopword_set=stopwords)
		
		processed_headline = []
		id_domain = []
		temporal_sentiment = []
		domain_id = {}
		all_key_candidates= {}
		dict_of_ners = {}
		array_of_ner = []
		
		for result in sorted_resultset:
			document_candidates, term_in_doc = dc.add_document(result.headline)

			#	NER 
			"""
			list_of_ners = self.nlp_pluggins.get_ner(result.headline, lan)
			ners_doc = []
			unique_ners = set()
			for ner_str in list_of_ners:
				ner_str = ner_str.lower().strip()
				if ner_str in dict_of_ners:
					ner_obj = dict_of_ners[ner_str]
					ner_obj.names[ner_str] += 1
					ner_obj.freq += 1
					if ner_obj.id not in unique_ners:
						unique_ners.add(ner_obj.id)
						ners_doc.append(ner_obj)
				else:
					#incluir casamento aproximado nos NERs
					max_sim = 0.
					ner_obj = None
					for n2 in array_of_ner:
						max_atual = max(map(Levenshtein.ratio, n2.names.keys(), repeat(ner_str)))
						if max_atual >= 0.6 and max_atual > max_sim:
							ner_obj = n2
							max_sim = max_atual
						elif any([ name_2 in ner_str for name_2 in n2.names ]) or any([ ner_str in name_2 for name_2 in n2.names ]) :
							ner_obj = n2
							nax_sim = 1.

					if ner_obj is None:
						ner_obj = NER(id=len(dict_of_ners), names={ner_str: 1}, freq=1, co_occur=dict() )
						dict_of_ners[ner_str] = ner_obj
						array_of_ner.append(ner_obj)
					else: 
						dict_of_ners[ner_str] = ner_obj
						ner_obj.names[ner_str] = 1
						ner_obj.freq += 1

			ners_doc = sorted(ners_doc, key=lambda x: x.id)
			for i, n1 in enumerate(ners_doc):
				for n2 in ners_doc[(i+1):]:
					if n2.id not in n1.co_occur:
						n1.co_occur[n2.id] = 1
					else:
						n1.co_occur[n2.id] += 1
			"""
			#	END NER

			proc_head = ProcessedHeadline(info=result, candidates=[], terms=term_in_doc, ner=None, sent=self.nlp_pluggins.get_sentiment(result.headline, lan))

			if proc_head.info.domain not in domain_id:
				domain_id[proc_head.info.domain] = len(id_domain)
				id_domain.append(proc_head.info.domain)
			temporal_sentiment.append( (str(proc_head.info.datetime), proc_head.sent, domain_id[proc_head.info.domain]) )
			for cand, cand_obj in document_candidates.items():
				if cand not in all_key_candidates:
					all_key_candidates[cand] = Keyphrase( kw=cand_obj.unique_kw, cand_obj=cand_obj, headlines=[], sent=self.nlp_pluggins.get_sentiment(cand_obj.kw, lan) )
				all_key_candidates[cand].headlines.append(proc_head)
				if cand_obj.isValid():
					proc_head.candidates.append(all_key_candidates[cand])
			processed_headline.append(proc_head)


		terms_correlations = [ (term_obj.unique_term, 1.-term_obj.bias) for term_obj in dc.add_bias(query)]
		dc.build_single_terms_features()
		dc.build_mult_terms_features()
		time_extract = time.time() - time_extract
		
		time_intervals = time.time()
		chunks = self.get_chunk(processed_headline)
		
		all_rank=[]
		general_array_results = []
		quality = []
		for chunk in chunks:
			from_chunk_datetime = chunk[0].info.datetime
			to_chunk_datetime = chunk[-1].info.datetime
			kws = set()
			to_analyse = []
			for doc_proc in chunk:
				for kw in doc_proc.candidates:
					if kw.kw not in kws:
						kws.add(kw.kw)
						to_analyse.append(kw)
			result_chunk, all_rank = self.build_geral_keys(to_analyse, all_kw=all_rank)

			#quality.append( np.mean( [self.sigmoid( kw.size, z0=5, b=np.e/self.top ) for kw in result_chunk ] ) )
			
			result_interval = { 'from':from_chunk_datetime, 'to':to_chunk_datetime, 'ndocs': len(chunk), 'from_all_keys': result_chunk }
			general_array_results.append(result_interval)
		time_intervals = time.time() - time_intervals
		dict_result = {
		'query': query,
		'status':'OK',
		'stats': {
			'nunique_docs': len(processed_headline), 'ndocs':len(resultset), 'ndomains': len(id_domain),
			'time': { 'total': str(time_intervals+time_extract+time_preproc),  'time_intervals': str(time_intervals), 'time_extract':str(time_extract), 'time_preproc':str(time_preproc) },
		 },
		 #'quality': (quality, self.sigmoid(len(general_array_results), z0=2, b=)),
		'domains': id_domain,
		'query_term_corr':terms_correlations[:self.top*2],
		'results': general_array_results,
		'sentiment': { 'raw':temporal_sentiment, 'all': Counter([ sent for _,sent,_ in temporal_sentiment]) }
		}
		#NER = recordclass('NER', ['id', 'names', 'co_occur', 'freq'])
		return dict_result
	def sigmoid(self, z, z0=0, b=1.):
		return  1. / ( 1. + np.exp(-b*(z-z0)) )
	def preprocessing(self, resultset):
		final_resultset = []
		headlines = set()
		for hl in resultset:
			if hl.headline not in headlines:
				headlines.add(hl.headline)
				final_resultset.append(hl)
		return final_resultset
	def build_geral_keys(self, to_analyse, sentiment=None, all_kw=[], min_size=2):
		# to_analyse = [ namedtuple('Keyphrase', ['kw', 'cand_obj', 'headlines', 'sent']) ]
		general_results = []
		if sentiment is not None:
			to_analyse = [ kw for kw in to_analyse if kw.sent == sentiment ]
		to_analyse = [ kw for kw in to_analyse if kw.cand_obj.size >= min_size ]
		to_analyse = sorted(to_analyse, key=lambda x: x.cand_obj.H)
		for kw in to_analyse:
			if self.can_add(all_kw, kw):
				general_results.append( kw )
				all_kw.append(kw)
			if len(general_results) == self.top:
				break
		general_results = sorted(general_results, key=lambda x: min([ t.info.datetime for t in x.headlines ]))
		return general_results, all_kw
	def can_add(self, all_kw, kw):
		for kw2 in all_kw:
			dd = Levenshtein.ratio(kw.cand_obj.unique_kw, kw2.cand_obj.unique_kw)
			if dd > self.thres or kw.cand_obj.unique_kw in kw2.cand_obj.unique_kw or kw2.cand_obj.unique_kw in kw.cand_obj.unique_kw:
				return False
		return True
	def getStopword(self, lan):
		if lan not in self.stopwords:
			self.stopwords[lan] = set( open(path.join(path.dirname(path.realpath(__file__)),'Resources','StopwordsList', 'stopwords_%s.txt' % lan), encoding='utf8').read().lower().split("\n") )
		return self.stopwords[lan]
	
	def serialize(self, result):
		serialized = {}
		serialized['query'] = result['query']
		serialized['query_term_corr'] = result['query_term_corr']
		serialized['domains'] = result['domains']
		serialized['status'] = result['status']
		serialized['stats'] = result['stats']

		serialized['sentiment'] = result['sentiment']
		serialized['results'] = []

		for chunk in result['results']:
			result_chunk = []
			for result_key in chunk['from_all_keys']:
				result_chunk.append(
					{ 'kw':result_key.cand_obj.kw,
					'sent': result_key.sent,
					'date': str(min([ t.info.datetime for t in result_key.headlines if chunk['from'] <= t.info.datetime <= chunk['to']])), 
					'docs':[ (t.info.headline, t.info.url) for t in result_key.headlines  ]  } )
			result_chunk = sorted(result_chunk, key=lambda kw_dict: kw_dict['date'] )
			result_interval = { 'from':str(chunk['from']), 'to':str(chunk['to']), 'ndocs': len(chunk), 'from_all_keys': result_chunk }
			serialized['results'].append(result_interval)
		return serialized
