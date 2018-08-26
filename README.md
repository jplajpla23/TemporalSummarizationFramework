# Temporal Summarization
This package can retrive articles from Arquivo.pt web archive and produce a temporal summarization.

## Install
Requires Python 3

 ```bash
 git clone  https://github.com/LIAAD/TemporalSummarizationFramework.git
 cd TemporalSummarizationFramework
 pip install -r requirements.txt
```

## Usage 

Using ArquivoPT search engine API as datasource.
  
```python  
  from conteme.datasources.ArquivoPT import ArquivoPT

# Specify website and time frame to restrict your query
  domains = [ 'http://publico.pt/', 'http://www.dn.pt/', 'http://www.rtp.pt/', 'http://www.cmjornal.xl.pt/', 'http://www.iol.pt/', 'http://www.tvi24.iol.pt/', 'http://noticias.sapo.pt/', 'http://expresso.sapo.pt/', 'http://sol.sapo.pt/', 'http://www.jornaldenegocios.pt/', 'http://abola.pt/', 'http://www.jn.pt/', 'http://sicnoticias.sapo.pt/', 'http://www.lux.iol.pt/', 'http://www.ionline.pt/', 'http://news.google.pt/', 'http://www.dinheirovivo.pt/', 'http://www.aeiou.pt/', 'http://www.tsf.pt/', 'http://meiosepublicidade.pt/', 'http://www.sabado.pt/', 'http://dnoticias.pt/', 'http://economico.sapo.pt/']

  params = { 'domains':domains, 
            'from':datetime(year=2016, month=3, day=1), 
            'to':datetime(year=2018, month=1, day=10) }
  
  query = 'Dilma Rousseff'
  

  apt =  ArquivoPT()
  search_result = apt.getResult(query=query, **params)
```  

Computing important dates and selecting relevant keyphrases
  
```python 
  
  language = "pt"
  
  cont = conteme.conteme.Conteme()
  intervals = cont.build_intervals(search_result, language, query)
  
  cont.pprint(intervals)
	  
``` 
Output
``` 
-------------------------
2016-03-01 01:22:06 until 2016-03-26 07:03:42
	 líder da maior associação patronal do brasil pede saída de dilma rousseff
	 começou processo de impeachment de dilma rousseff
	 dilma rousseff foi a casa de lula da silva oferecer solidariedade
	 milhares de pessoas saem à rua contra governo de dilma rousseff
	 milhares saem à rua exigindo demissão da presidente brasileira dilma rousseff
	 sociedade civil exige na rua demissão de dilma rousseff
	 manifestações pressionam dilma rousseff para deixar a presidência
	 milhares protestam contra governo de dilma rousseff no brasil
	 lula já terá aceitado ser ministro de dilma rousseff
	 presidente brasileira confirma entrada de lula da silva para o seu governo
	 lula da silva é ministro de dilma
	 lula da silva toma posse como ministro de dilma
	 dilma rousseff renuncia ao cargo ao nomear lula da silva
	 partido do ministro do desporto abandona governo de dilma rousseff
	 oposição a dilma pede destituição do novo ministro da justiça
	 comissão especial vai analisar a destituição de dilma rousseff
	 gregório duvivier escreve em exclusivo para a sábado sobre dilma e lula
-------------------------
2016-03-27 04:23:41 until 2016-05-04 07:10:13
	 parceiro de coligação deixa governo de dilma rousseff
	 juiz pede desculpa por divulgar escutas de dilma e lula
	 pmdb oficializa saída do governo de dilma rousseff
	 lula da silva apoia dilma rousseff através do facebook
	 lula defende dilma em vídeo no facebook
	 lula espera que supremo tribunal autorize a sua entrada no governo brasileiro
	 josé sócrates diz que destituição de dilma é um golpe político
	 comissão do impeachment aprova parecer favorável à destituição de dilma rousseff
	 advogado do governo vê irregularidades em parecer favorável à destituição de dilma
	 deputados aprovam relatório que propõe impeachment de dilma
	 aprovado relatório que propõe a destituição de dilma rousseff
	 comissão parlamentar aprova processo de destituição de dilma rousseff
	 pedido de destituição de dilma rousseff aquece congresso brasileiro
	 câmara dos deputados vota pedido de afastamento de dilma
	 câmara dos deputados aprova impeachment de dilma rousseff
	 parlamento do brasil aprova destituição de dilma
	 temer assume presidência enquanto rousseff procura apoios na onu
	 nicolás maduro sai em defesa de dilma rousseff
	 senado brasileiro aprovou nomes dos parlamentares que vão analisar destituição de dilma
	 processo de impeachment de dilma já está na comissão especial no senado

 ``` 

## Iterate over response

 ```python
summ_result = cont.build_intervals(search_result, language, query)

for period in summ_result["results"]:
    
    print("--------------------------------")
    print(period["from"],"until",period["to"])
    
    # selected keyphrases
    keyphrases = period["from_all_keys"]
    
    for keyphrase in keyphrases:
        print(keyphrase.kw)
        
        # sources
        for headline in keyphrase.headlines:
            print("Date", headline.info.datetime)
            print("Source", headline.info.domain)
            print("Url", headline.info.url)
            
        print()  
		
 ```

## Serialization
Serializing results. Useful for caching.

### Serializing search results
 ```python
search_result = apt.getResult(query=query, **params)

# object to string
search_result_serialized = apt.toStr(search_result) 

# string to object
search_result = apt.toObj( search_result_serialized )
```
 
### Serializing summarization results
```python
import json

summ_result = conteme.build_intervals(search_result)

# object to string
summ_result_serialized = json.dumps(conteme.serialize(summ_result))

# string to object
summ_result = json.loads(str(summ_result_serialized))
```
 
