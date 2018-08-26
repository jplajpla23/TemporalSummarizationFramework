# TemporalSummarization
temporal summarization engine

## install
  > pip install -r requirements.txt

## Usage 

### Using ArquivoPT search engine API as datasource.
  
  from conteme.datasources.ArquivoPT import ArquivoPT

  domains = [ 'http://publico.pt/', 'http://www.dn.pt/', 'http://www.rtp.pt/', 'http://www.cmjornal.xl.pt/', 'http://www.iol.pt/', 'http://www.tvi24.iol.pt/', 'http://noticias.sapo.pt/', 'http://expresso.sapo.pt/', 'http://sol.sapo.pt/', 'http://www.jornaldenegocios.pt/', 'http://abola.pt/', 'http://www.jn.pt/', 'http://sicnoticias.sapo.pt/', 'http://www.lux.iol.pt/', 'http://www.ionline.pt/', 'http://news.google.pt/', 'http://www.dinheirovivo.pt/', 'http://www.aeiou.pt/', 'http://www.tsf.pt/', 'http://meiosepublicidade.pt/', 'http://www.sabado.pt/', 'http://dnoticias.pt/', 'http://economico.sapo.pt/']

  params = { 'domains':domains, 'from':datetime(year=2016, month=3, day=1), 'to':datetime(year=2018, month=1, day=10) }
  query = 'Dilma Rousseff'
  language = "pt"

  #instantiate ArquivoPT search engine
  apt =  ArquivoPT()

  print('Perform search')
  search_result = apt.getResult(query=query, **params)
  
### Computing important dates and selecting relevant keyphrases

  cont = conteme.conteme.Conteme()
  intervals = cont.build_intervals(search_result, language, query)

  periods = intervals["results"]
  for period in periods:
      print("-------------------------")
      print(period["from"],"until",period["to"])
      headlines = period["from_all_keys"]
      for headline in headlines:
          print("\t",headline.kw)
