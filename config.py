# -*- coding: utf-8 -*-
MAIL_HOST = 'smtp.gmail.com' # if you want to use gmail
MAIL_PORT = 587
MAIL_USERNAME = 'your.name@gmail.com'
MAIL_PASSWORD = 'yourpass'

EMAILS = {
    'Pierre': 'pierre@test.com',
    'Marie': 'marie@test.com',
    'Jean': 'jean@test.com',
    'Claire': 'claire@test.com',
}
    
COUPLES = (('Pierre','Marie'),('Jean',),('Claire',))
SENDER = '"Le Père-Noël" <yourmail@test.com>'

CONTENT = """Cher(e) {mail_receiver},

Cette année j'ai eu la chance d'échapper à la grippe de l'année dernière,
cependant j'ai pris un peu de retard dans mon travail. Comme je sais que dans
votre famille vous êtes toujours prêts à aider et que vous aimez beaucoup faire
les magasins, j'ai demandé à mes lutins de confectionner un petit logiciel pour
répartir les rôles entre vous sans que personne ne sache qui offre à qui.
Eh oui, c'est qu'ils se mettent à l'informatique mes lutins !

Je serais donc ravi si tu pouvais m'aider pour offrir un cadeau à {gift_receiver}.

Ah oui, aussi, envoie-moi vite ta liste !
Allez ! Bybye !

Le Père-Noël.
"""
