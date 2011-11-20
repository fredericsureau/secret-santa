#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import smtplib
from email import message

#######################################################################
# Functions
#######################################################################

## Return a list of persons from a list of couples
def get_persons(couples):
	persons = []
	for couple in couples:
		persons += list(couple)
	
	return persons

## Find possibilities lists
# Creating the possibilities for each person
# possibilities[i] is all possibles persons for the i-eme person
def find_persons_possibilities(couples):
	possibilities = []
	for i in range(len(couples)):
		other_couples = couples[0:i] + couples[i+1:]
		other_persons = get_persons(other_couples)
		for j in range(len(couples[i])):
			possibilities.append(other_persons)
	
	return possibilities

## Finding all possible cases
def find_all_possible_cases(possibilities, index, persons_available):

	results = []

	for i in possibilities[index]:
		try:
			person_index = persons_available.index(i)
		
			if index == len(possibilities) - 1:
				#print 'In function : ', i
				tail = []
				tail.append(i)
				results.append(tail)
				
			else:
				remaining_persons = persons_available[0:person_index] + persons_available[person_index+1:]
				subpossibles = find_all_possible_cases(possibilities, index+1, remaining_persons)
				
				for j in subpossibles:
					j.insert(0, i)
					results.append(j)
			
		except ValueError:
			pass
	
	return results

## Let's do the santa claus' job !
def lets_do_santa_claus_job(couples):

	# Creating the possibilities for each person
	persons_possibilities = find_persons_possibilities(couples)

	# Identify all possible cases
	persons = get_persons(couples)

	possible_cases = find_all_possible_cases(persons_possibilities, 0, persons)

	random_case = random.choice(possible_cases)

	return random_case

#######################################################################
# Main routine
#######################################################################

# Define the emails and couples
# Only one sub-tuple level is supported

emails = dict()
emails['Pierre'] = 'pierre@test.com'
emails['Marie'] = 'marie@test.com'
emails['Jean'] = 'jean@test.com'
emails['Claire'] = 'claire@test.com'

couples = (('Pierre','Marie'),('Jean',),('Claire',))

# Find a random possible case

persons = get_persons(couples)

random_case = lets_do_santa_claus_job(couples)

# Send mails

sender = '"Le Père-Noël" <yourmail@test.com>'

content = """Cher(e) %s,

Cette année j'ai eu la chance d'échapper à la grippe de l'année dernière,
cependant j'ai pris un peu de retard dans mon travail. Comme je sais que dans
votre famille vous êtes toujours prêts à aider et que vous aimez beaucoup faire
les magasins, j'ai demandé à mes lutins de confectionner un petit logiciel pour
répartir les rôles entre vous sans que personne ne sache qui offre à qui.
Eh oui, c'est qu'ils se mettent à l'informatique mes lutins !

Je serais donc ravi si tu pouvais m'aider pour offrir un cadeau à %s.

Ah oui, aussi, envoie-moi vite ta liste !
Allez ! Bybye !

Le Père-Noël.
"""

print content

message = message.Message()
message.add_header('from',sender)
message.add_header('to','test@test.com')
message.add_header('subject','[Confidentiel] Message du Père-Noël')

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your.name@gmail.com','yourpass')

for i in range(len(persons)):
	recipients = emails[persons[i]]
	message.replace_header('to',recipients)
	message.set_payload(content % (persons[i], random_case[i]))

	server.sendmail(sender, [recipients], message.as_string())
	print persons[i], ' => ', random_case[i]

server.quit()

