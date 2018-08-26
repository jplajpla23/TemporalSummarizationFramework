# Temporal Summarization
Temporal summarization engine

## Install
 ```bash
 pip install -r requirements.txt
```

## Usage 

Using ArquivoPT search engine API as datasource.
  
```python  
  from conteme.datasources.ArquivoPT import ArquivoPT

  domains = [ 'http://publico.pt/', 'http://www.dn.pt/', 'http://www.rtp.pt/', 'http://www.cmjornal.xl.pt/', 'http://www.iol.pt/', 'http://www.tvi24.iol.pt/', 'http://noticias.sapo.pt/', 'http://expresso.sapo.pt/', 'http://sol.sapo.pt/', 'http://www.jornaldenegocios.pt/', 'http://abola.pt/', 'http://www.jn.pt/', 'http://sicnoticias.sapo.pt/', 'http://www.lux.iol.pt/', 'http://www.ionline.pt/', 'http://news.google.pt/', 'http://www.dinheirovivo.pt/', 'http://www.aeiou.pt/', 'http://www.tsf.pt/', 'http://meiosepublicidade.pt/', 'http://www.sabado.pt/', 'http://dnoticias.pt/', 'http://economico.sapo.pt/']

  params = { 'domains':domains, 
            'from':datetime(year=2016, month=3, day=1), 
            'to':datetime(year=2018, month=1, day=10) }
  
  query = 'Dilma Rousseff'
  language = "pt"

  apt =  ArquivoPT()
  search_result = apt.getResult(query=query, **params)
```  

Computing important dates and selecting relevant keyphrases
  
```python 
  cont = conteme.conteme.Conteme()
  intervals = cont.build_intervals(search_result, language, query)

  periods = intervals["results"]
  for period in periods:
      print("-------------------------")
      print(period["from"],"until",period["to"])
      headlines = period["from_all_keys"]
      for headline in headlines:
          print("\t",headline.kw)
``` 

``` 
-------------------------
2016-03-01 01:22:06 until 2016-03-26 07:03:42
	 líder da maior associação patronal do brasil pede saída de dilma rousseff
	 começou processo de impeachment de dilma rousseff
	 lula da silva e dilma rousseff
	 dilma rousseff visitará hoje lula da silva
	 dilma sai em defesa de lula da silva
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
-------------------------
2016-05-04 17:17:24 until 2016-05-29 21:13:03
	 processo de destituição de dilma rousseff já está no senado
	 aprovado relatório favorável ao impeachment de dilma
	 aprovado parecer que pede destituição de dilma
	 comissão do senado viabiliza abertura do processo de impeachment de dilma
	 destituição de dilma rousseff avança
	 morreu soldado que torturou dilma rousseff
	 senadores decidem na quarta-feira futuro político da presidente dilma rousseff
	 revogada decisão que suspendia processo de impeachment de dilma
	 ex-ministro das finanças de lula e dilma detido
	 defesa de dilma rousseff vai recorrer contra destituição para o supremo
	 câmara dos deputados recua e segue com destituição de dilma rousseff
	 senado recusa anular destituição de dilma
	 supremo e senado decidem futuro de dilma
	 começou a votação no senado do pedido de destituição de dilma rousseff
	 senado deve aprovar julgamento e afastamento de dilma
	 dilma rousseff mais perto da porta dos fundos
	 dilma rousseff afastada da presidência do brasil
	 senado aprova processo de destituição de dilma
	 vodafone e rock in rio criam primeira cidade do rock inteligente do mundo
	 presidente do senado decide manter impeachment de dilma
-------------------------
2016-06-01 07:01:32 until 2016-08-20 01:02:45
	 dilma chega a portugal em plena crise polí­tica
	 parlamentares aceleram tramitação de processo de destituição de dilma
	 raúl castro apoia nicolás maduro e dilma roussseff
	 michel temer corta cartão de alimentação de dilma
	 dilma e lula visados por odebrecht e oas
	 senado vota afastamento definitivo de rousseff durante os jogos
	 milhares apoiam dilma em são paulo mesmo sabendo que regresso será difícil
	 dilma favorável à realização de eleições se voltar à presidência
	 supremo nega pedido de dilma para trocar relator
	 milhares de manifestantes mediram a força da destituição de dilma nas ruas
	 relatório do senado dá parecer favorável à destituição de dilma rousseff
	 deputados brasileiros aprovam afastamento definitivo de dilma roussef
	 aberto caminho à destituição de dilma rousseff
	 dilma rousseff enfrenta nova fase do impeachment
	 senado decide se dilma vai a julgamento
	 senadores decidem levar dilma rousseff a julgamento
	 dilma rousseff decide ir ao senado fazer a sua prí ³ pria defesa
	 supremo tribunal autoriza abertura de inquérito a dilma e lula
	 dilma rousseff defende eleições antecipadas
	 edp brasil não está preocupada com o impeachment de dilma
-------------------------
2016-08-24 06:31:15 until 2016-11-13 11:11:42
	 julgamento sobre impeachment de dilma rousseff já começou
	 senado aprova julgamento de dilma
	 dilma rousseff garante ser inocente
	 dilma rousseff garante que nunca renunciará ao cargo
	 acusação de dilma é quase bizarra se comparada com o lava jato
	 discurso de dilma rousseff é de despedida
	 confrontos no brasil durante discussão sobre futuro de dilma
	 dilma rousseff destituída do cargo de presidente do brasil
	 senado brasileiro decide hoje se dilma rousseff é ou não destituída
	 taylor swift furiosa com o vídeo de kanye west
	 daniel oliveira pede andreia rodrigues em casamento
	 cristiano ronaldo partilha história de bernardo pinto coelho
	 sofia cerveira e gonçalo diniz no santuário de fátima
	 começa julgamento sobre destituição de dilma rousseff
	 cristina ferreira e manuel luís goucha fazem dueto
	 kim kardashian e kanye west de olhos azuis
	 cristiano ronaldo no casamento de jorge mendes
	 rousseff recorre ao supremo tribunal e alega irregularidades
	 tumultos em são paulo depois de destituição de dilma rousseff
	 brasileiros saem à rua contra destituição de dilma rousseff
 ``` 
