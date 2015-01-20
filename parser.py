# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import xlsxwriter
from pyparsing import *
import re
import sys

tdStart,tdEnd = makeHTMLTags("td")
td = tdStart + SkipTo(tdEnd).setResultsName("data") + tdEnd

dict_ruts_op={61808000: "aguas_andinas",
99542570: "aguas_chañar",
99540870: "aguas_antofagasta",
99541380: "aguas_valle",
99501280: "aguas_patagonia",
96963440: "nuevo_sur",
76215634: "aguas_altiplano",
76741450: "tratacal",
76215637: "aguas_araucania",
76215628: "aguas_magallanes",
96579330: "essbio",
76833300: "essbio",
89900400: "esval",
76000739: "esval",
96579800: "essal"}
dict_informe = {1 : "situacion_financiera",2 : "resultado"}
def isInt(s):
        try:
                int(s)
                return True
        except ValueError:
                return False

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
def main(argv):
        if(len(argv)!=3):
                print "se deben entregar 3 argumentos enteros, un mes y un anio"
                return
        if(not isInt(argv[0]) or not isInt(argv[1]) or not isInt(argv[2])):
                print "Ambos argumentos deben ser números enteros"
                return
        par_m=argv[0]
        par_a=argv[1]
        par_rut=argv[2]

        url="http://www.svs.cl/institucional/mercados/entidad.php?auth=&send=&mercado=V&rut=00000000&rut_inc=&grupo=0&tipoentidad=RVEMI&vig=VI&row=AABbBQABwAAAA5TAAm&mm=22&aa=1111&tipo=C&orig=lista&control=svs&tipo_norma=IFRS&pestania=3"
        url = url.replace("aa=1111", "aa="+par_a)
        url = url.replace("mm=22", "mm="+par_m)
        url = url.replace("rut=00000000", "rut="+par_rut)
        #Obtencion de datos del archivo(anio, mes y rut operador)
        anio = par_a
        mes = par_m
        rut = par_rut
        #nombre_archivo = dict_ruts_op[int(rut)]+"_"+mes+"_"+anios

        page = urllib2.urlopen(url)
        soup=BeautifulSoup(page)
        soup_tables=soup.findAll("table",limit=4)

        #Validar la existencia de informacion en dicho url
        if len(soup.find_all(text=re.compile("No existe informa"))) == 0:
                c=0
                for table in soup_tables:
                        c+=1
                        nombre_archivo = dict_ruts_op[int(rut)]+"_"+dict_informe[c]+"_"+mes+"_"+anio
                        print nombre_archivo
                        procesar(table, nombre_archivo)
                        if(c==2):
                                break
        else:
                print "No se encontro informacion"


if __name__ == "__main__":
   main(sys.argv[1:])
