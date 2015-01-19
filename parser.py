# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import xlsxwriter
from pyparsing import *

tdStart,tdEnd = makeHTMLTags("td")
td = tdStart + SkipTo(tdEnd).setResultsName("data") + tdEnd
def procesar(table, cantidad):
        #file=open("tabla" + str(cantidad) + ".xlsx","w")
        workbook=xlsxwriter.Workbook("libro"+str(cantidad)+".xlsx")
        worksheet=workbook.add_worksheet()
        worksheet.write(0,0,"nombre")
        worksheet.write(0,1,"valor")
        worksheet.write(0,2,"valor_ant")
        rows=table.findAll("tr")
        table=[]
        rown=1
        coln=0
        sirve = False
        for row in rows:
                if sirve:
                        cols=row.findAll("td")
                        for col in cols:
                                for tokens,start,end in td.scanString(str(col)):
                                        row.append(tokens.data.strip())
                                        worksheet.write(rown,coln,tokens.data.decode('utf-8').strip())
                                coln+=1
                        rown+=1
                        coln=0
                else:
                        sirve = True
        workbook.close()

url="http://www.svs.cl/institucional/mercados/entidad.php?auth=&send=&mercado=V&rut=61808000&rut_inc=&grupo=0&tipoentidad=RVEMI&vig=VI&row=AABbBQABwAAAA5TAAm&mm=12&aa=2013&tipo=C&orig=lista&control=svs&tipo_norma=IFRS&pestania=3"
page = urllib2.urlopen(url)
soup=BeautifulSoup(page)
soup_tables=soup.findAll("table",limit=4)
c=0
for table in soup_tables:
	c+=1
	procesar(table, c)
	break
'''
file=open("html.txt","w")
file.write(str(soup_tables))
file.close()
'''
