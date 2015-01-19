# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import xlsxwriter
from pyparsing import *
import re

tdStart,tdEnd = makeHTMLTags("td")
td = tdStart + SkipTo(tdEnd).setResultsName("data") + tdEnd
def procesar(table, nombre):
        workbook=xlsxwriter.Workbook(nombre+".xlsx")
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
                                		data=tokens.data.decode('utf-8').strip()
                                		if(data.startswith("<strong>")):
                                			data=data.replace("<strong>","")
                                			data=data.replace("</strong>","")
                                		worksheet.write(rown,coln,data)
                                coln+=1
                        rown+=1
                        coln=0
                else:
                        sirve = True
        workbook.close()

url="http://www.svs.cl/institucional/mercados/entidad.php?auth=&send=&mercado=V&rut=61808000&rut_inc=&grupo=0&tipoentidad=RVEMI&vig=VI&row=AABbBQABwAAAA5TAAm&mm=12&aa=2013&tipo=C&orig=lista&control=svs&tipo_norma=IFRS&pestania=3"
#Obtencion de datos del archivo(anio, mes y rut operador)
ini = url.find("aa=")+3
anio = url[ini:ini+4]
ini = url.find("mm=")+3
mes = url[ini:ini+2]
ini = url.find("rut=")+4
rut = url[ini:ini+8]
nombre_archivo = rut+"_"+mes+"_"+anio
print nombre_archivo

page = urllib2.urlopen(url)
soup=BeautifulSoup(page)
soup_tables=soup.findAll("table",limit=4)
c=0
for table in soup_tables:
	c+=1
	procesar(table, nombre_archivo)
	if(c==2):
		break
