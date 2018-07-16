import engines # import SearchEngine
import conteme
#import .engines # import ArquivoPT
#import .conteme # import Conteme


domains = [ 'http://publico.pt/', 'http://www.dn.pt/', 'http://www.rtp.pt/', 'http://www.cmjornal.xl.pt/', 'http://www.iol.pt/', 'http://www.tvi24.iol.pt/', 'http://noticias.sapo.pt/', 'http://expresso.sapo.pt/', 'http://sol.sapo.pt/', 'http://www.jornaldenegocios.pt/', 'http://abola.pt/', 'http://www.jn.pt/', 'http://sicnoticias.sapo.pt/', 'http://www.lux.iol.pt/', 'http://www.ionline.pt/', 'http://news.google.pt/', 'http://www.dinheirovivo.pt/', 'http://www.aeiou.pt/', 'http://www.tsf.pt/', 'http://meiosepublicidade.pt/', 'http://www.sabado.pt/', 'http://dnoticias.pt/', 'http://economico.sapo.pt/' ]
params = { 'domains':domains, 'from':datetime(year=2016, month=3, day=1), 'to':datetime(year=2018, month=1, day=10) }

query = 'Dilma Rousseff'

apt = engines.ArquivoPT()
rr = apt.getResult(query=query, **params)
cont = conteme.Conteme()
cont.build_intervals(rr, 'pt', query)
