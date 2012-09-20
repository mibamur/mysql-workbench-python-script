# -*- coding: utf-8 -*-
# 
# 
# auto-layer_for_tables_ver001.py
#
# Script create *second* EER diagram,
# group tables on each layer
#
# you must load tables structure at first from database, 
# create one EER diagram and place all tables on your diagram 
# - it`s necessary because script do not colorize table-figure and table-figure will be dark color 
#
# to run script you must go to menu -> Scripting -> Scripting Shell -> Load scrpt from file 
# OR create new script and copy code, then Execute Script
#
# for example - table like
#	product
#	product_descriprion
# 	product_something_else
# put on layer named "product" and so on - tables vendor vendor_information put on "vendor" layer 
# each layer get own color from array
#
# Written in MySQL Workbench 5.2.34 also must work in older version
# author mibamur@gmail.com
# homepage https://github.com/mibamur/mysql-workbench-python-script

import os
import re
import random
from wb import *
import grt
#import mforms

def add_new_diagram():
    grt.root.wb.doc.physicalModels[0].addNewDiagram('NEW')
    grt.root.wb.doc.physicalModels[0].diagrams[1].name = 'Opencart 1.5.5 EER'
    grt.root.wb.doc.physicalModels[0].diagrams[1].width = 8000
    grt.root.wb.doc.physicalModels[0].diagrams[1].height = 8000
    grt.root.wb.doc.physicalModels[0].diagrams[1].zoom = 0.3
    return 0

def podschet_slov():
  figsort = {}
  figtabl = {}
  TABL_S = grt.root.wb.doc.physicalModels[0].catalog.schemata[0].tables
  for TABL in TABL_S:
    ''' try find figure.name with _ '''
    txt=TABL.name
    re1='((?:[a-z]+[_]))'	# Alphanum 1
    rg = re.compile(re1,re.IGNORECASE|re.DOTALL)
    n = rg.search(txt)
    if n:
        alphanum1=n.group(1)
        ''' try find figure.name >>> txt >>> alphanum1 with one_word >>> alphanum2'''
        re2='((?:[a-z][a-z]*[0-9]*))'	# Alphanum 1
        rg = re.compile(re2,re.IGNORECASE|re.DOTALL)
        m2 = rg.search(alphanum1)
        if m2:
            alphanum2=m2.group(1)
            figsort[TABL.name] = alphanum2
            figtabl[TABL.name] = TABL
  
  for TABL in TABL_S:
    ''' try find figure.name with _ '''
    txt=TABL.name
    re1='((?:[a-z]*[a-z]))'	# Alphanum 1
    rg = re.compile(re1,re.IGNORECASE|re.DOTALL)
    n = rg.search(txt)
    if n:
        alphanum1=n.group(1)
        figsort[TABL.name] = alphanum1 #print "find word (", alphanum2, ") in ", TABL.name
        figtabl[TABL.name] = TABL

  return figsort, figtabl

def podschet_kol():
 k = {}
 ki = 1
 kv = ''
 sorr, tabb = podschet_slov()
 for ss in sorted(sorr):
    bbb = sorr.get(ss)
    if bbb == kv:
        ki = ki + 1
        k[bbb] = ki
    else:
        ki = 1
        k[bbb] = ki
        kv = bbb
 return k

def add_new_layer():
#placeNewLayer on diagram
 schet_y = 20; schet_x = 20;
 schet_diagname = ''
 kol = podschet_kol()
 colrs = ['a179f3','79c0f3','f3bb79','b0f379','f39379','7985f3','79f3db','7990f3','d6f379','f379e4','f37994','8779f3','79d3f3','adf379','f38e79','f38b79','f379ec','79f3b1','79f37c','79f39b','9ff379','f3e179','e679f3','79f3a0','f3798f','c479f3','79f393','f37983','79a7f3','caf379','f379ee','79f3d4','f3b179','8d79f3','88f379','f379ac','79cff3','f3f379','cf79f3','79f3ac','f38879','798df3','b1f379','f379d4','79f3ee','f3ca79','a779f3','79f383','f37993','79b6f3','daf379','e879f3']
 table_match, table_key_s = podschet_slov()
 for ddd in sorted(kol):
    nado_mesta = int(kol.get(ddd))
  #print nado_mesta
  #if schet_diagname != (kol.get(ddd)):
  #placeNewLayer (double x, double y, double width, double height, const std::string &name)=0
  #lll = grt.root.wb.doc.physicalModels[0].diagrams[1].placeNewLayer(schet_x,schet_y,schet_width,schet_height,kol.get(ddd))
    schet_width =250; schet_height = 400;
    schet_width = schet_width * nado_mesta
    if nado_mesta > 3:
        schet_height = schet_height * nado_mesta / 2
    else:
        schet_height = schet_height * nado_mesta
    lll = grt.root.wb.doc.physicalModels[0].diagrams[1].placeNewLayer(schet_x,schet_y,schet_width,schet_height,ddd+' - Layer')
    lll.color = "#"+random.choice(colrs)
    ii= 0
    x_table = schet_x + 40; y_table = schet_y + 40;
    for table_key in sorted(table_key_s):
      if nado_mesta > ii:
        tables_uid = table_key_s[table_key]
        if len(tables_uid.columns) > 25: lll.height = 1050; #print len(tables_uid.columns);
        if len(tables_uid.columns) > 35: lll.height = 1550; #print len(tables_uid.columns);
        grt.root.wb.doc.physicalModels[0].diagrams[1].placeTable(tables_uid, x_table, y_table)
        x_table = x_table + 210; #y_table = schet_y + 40;
        #print "nado_mesta ", nado_mesta, "table_KEY =",table_key,"=>", tables_uid.tableEngine,'type OF tables_uid',tables_uid.name
        table_key_s.pop(table_key)
        ii = ii +1
    schet_x = schet_x + schet_width + 50
    if schet_x > 7300:
        schet_x = 20
        schet_y = schet_y + schet_height + 350
  #schet_diagname = kol.get(ddd)
 return 0

def print_table(nado_mesta):
 kol = podschet_kol()
 kol_tabl = podschet_kol_tabl()
 table_match, table_key_s = podschet_slov()
 for ddd in sorted(kol):
   #if nado_mesta if locals():
    nado_mesta = int(kol.get(ddd))
    print "nado_mesta=", nado_mesta, " |  ddd=", ddd
    ii= 0
    for table_key in sorted(table_key_s):
      if nado_mesta > ii:
        tables_uid = table_key_s[table_key]
        print "_KEY =",table_key,"=>", tables_uid.tableEngine,'type OF tables_uid',tables_uid.name
        table_key_s.pop(table_key)
        ii = ii +1
 return 0


add_new_diagram()
add_new_layer()

