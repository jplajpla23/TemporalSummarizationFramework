import conteme.engines
import conteme.conteme
from datetime import datetime

import json

print('Params')
domains = [ 'http://publico.pt/', 'http://www.dn.pt/', 'http://www.rtp.pt/', 'http://www.cmjornal.xl.pt/', 'http://www.iol.pt/', 'http://www.tvi24.iol.pt/', 'http://noticias.sapo.pt/', 'http://expresso.sapo.pt/', 'http://sol.sapo.pt/', 'http://www.jornaldenegocios.pt/', 'http://abola.pt/', 'http://www.jn.pt/', 'http://sicnoticias.sapo.pt/', 'http://www.lux.iol.pt/', 'http://www.ionline.pt/', 'http://news.google.pt/', 'http://www.dinheirovivo.pt/', 'http://www.aeiou.pt/', 'http://www.tsf.pt/', 'http://meiosepublicidade.pt/', 'http://www.sabado.pt/', 'http://dnoticias.pt/', 'http://economico.sapo.pt/' ]
#domains = [ 'http://publico.pt/']

params = { 'domains':domains, 'from':datetime(year=2016, month=3, day=1), 'to':datetime(year=2018, month=1, day=10) }
query = 'Dilma Rousseff'

print('engine and conteme')
apt = conteme.engines.ArquivoPT()
cont = conteme.conteme.Conteme()

print('Results', end='... ')
rr = apt.getResult(query=query, **params)
resultset_str = apt.toStr(rr)

text_file = open("test_search_result.json", "w")
text_file.write(resultset_str)
text_file.close()

#print('interlvals')
#intervals = cont.build_intervals(rr, 'pt', query)

#print(len(rr))
#for inte in intervals:
#    print(inte)


#timeseries = intervals[""]

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