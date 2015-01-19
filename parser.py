from bs4 import BeautifulSoup
import urllib2


url="http://www.svs.cl/institucional/mercados/entidad.php?auth=&send=&mercado=V&rut=61808000&rut_inc=&grupo=0&tipoentidad=RVEMI&vig=VI&row=AABbBQABwAAAA5TAAm&mm=12&aa=2013&tipo=C&orig=lista&control=svs&tipo_norma=IFRS&pestania=3"
page = urllib2.urlopen(url)
soup=BeautifulSoup(page)
soup_tables=soup.findAll("table",limit=4)
file2=open("html2.txt","w")
c=0
for row in soup_tables:
	c+=1
	col=row.findAll("td")
	file2.write(str(col))
print c
file=open("html.txt","w")
file.write(str(soup_tables))
file.close()
file2.close()
