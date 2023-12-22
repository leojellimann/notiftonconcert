# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 00:11:31 2022

@author: Léo
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
import logging.config
from datetime import datetime

from string import Template
from email.message import EmailMessage
import ssl
import smtplib
import pymysql

config = {
  'user': 'root',
  'password': 'root',
  'host': 'localhost:3306',
  'database': 'inventory',
  'raise_on_warnings': True,
}

connection = pymysql.connect(host="localhost:3306", user="root", password="root",database="notif_ton_concert")
cursor = connection.cursor()
retrive = "Select * from notiftonconcert;"
cursor.execute(retrive)
rows = cursor.fetchall()
for row in rows:
   print(row)


#commiting the connection then closing it.
connection.commit()
connection.close()


#email_password = 'stresbdlbkesupwg'

#non disponibles
#url = 'https://www.seetickets.com/fr/ap/event/orelsan/zenith-de-strasbourg-europe/25085'
#disponible
#url = 'https://www.seetickets.com/fr/ap/event/orelsan/paris-la-defense-arena/32125'
#complet
#url = 'https://www.seetickets.com/fr/ap/event/orelsan/le-dome/25079'


"""   
def getartist2():
    #search = input("Entrez l'artiste qui vous intéresse: ")
    try:
        #response = requests.get(f'https://www.seetickets.com/fr/search?q={search}')
        response = requests.get('https://www.seetickets.com/fr/search?q=orelsan')
        #print(f'https://www.seetickets.com/fr/search?q={search}')
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')
            li = soup.findAll('div')#div84 li[84]
            l = li[84]
            #liste = l.findAll('span')
            liste = l.findAll(class_='g-blocklist-sub-text')
            #print(liste)
            #place = liste[0].text
            #goodplace = place.split("\r\n")
            #showplace = goodplace[1]
            #print(showplace)
            location = []
            keeplocation = []
            for var in liste:
                listtotext = var.text
                #print(listtotext)
                getarrayloc = listtotext.split("\r\n")
                print(getarrayloc)
                removeextraponctuation = getarrayloc[1].replace('                                       \n', '')
                #li = removeextraponctuation.splitlines()
                #print(listtotext)
                #print(type(removeextraponctuation))
                #getfinallocdate = removeextraponctuation.split(', ', '')
                #print(removeextraponctuation)
                
                #keeplocation.append(getarray[1])
                #location.append(keeplocation)
                #print(keeplocation)
                #print(type(removeextraponctuation))
                #finallocdate = removeextraponctuation.split(', ', '')
                #print(finallocdate)
    except ValueError:
        print(ValueError)
"""
"""
def isavailable2(url):
    try:
        print(url)
        response = requests.get(url)
        if response.ok:
            #print('response ok')
            #soup = BeautifulSoup(response.text, 'lxml')
            soup = BeautifulSoup(response.text, 'lxml')
            #section = soup.findAll('section') A garder pour liste des artistes
            div = soup.findAll('div')
            gooddiv = div[80]#IndexError: list index out of range
            available = gooddiv.find('p').text
            #MESSAGE D'ERREUR AttributeError: 'NoneType' object has no attribute 'text'
            print(available)#80
            return available
    except ValueError:
        print("Pas de billets disponibles pour l'instant")
        #print(ValueError)
"""


def getartist(artist):
    try:
        response = requests.get(f'https://www.seetickets.com/fr/search?q={artist}')
        #response = requests.get('https://www.seetickets.com/fr/search?q=orelsan')
        #print(f'https://www.seetickets.com/fr/search?q={search}')
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')
            #scripts = str(soup.findAll('script')[26])#div84 li[84]
            
            #Mieux gérer la récupération de l'état des billets dispos
            
            
            scripts = str(soup.findAll('script', {'type': 'application/ld+json'}))
            raw_data = scripts.replace('[<script type="application/ld+json">', '').replace('\n            ', '').replace('\r', '').replace('\n        </script>]', '')
            jsondata = json.loads(raw_data)
            #print(jsondata[0]['location']['name'])
            data = []
            url = []
            for var in range(len(jsondata)):
                data.append(jsondata[var]['location']['name'] + " " + jsondata[var]['endDate'])
                url.append('https://www.seetickets.com' + jsondata[var]['url'])
                print(data[var])
                #print(url[var])
            search = input("Entrez le lieu qui vous intéresse: ")
            location = int(search)
            print("Vous avez sélectionné le concert à : " + data[location-1])
            print ("   ")
            print("Vous serez informé quand une place sera disponible pour ce concert")
            return url[location-1]
    except ValueError:
        print(ValueError)
    
