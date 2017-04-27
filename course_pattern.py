#!/usr/bin/env python

import codecs
from datetime import datetime

def calculaIdade(nascimento, ingresso):
    return ingresso.year - nascimento.year - ((ingresso.month, ingresso.day) < (nascimento.month, nascimento.day))

file = codecs.open('./base/alunos_jan.txt', encoding='utf-8')

#file = open("./base/alunos_jan.txt", "r");
list = { };
cont = 0;
listAdmission = { };

dictStatus = { 'Sem Evaso': 'semevasao', 'Desistente': 'desistente', 'Cancelamento Cota': 'cancelamento', 'Formado': 'formado', 'Jubilado (Crit. 01)': 'jubilado 01', 'Jubilado (Crit. 02)': 'jubilado 02', 'Transferido': 'transferido', 'Excludo': 'excluido' };
dictStatusWhiteList = { 'Desistente': 'desistente', 'Cancelamento Cota': 'cancelamento', 'Formado': 'formado', 'Jubilado (Crit. 01)': 'jubilado 01', 'Jubilado (Crit. 02)': 'jubilado 02', 'Transferido': 'transferido', 'Excludo': 'excluido' };

dictCourse = { 'Sistemas de Informao': 'Sistemas de Informacao', 'Cincia da Computao': 'Ciencia da Computacao' };
dictSexo = { 'M': 'Masculino', 'F': 'Feminino' };
dictSexoDefault = { 'M': 0, 'F': 0 };

for line in file: 
	separateFields = line.split("\t");

	year = separateFields[10].split("/");
	evasao = separateFields[11].strip().split(" ");

	if (len(evasao)) :
		evasao = evasao[0]

	reason = separateFields[5].encode('ascii','ignore');
	course = separateFields[7].encode('ascii','ignore');
	sexo = separateFields[2].encode('ascii','ignore');
	nascimento = separateFields[3].strip().split(" ");

	if (len(nascimento) > 0):
		nascimento = nascimento[0];

	if len(year) > 1:
		year[0] = year[0].encode('ascii','ignore');
		year[1] = year[1].encode('ascii','ignore');
		year[1] = str(year[1].strip().replace(" ", "+").replace("", "").lower());

		mesentrada = "01";

		if (year[1].split("+")[0] == 2) :
			mesentrada = "06";

		stringresso = "01/" + mesentrada + "/" + year[0];

		anoingresso = datetime.strptime(stringresso, '%d/%m/%Y');
		aniversario = datetime.strptime(nascimento, '%d/%m/%Y');
		idade = calculaIdade(aniversario, anoingresso);

		admission = str(year[0].strip()) + "," + str(year[1].strip()) + "," + dictCourse[course];

		if (admission in listAdmission):
			listAdmission[admission]['ingressantes'][sexo] += 1;
		else:
			listAdmission[admission] = { 'ingressantes' : { 'M': 0, 'F': 0, 'idade': [] }, 'semevasao' : { 'M': 0, 'F': 0, 'idade': [] }, 'desistente' : { 'M': 0, 'F': 0, 'idade': [] }, 'cancelamento' : { 'M': 0, 'F': 0, 'idade': [] }, 'formado' : { 'M': 0, 'F': 0, 'idade': [], 'tempo' : [] }, 'jubilado 01' : { 'M': 0, 'F': 0, 'idade': [] }, 'jubilado 02' : { 'M': 0, 'F': 0, 'idade': [] }, 'transferido' : { 'M': 0, 'F': 0, 'idade': [] }, 'excluido' : { 'M': 0, 'F': 0, 'idade': [] } };
			listAdmission[admission]['ingressantes'][sexo] = 1;

		listAdmission[admission]['ingressantes']['idade'].append(idade);

		if (reason in dictStatus) :
			listAdmission[admission][dictStatus[reason]][sexo] +=  1;

			if (dictStatus[reason] is 'formado' and len(evasao) > 0): 
				anoegresso = datetime.strptime(evasao, '%d/%m/%Y');
				anoingresso = datetime.strptime(stringresso, '%d/%m/%Y');
				formacao = calculaIdade(anoingresso, anoegresso);

				listAdmission[admission][dictStatus[reason]]['tempo'].append(formacao);

		if (reason in dictStatusWhiteList and len(separateFields[11]) > 0):
			anoegresso = datetime.strptime(evasao, '%d/%m/%Y');
			aniversario = datetime.strptime(nascimento, '%d/%m/%Y');
			idade = calculaIdade(aniversario, anoegresso);
			listAdmission[admission][dictStatus[reason]]['idade'].append(idade);

