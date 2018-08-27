# -*- coding: utf-8 -*-

"""Console script for tempsummarization."""
import sys
import click
from datetime import datetime
from click_datetime import Datetime
from contamehistorias.engine import TemporalSummarizationEngine
from contamehistorias.datasources.ArquivoPT import ArquivoPT

default_domains = [ 'http://publico.pt/', 'http://www.dn.pt/', 'http://www.rtp.pt/', 'http://www.cmjornal.xl.pt/', 'http://www.iol.pt/', 'http://www.tvi24.iol.pt/', 'http://noticias.sapo.pt/', 'http://expresso.sapo.pt/', 'http://sol.sapo.pt/', 'http://www.jornaldenegocios.pt/', 'http://abola.pt/', 'http://www.jn.pt/', 'http://sicnoticias.sapo.pt/', 'http://www.lux.iol.pt/', 'http://www.ionline.pt/', 'http://news.google.pt/', 'http://www.dinheirovivo.pt/', 'http://www.aeiou.pt/', 'http://www.tsf.pt/', 'http://meiosepublicidade.pt/', 'http://www.sabado.pt/', 'http://dnoticias.pt/', 'http://economico.sapo.pt/']

@click.command()
@click.option('--query', help="Perform news retrieval with informed query")
@click.option('--domains',default=",".join(default_domains), help="Comma separated list of domains (www.publico.pt,www.dn.pt)")
@click.option('--language',default="pt", help="Expected language in headlines")
@click.option('--start_date', type=Datetime(format='%d/%m/%Y'), default=datetime(year=2010, month=1, day=1), help="Perform news retrieval since this date")
@click.option('--end_date', type=Datetime(format='%d/%m/%Y'), default=datetime.now(), help="Perform news retrieval until this date")
def main(query, domains, language, start_date, end_date):
    """Console script for tempsummarization."""
    click.echo("Conta-me Historias Temporal Summarization Engine")
    print("--query",query)
    #print("--domains",domains)
    print("--start_date",start_date)
    print("--end_date",end_date)
    print("--language",language)
    print()

    params = { 'domains':domains.split(","), 
                'from':start_date, 
                'to':end_date }

    click.echo("Performing search using Arquivo.pt search engine. This may take a while.")
    apt =  ArquivoPT()
    search_result = apt.getResult(query=query, **params)

    click.echo("Compute temporal summarization")
    engine = TemporalSummarizationEngine()
    summary_result = engine.build_intervals(search_result, language, query)

    engine.pprint(summary_result)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