def isavailable(url):
    try:
        response = requests.get(url)
        if response.ok:
            essai = 0
            notfound = 0
            found = 0
            while essai < 3 and found == 0:
                soup = BeautifulSoup(response.text, 'lxml')
                scripts = str(soup.findAll('script', {'type': 'application/ld+json'}))
                if len(scripts) > 2:#Cas évenement introuvable ou autre erreur
                    raw_data = scripts.replace('<script type="application/ld+json">','').replace('</script>', '')
                    jsondata = json.loads(raw_data)
                    stateavailability = []
                    available = 0
                    for var in range(len(jsondata)):
                        try:
                            stateavailability.append(jsondata[var])
                            available = available + len(stateavailability[var]['offers'])
                            if var == len(jsondata)-1 and available != 0:
                                print("Fonce acheter un billet")
                                found = 1
                            elif var == len(jsondata)-1 and available == 0:#doesn't display if no offers found
                                print("Pas de billets disponibles pour le moment")
                                
                        except :#normal -> case of the first applicationjson script that doesn't render the availability
                            #print("Le premier script n'a pas la donnée availability")
                            essai = essai + 1
                            #print(ValueError)
                else: 
                    print('Impossible de trouver l\'état de vente des billets pour cette page')
                    essai = essai + 1
                    notfound = 1
                
            if essai >= 3 and notfound == 1 and found == 0:
                print("Impossible de trouver l'évenement demandé")
            elif essai >= 3 and notfound == 0 and found == 0:
                print("Pas de billets disponibles pour le moment")
            #•elif found == 1:
                #print("Fonce acheter ton billet")
                    
    except ValueError:
        print(ValueError)


        
def sendemail(url):
    #envoi mail
    email_sender = 'testinfoleo@gmail.com'
    email_password = 'stresbdlbkesupwg'
    email_receiver = 'leo.jellimann@gmail.com'
    subject = "Une place de concert est disponible"
    body = f"Fonce acheter ton billet pour voir Orelsan à Strasbourg sur le lien : {url}"
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        
        
#main program
f = open("bddsimu.txt", "r")
artist = []
location = []
email = []
for x in f:
    print(len(x))
    #artist.append(x)
#print(artist[2])
#urlconcert = getartist(artist)
i = 0
"""while i < 3: 
    
    availability = isavailable(urlconcert)
    print("en attente de la prochaine demande")
    time.sleep(3)
    print("on reesaye un coup")
    i = i + 1

"""
"""
urlconcert = getartist()
       
availability = isavailable(urlconcert)
#print(availability)  
if availability == 'Complet':
    print("Le concert est complet")
elif availability == 'Billets non disponibles':
    print("Vous serez informés lors de la sortie de nouveaux billets")
elif availability == 'Des frais de transaction d\'un montant de 1,45€ seront appliqués. Si vous achetez cinq billets, vous ne paierez qu\'une fois les frais de réservation. ':
    print("De nouvelles places de concert sont disponibles pour votre concert")
    #sendemail()
elif availability == 'None':
    while True:
        print("Erreur lors de la réception du statut des places de concert")
        availability = isavailable(urlconcert)
        if availability != 'None':
            break
"""        
       
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
"""
    for d in body:    
        div = d.findAll('div')
    print(len(div))#§85/323
    print(div[40])
    #print(div)
    #réponse peut être "Service Busy"
    #script = str(soup.findAll('script', {'type': 'application/ld+json'})[1])
    #print(script)

"""
    
    



#PROGRAMME FONCTIONNE SEETICKETS
"""    
driver = webdriver.Chrome(executable_path=r'D:\OneDrive\Documents\Projets perso\Scrapping\ticket orelsan\chromedriver.exe')
driver.maximize_window()
test = 0
while test != 'ok':
    print("test ", test)
    test = test + 1
    
    #exemple seetickets
    driver.get(url)
    #exemple complet
    #driver.get('https://www.seetickets.com/fr/ap/event/orelsan/zenith-arena/25074')
    
    #Erreur temporaire
    #xpath erreur temporaire : Erreur temporaire /html/body/main/div[3]/div/h1 /html/body/main/div[3]/div/h1/text()
    
    
    #select artist
    
    #ticket master
    #https://www.ticketmaster.fr/fr/resultat?ipSearch=orelsan
    #xpath city /html/body/div[1]/div[1]/span/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/article/div/div[2]/div[1]/div/p[1]/a
    
    #Seetickets
    #https://www.seetickets.com/fr/search?q=damso
    #xpath city /html/body/main/div[4]/div/div/div[2]/div/div/div/ul/li[1]/article/a/span[1]
    
    
    
    try:
        result = driver.find_element_by_xpath("/html/body/main/div[4]/div[2]/div/div[2]/section[1]/div/div/p").text
        if len(result) > 0:
            if result == 'Billets non disponibles':
                print("Billets non disponibles")
                print(body)
            elif result == 'Complet':
                print("Concert complet")
                test = 'ok'
                driver.close()
        else:
            print("Fonce acheter tes billets")#c'est pas celui là qui est pris en compte
            test = 'ok'
            driver.close()
    except :
        print("Fonce acheter tes billets")
        test = 'ok'
        driver.close()
        
        #envoi mail
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
                
    time.sleep(5)    
    print("fin de la tempo")
    if test != 'ok':
        driver.refresh()
        print("fenêtre rafraichie")
    #get inspecter l'élément du site quand on a envoyé la notif pour vérifier 
    #que y'avait bien des places dispos
    #serverTime: get sa valeur pour être sûr de l'heure de l'envoi de la notif
    #converter avec : https://www.epochconverter.com/
   
"""
