#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os

rut_op = [61808000,99542570,99540870,
99541380,99501280,96963440,
76215634,
76741450,
76215637,
76215628,
96579330,
76833300,
89900400,
76000739,
96579800]

for rut in rut_op:
  for x in  range(6):
    anio = x + 2008
    os.system("parser.py 12 " + str(anio)+" "+str(rut))

