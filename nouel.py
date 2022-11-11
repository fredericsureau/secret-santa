#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random
import smtplib
import yaml
import copy
from email.message import EmailMessage

def getcases(possibilities, remaining=None):
    if not possibilities:
        return [[]]

    if remaining is None:
        remaining = list(possibilities)

    possibilities = copy.deepcopy(possibilities)
    person, candidates = possibilities.popitem()
    candidates.intersection_update(remaining)
    
    allcases = []
    for candidate in candidates:
        remaining_copy = remaining.copy()
        remaining_copy.remove(candidate)
        subcases = getcases(possibilities, remaining_copy)
        cases = [[(person, candidate)] + subcase for subcase in subcases]
        allcases += cases

    return allcases

def main(config_file="config.yml"):
    with open(config_file) as f:
        config = yaml.safe_load(f)
    
    participants = config["participants"]
    exclusions = config.get("exclusions", {}).get("simple", {})
    mutual_exclusions = config.get("exclusions", {}).get("mutual", [])
    
    # Add mutual exclusions to simple exclusions list
    for group in mutual_exclusions:
        for p in group:
            exclusions.setdefault(p, []).extend(group)

    possibilities = {}
    for p in list(participants):
        possibilities[p] = set(participants)
        possibilities[p].difference_update({p}, exclusions.get(p, {}))

    cases = getcases(possibilities)
    
    print(len(cases), "cas possibles")
    
    case = random.choice(cases)
    
    sender = config.get("email").get("sender")
    
    message = EmailMessage()
    message['From'] = sender
    message['To'] = sender
    message['Subject'] = config.get("email").get("subject")

    server = smtplib.SMTP(config.get("smtp").get("host"), config.get("smtp").get("port"))
    server.starttls()
    server.login(config.get("smtp").get("username"), config.get("smtp").get("password"))

    content = config.get("email").get("content")

    for mail_receiver, gift_receiver in case:
        recipient = participants[mail_receiver]
        message.replace_header('To', recipient)
        message.set_content(content.format(mail_receiver=mail_receiver, gift_receiver=gift_receiver), charset="UTF-8")

        server.sendmail(sender, [recipient], message.as_string())
        print(mail_receiver, "→", gift_receiver)

    server.quit()

if __name__ == '__main__':
    main(*sys.argv[1:])

