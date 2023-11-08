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
from datetime import date

from string import Template
from email.message import EmailMessage
import ssl
import smtplib
import pymysql

import mysql.connector
from mysql.connector import Error
import psycopg2


def getdata():
    try:
        # Établir la connexion à la base de données
        connection = psycopg2.connect(
        user="SQLadmin",
        password="password",
        host="host-001.eu.clouddb.ovh.net",
        port="35900",
        database="notiftonconcert"
    )
        if connection:
            cursor = connection.cursor()
            print("Nouveau test en cours\n")
            print("Tu es connecté à la base de données")
            
            #get number of rows with date
            mysql_get_nbenddate_query = "SELECT COUNT(end_date) FROM infosnotif WHERE notifsent = FALSE"
            cursor.execute(mysql_get_nbenddate_query)
            nbdates = cursor.fetchone()
            sizedates = nbdates[0]
            print(f"Il y a {sizedates} lignes à vérifier sans notif envoyée et avec la date à jour\n")
            
            #get dates where notifsent = 0
            #check if enddate is passed
            today = date.today()
            todayyear = today.strftime("%Y")
            todaymonth = today.strftime("%m")
            todayday = today.strftime("%d")
            actualday = int(todayyear+todaymonth+todayday)#actual date in number ex: 20221109 for 9 november 2022
            #print("today: ", actualday)
            
            mysql_get_enddate_query = "SELECT artist, email, end_date, id FROM infosnotif WHERE notifsent = FALSE"
            cursor.execute(mysql_get_enddate_query)
            alldates = cursor.fetchall()
            #print(alldates)
            ids = [lis[-1] for lis in alldates]#get each id value
            enddate = [lis[-2] for lis in alldates]#get each date value
            emails = [lis[-3] for lis in alldates]#list of emails
            artists = [lis[-4] for lis in alldates]#list of artists
            
            #compare actual date and enddate of concert
            for var in range(sizedates):
                datestring = enddate[var]
                idvalue = ids[var]
                day, month, year = datestring.split()
                enddatenumber = int(year+month+day)
                #print(enddatenumber)
                
                if enddatenumber < actualday :#set notifsent = 1 if date passed
                    mysql_post_notifsent_query = f"DELETE FROM infosnotif where ID = {idvalue}"
                    cursor.execute(mysql_post_notifsent_query)
                    connection.commit()
                    if cursor.rowcount == 1:
                        print(f"La date est dépassée. On a supprimé de la base de données l'id ", idvalue)
                        #print(ids[var])
                        #print(enddate[var])
                        #print(emails[var])
                        #print(artists[var])
                        #sendemaillate(emails[var], artists[var])
            
            
            mysql_get_sizerows_query = "SELECT COUNT(ID) FROM infosnotif WHERE notifsent = FALSE"
            mysql_get_rows_query = "SELECT email, url, id FROM infosnotif WHERE notifsent = FALSE"
            cursor.execute(mysql_get_sizerows_query)
            sizerows = cursor.fetchone()
            cursor.execute(mysql_get_rows_query)
            nbrows = cursor.fetchall()
            sizerequest = sizerows[0]#render total number of ids/rows with notifsent = 0
            ids = [lis[-1] for lis in nbrows]#ids of the ids with notifsent = 0
            url = [lis[-2] for lis in nbrows]#list of all url
            emails = [lis[-3] for lis in nbrows]#list of emails
            artists = [lis[-4] for lis in alldates]#list of artists
           # print(ids[25])
            #print(url[25])
            #print(emails[25])
            #Check if new tickets are available
            for x in range(sizerequest):
                print(f"\nVérification disponibilité numéro: {x+1}. Id de la base de données numéro : {ids[x]}")
                time.sleep(2)
                isavailable(url[x], emails[x], connection, cursor, ids[x], artists[x])
            #isavailable(url[25], emails[25], connection, cursor, ids[25])    
    
    except Error as e:
        print("Error while connecting to PostGreSQL", e)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("\n\nFermeture de la connexion avec la base de données\n\n")


def isavailable(url, email, connection, cursor, ids, artist):
    essai = 0
    notfound = 0
    found = 0
    try:
        response = requests.get(url)
        if response.ok:
            
            while essai < 3 and found == 0:#loop several times in case impossible to get html code of the page
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
                            #print("statut de dispo : ", stateavailability)
                            if 'offers' in stateavailability[var]:#to check if there is 'offers' in the string. If not in every string then no tickets available
                                available = available + len(stateavailability[var]['offers'])
                                #print("dispo : ", available)
                            if available != 0:
                                print("Fonce acheter un billet : ", ids)
                                found = 1
                                mysql_post_notifsent_query = f"UPDATE infosnotif set notifsent = TRUE where ID = {ids}"
                                cursor.execute(mysql_post_notifsent_query)
                                connection.commit()
                                
                                if cursor.rowcount == 1:
                                    print(f"email envoyé à {email}")
                                    sendemail(url, email, artist)
                                break
                            elif var == len(jsondata)-1 and available == 0:#doesn't display if no offers found
                                print("Le concert est toujours complet pour le moment !")
                                essai=3#essai = 3 to break the whileesai < 3 condition
                                
                        except ValueError:#normal -> case of the first applicationjson script that doesn't render the availability
                            #print("Le premier script n'a pas la donnée availability")
                            essai = essai + 1
                            print(ValueError)
                else: 
                    print('Impossible de trouver l\'état de vente des billets pour cette page')
                    essai = essai + 1
                    notfound = 1
                    response = requests.get(url)
                    
                if essai >= 3 and notfound == 1 and found == 0:
                    print("Impossible de trouver l'évenement demandé")
                #elif essai >= 3 and notfound == 0 and found == 0:
                    #print("Pas de billets disponibles pour le moment")
                #•elif found == 1:
                    #print("Fonce acheter ton billet")
                    
    except ValueError:
        print(ValueError)


        
def sendemail(url, email, artist):
    #envoi mail
    email_sender = 'email@gmail.com'
    email_password = 'password'
    email_receiver = email
    
    subject = "notiftonconcert | UNE PLACE EST DISPO !"
    body = f"Salut chef !\n\n\nDe nouvelles places sont dispo pour le concert de "+artist+" pour lequel tu t'es inscrit.\n\nViens vite réserver ta place sur : "+url+"\n\nN'hésite pas à nous dire ce que t'as pensé de notiftonconcert en réponse à ce mail.\n\n\nAu plaisir de te revoir parmi notiftonconcert.fr :)"

    

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

while 1:
    getdata()
    time.sleep(100)
