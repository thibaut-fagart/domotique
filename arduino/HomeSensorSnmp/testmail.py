#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
 
import smtplib
 
sender = 'dimitri@schugart.net'
receivers = ['lilou@schugart.net']
temperatureSeuil = 5
 
message = """From: Le Roux temperature <dimitri@schugart.net>
To: Le Roux User <lilou@schugart.net>
Subject: Alerte, temperature basse au Roux
 
La temperature d'une des 2 sondes interieur est passé sous le seuil de %i °C """%temperatureSeuil
 
try:
   smtpObj = smtplib.SMTP('mail.schugart.net')
   smtpObj.sendmail(sender, receivers, message)        
   print "Successfully sent email"
except SMTPException:
   print "Error: unable to send email"
