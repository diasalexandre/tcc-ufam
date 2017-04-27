#!/usr/bin/env python

import codecs
file = codecs.open('./base/alunos_jan.txt', encoding='utf-8')

#file = open("./base/alunos_jan.txt", "r");
list = { };
cont = 0;
listAdmission = { };

dictStatus = { 'Sem Evaso': 'semevasao', 'Desistente': 'desistente', 'Cancelamento Cota': 'cancelamento', 'Formado': 'formado', 'Jubilado (Crit. 01)': 'jubilado 01', 'Jubilado (Crit. 02)': 'jubilado 02', 'Transferido': 'transferido', 'Excludo': 'excluido' };

for line in file: 
	separateFields = line.split("\t");

	year = separateFields[10].split("/");
	evasao = separateFields[12].split("/");

	reason = separateFields[5].encode('ascii','ignore');

	if len(year) > 1:
		year[0] = year[0].encode('ascii','ignore');
		year[1] = year[1].encode('ascii','ignore');

		year[1] = str(year[1].strip().replace(" ", "+").replace("", "").lower());

		admission = str(year[0].strip()) + "," + str(year[1].strip());

		if (admission in listAdmission):
			listAdmission[admission]['ingressantes'] = listAdmission[admission]['ingressantes'] + 1;
		else:
			listAdmission[admission] = { 'ingressantes'  : 1, 'semevasao' : 0, 'desistente' : 0, 'cancelamento' : 0, 'formado' : 0, 'jubilado 01' : 0, 'jubilado 02' : 0, 'transferido' : 0 , 'excluido' : 0 };

		if (reason in dictStatus) :
			listAdmission[admission][dictStatus[reason]] = listAdmission[admission][dictStatus[reason]] + 1;
		

for admission in listAdmission: 
	print "%s : %s" % (admission, listAdmission[admission]);	
	#print "Relação Ingresso/Formado:  %f" % listAdmission[admission]  (admission, listAdmission[admission]);