for admission in listAdmission: 
	turma = admission.split(",");
	
	turmaAno = turma[0];
	semestreAno = turma[1].replace("+", "o ");
	cursoAno = turma[2];

	ingressantes = (listAdmission[admission]['ingressantes']['M'] + listAdmission[admission]['ingressantes']['F']);
	print "\n\n%s\n" % (turmaAno + " - " + semestreAno + " - " + cursoAno + " - " + str(ingressantes) + " ingressante(s)");	
	#print "\n%s\n\n" % (listAdmission[admission]);	
	print "Relacoes: ";

	print "\nHomens: %i" % (listAdmission[admission]['ingressantes']['M']);	
	print "Mulheres: %i" % (listAdmission[admission]['ingressantes']['F']);	
	print "Media idade: %.2f anos" % (sum(listAdmission[admission]['ingressantes']['idade']) / float(ingressantes));

	# Formados
	formado = listAdmission[admission]['formado']['M'] + listAdmission[admission]['formado']['F'];

	if (formado > 0):
		print "\nFormado/Ingresso (%i):  %.2f" % (formado, (formado * 100)/ ingressantes);	
		print "Media idade: %.0f anos" % (sum(listAdmission[admission]['formado']['idade']) / float(formado));
		print "Media tempo formacao: %.2f anos" % (sum(listAdmission[admission]['formado']['tempo']) / float(len(listAdmission[admission]['formado']['tempo'])));
	
		if (listAdmission[admission]['formado']['M'] > 0) :
			print "Formado/Ingresso H (%i):  %.2f" % (listAdmission[admission]['formado']['M'], (listAdmission[admission]['formado']['M'] * 100)/ float(ingressantes));
		else: 
			print "Formado/Ingresso H: 0";

		if (listAdmission[admission]['formado']['F'] > 0) :
			print "Formado/Ingresso M (%i):  %.2f" % (listAdmission[admission]['formado']['F'], (listAdmission[admission]['formado']['F'] * 100)/ float(ingressantes));
		else: 
			print "Formado/Ingresso M: 0";


	# Sem evasao
	semevasao = listAdmission[admission]['semevasao']['M'] + listAdmission[admission]['semevasao']['F'];

	if (semevasao > 0):
		print "\nSem Evasao/Ingresso (%i):  %.2f" % (semevasao, (semevasao * 100)/ float(ingressantes));

		if (listAdmission[admission]['semevasao']['M'] > 0) :
			print "Sem Evasao/Ingresso H (%i):  %.2f" % (listAdmission[admission]['semevasao']['M'], (listAdmission[admission]['semevasao']['M'] * 100)/ float(ingressantes));
		else: 
			print "Sem Evasao/Ingresso H: 0";

		if (listAdmission[admission]['semevasao']['F'] > 0) :
			print "Sem Evasao/Ingresso M (%i):  %.2f" % (listAdmission[admission]['semevasao']['F'], (listAdmission[admission]['semevasao']['F'] * 100)/ float(ingressantes));
		else: 
			print "Sem Evasao/Ingresso M: 0";


	# Jubilados Cond 01
	jubilados1 = listAdmission[admission]['jubilado 01']['M'] + listAdmission[admission]['jubilado 01']['F'];

	if (jubilados1 > 0):
		print "\nJubilado 01/Ingresso (%i):  %.2f" % (jubilados1, (jubilados1 * 100)/ float(ingressantes));

		if (jubilados1 > 1):
			print "Media idade: %.0f anos" % (sum(listAdmission[admission]['jubilado 01']['idade']) / float(jubilados1));
			print "Mais velho: %.0f anos" % (max(listAdmission[admission]['jubilado 01']['idade']));
			print "Mais novo: %.0f anos" % (min(listAdmission[admission]['jubilado 01']['idade']));				
	
		if (listAdmission[admission]['jubilado 01']['M'] > 0) :
			print "Jubilado 01/Ingresso H (%i):  %.2f" % (listAdmission[admission]['jubilado 01']['M'], (listAdmission[admission]['jubilado 01']['M'] * 100)/ float(ingressantes));
		else: 
			print "Jubilado 01/Ingresso H: 0";		

		if (listAdmission[admission]['jubilado 01']['F'] > 0) :
			print "Jubilado 01/Ingresso M (%i):  %.2f" % (listAdmission[admission]['jubilado 01']['F'], (listAdmission[admission]['jubilado 01']['F'] * 100)/ float(ingressantes));
		else: 
			print "Jubilado 01/Ingresso M: 0";	

	
	# Jubilados Cond 02
	jubilados2 = listAdmission[admission]['jubilado 02']['M'] + listAdmission[admission]['jubilado 02']['F'];

	if (jubilados2 > 0):
		print "\nJubilado 02/Ingresso (%i):  %.2f" % (jubilados2, (jubilados2 * 100)/ float(ingressantes));

		if (jubilados2 > 1):
			print "Media idade: %.0f anos" % (sum(listAdmission[admission]['jubilado 02']['idade']) / float(jubilados2));
			print "Mais velho: %.0f anos" % (max(listAdmission[admission]['jubilado 02']['idade']));
			print "Mais novo: %.0f anos" % (min(listAdmission[admission]['jubilado 02']['idade']));		

		if (listAdmission[admission]['jubilado 02']['M'] > 0) :
			print "Jubilado 02/Ingresso H (%i):  %.2f" % (listAdmission[admission]['jubilado 02']['M'], (listAdmission[admission]['jubilado 02']['M'] * 100)/ float(ingressantes));
		else: 
			print "Jubilado 02/Ingresso H: 0";		

		if (listAdmission[admission]['jubilado 01']['F'] > 0) :
			print "Jubilado 02/Ingresso M (%i):  %.2f" % (listAdmission[admission]['jubilado 02']['F'], (listAdmission[admission]['jubilado 02']['F'] * 100)/ float(ingressantes));
		else: 
			print "Jubilado 02/Ingresso M: 0";	

	# Excluido
	excluido = listAdmission[admission]['excluido']['M'] + listAdmission[admission]['excluido']['F'];

	if (excluido > 0):
		print "\nExcluido/Ingresso (%i):  %.2f" % (excluido, (excluido * 100)/ float(ingressantes));

		if (excluido > 1):
			print "Media idade: %.0f anos" % (sum(listAdmission[admission]['excluido']['idade']) / float(excluido));
			print "Mais velho: %.0f anos" % (max(listAdmission[admission]['excluido']['idade']));
			print "Mais novo: %.0f anos" % (min(listAdmission[admission]['excluido']['idade']));		

		if (listAdmission[admission]['excluido']['M'] > 0) :
			print "Excluido/Ingresso H (%i):  %.2f" % (listAdmission[admission]['excluido']['M'], (listAdmission[admission]['excluido']['M'] * 100)/ float(ingressantes));
		else: 
			print "Excluido/Ingresso H: 0";		

		if (listAdmission[admission]['excluido']['F'] > 0) :
			print "Excluido/Ingresso M (%i):  %.2f" % (listAdmission[admission]['excluido']['F'], (listAdmission[admission]['excluido']['F'] * 100)/ float(ingressantes));
		else: 
			print "Excluido/Ingresso M: 0";				

	# Desistente
	desistente = listAdmission[admission]['desistente']['M'] + listAdmission[admission]['desistente']['F'];

	if (desistente > 0):
		print "\nDesistente/Ingresso (%i):  %.2f" % (desistente, (desistente * 100)/ float(ingressantes));			

		if (desistente > 1):
			print "Media idade: %.0f anos" % (sum(listAdmission[admission]['desistente']['idade']) / float(desistente));
			print "Mais velho: %.0f anos" % (max(listAdmission[admission]['desistente']['idade']));
			print "Mais novo: %.0f anos" % (min(listAdmission[admission]['desistente']['idade']));
		
		if (listAdmission[admission]['desistente']['M'] > 0) :
			print "Desistente/Ingresso H (%i):  %.2f" % (listAdmission[admission]['desistente']['M'], (listAdmission[admission]['desistente']['M'] * 100)/ float(ingressantes));
		else: 
			print "Desistente/Ingresso H: 0";		

		if (listAdmission[admission]['desistente']['F'] > 0) :
			print "Desistente/Ingresso M (%i):  %.2f" % (listAdmission[admission]['desistente']['F'], (listAdmission[admission]['desistente']['F'] * 100)/ float(ingressantes));
		else: 
			print "Desistente/Ingresso M: 0";		


	# Transferido
	transferido = listAdmission[admission]['transferido']['M'] + listAdmission[admission]['transferido']['F'];

	if (transferido > 0):
		print "\nTransferido/Ingresso (%i):  %.2f" % (transferido, (transferido * 100)/ float(ingressantes));	

		if (transferido > 1):
			print "Media idade: %.0f anos" % (sum(listAdmission[admission]['transferido']['idade']) / float(transferido));
			print "Mais velho: %.0f anos" % (max(listAdmission[admission]['transferido']['idade']));
			print "Mais novo: %.0f anos" % (min(listAdmission[admission]['transferido']['idade']));		
		
		if (listAdmission[admission]['transferido']['M'] > 0) :
			print "Transferido/Ingresso H (%i):  %.2f" % (listAdmission[admission]['transferido']['M'], (listAdmission[admission]['transferido']['M'] * 100)/ float(ingressantes));
		else: 
			print "Transferido/Ingresso H: 0";		

		if (listAdmission[admission]['transferido']['F'] > 0) :
			print "Transferido/Ingresso M (%i):  %.2f" % (listAdmission[admission]['transferido']['F'], (listAdmission[admission]['transferido']['F'] * 100)/ float(ingressantes));
		else: 
			print "Transferido/Ingresso M: 0";	
	

	# Cancelamento
	cancelamentos = listAdmission[admission]['cancelamento']['M'] + listAdmission[admission]['cancelamento']['F'];

	if (cancelamentos > 0):
		print "\nCancelamento/Ingresso (%i):  %.2f" % (cancelamentos, (cancelamentos * 100)/ float(ingressantes));	

		if (cancelamentos > 1):
			print "Media idade: %.0f anos" % (sum(listAdmission[admission]['cancelamento']['idade']) / float(cancelamentos));
			print "Mais velho: %.0f anos" % (max(listAdmission[admission]['cancelamento']['idade']));
			print "Mais novo: %.0f anos" % (min(listAdmission[admission]['cancelamento']['idade']));				

		if (listAdmission[admission]['cancelamento']['M'] > 0) :
			print "Cancelamento/Ingresso H (%i):  %.2f" % (listAdmission[admission]['cancelamento']['M'], (listAdmission[admission]['cancelamento']['M'] * 100)/ float(ingressantes));
		else: 
			print "Cancelamento/Ingresso H: 0";		

		if (listAdmission[admission]['transferido']['F'] > 0) :
			print "Cancelamento/Ingresso M (%i):  %.2f" % (listAdmission[admission]['cancelamento']['F'], (listAdmission[admission]['cancelamento']['F'] * 100)/ float(ingressantes));
		else: 
			print "Cancelamento/Ingresso M: 0";	


