#!/usr/bin/env python

file = open("alunos_jan.txt", "r");
lista = {};
cont = 0;
for line in file: 
	separate = line.split("\t");
	year = separate[10].split("/");
	evasao = separate[12].split("/");

	listIngresso = { };


	if len(year) > 1:
		ingresso = str(year[0].strip()) + "," + str(year[1].strip());
		#print "%s" % ingresso

		if (ingresso in listIngresso):
			listIngresso[ingresso] = listIngresso[ingresso] + 1;
		else:
			listIngresso[ingresso] = 0;

	#yearString = year[0] + year[1];
	

for ingresso in listIngresso: 
	print "%s" % (ingresso);

	#if len(year) > 1:
		#print str(year[0].strip()) + str(year[1].strip());
		#print "%s : %s" % (year[0], year[1]);
	
#	for ano in year: 
#		print "%s" % ano.strip();

	