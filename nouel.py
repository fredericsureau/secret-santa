#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
import smtplib
from email.message import Message

def get_persons(couples):
    """Return a list of persons from a list of couples"""
    persons = []
    for couple in couples:
            persons += list(couple)
    
    return persons

def find_persons_possibilities(couples):
    """ Find possibilities lists
    Creating the possibilities for each person
    possibilities[i] is all possibles persons for the i-eme person
    """
    possibilities = []
    for i in range(len(couples)):
        other_couples = couples[0:i] + couples[i+1:]
        other_persons = get_persons(other_couples)
        for j in range(len(couples[i])):
            possibilities.append(other_persons)
    
    return possibilities

def find_all_possible_cases(possibilities, index, persons_available):
    """Finding all possible cases"""

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
                remaining_persons = persons_available[0:person_index] \
                                    + persons_available[person_index+1:]

                subpossibles = find_all_possible_cases(possibilities, 
                        index+1, remaining_persons)
                    
                for j in subpossibles:
                    j.insert(0, i)
                    results.append(j)
                
        except ValueError:
            pass
    
    return results

def lets_do_santa_claus_job(couples):
    """Let's do the santa claus' job !"""

    # Creating the possibilities for each person
    persons_possibilities = find_persons_possibilities(couples)

    # Identify all possible cases
    persons = get_persons(couples)

    possible_cases = find_all_possible_cases(persons_possibilities, 0, persons)

    random_case = random.choice(possible_cases)

    return random_case

def read_config(filename):
    """Load a Python file into a dictionary.
    """
    context = {}
    if filename:
        tempdict = {}
        execfile(filename, tempdict)
        for key in tempdict:
            if key.isupper():
                context[key] = tempdict[key]
    return context

def main(config):
    """main routine"""
    # Define the emails and couples
    # Only one sub-tuple level is supported
    emails = config['EMAILS']
    couples = config['COUPLES']
    sender = config['SENDER']
    content = config['CONTENT']

    # Find a random possible case
    persons = get_persons(couples)
    random_case = lets_do_santa_claus_job(couples)

    # Send mails
    message = Message()
    message.add_header('from', sender)
    message.add_header('subject','[Confidentiel] Message du Père-Noël')
    message.add_header('to', sender)

    server = smtplib.SMTP(config['MAIL_HOST'], config['MAIL_PORT'])
    server.starttls()
    server.login(config['MAIL_USERNAME'], config['MAIL_PASSWORD'])

    for i in range(len(persons)):
        recipients = emails[persons[i]]
        message.replace_header('to', recipients)
        message.set_payload(content % (persons[i], random_case[i]))

        server.sendmail(sender, [recipients], message.as_string())
        print persons[i], ' => ', random_case[i]

    server.quit()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        fn = sys.argv[1]
    else:
        fn = "config.py"
    config = read_config(fn)
    main(config)
