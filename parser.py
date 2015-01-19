from bs4 import BeautifulSoup
import urllib2
from pyparsing import *

tdStart,tdEnd = makeHTMLTags("td")
td = tdStart + SkipTo(tdEnd).setResultsName("data") + tdEnd
def procesar(table, cantidad):
        file=open("tabla" + str(cantidad) + ".txt","w")
        rows=table.findAll("tr")
        table=[]
        for row in rows:
        	cols=row.findAll("td")
        	row=[]
        	for col in cols:
        		for tokens,start,end in td.scanString(str(col)):
        			row.append(tokens.data)
        	table.append(row)
        for row in table:
        	file.write(" ".join(row))
        file.close()


url="http://www.svs.cl/institucional/mercados/entidad.php?auth=&send=&mercado=V&rut=61808000&rut_inc=&grupo=0&tipoentidad=RVEMI&vig=VI&row=AABbBQABwAAAA5TAAm&mm=12&aa=2013&tipo=C&orig=lista&control=svs&tipo_norma=IFRS&pestania=3"
page = urllib2.urlopen(url)
soup=BeautifulSoup(page)
soup_tables=soup.findAll("table",limit=4)
c=0
for table in soup_tables:
	c+=1
	procesar(table, c)
'''
file=open("html.txt","w")
file.write(str(soup_tables))
file.close()
'''
