"""
This program queries Craigslist for the paramets specified in housingQuery, then
sends an email with the results.
craigslist documentation: https://github.com/juliomalegria/python-craigslist
email documentation: http://naelshiab.com/tutorial-send-email-python/

"""

from craigslist import CraigslistHousing #use "pip install python-craigslist" to install module
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

count = 0
jsonData = '{"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}'
loadedJson = json.loads(jsonData)
queryResultsFile = open('craigslistRooms.json', 'w')
emailString = ''

queryResultsFile.truncate() # erases existing queryResultsFile content
housingQuery = CraigslistHousing(site='sfbay', area='sby', category='rooms-shares',
                         filters={'max_price': 800, 'min_price': 500,
                         'private_room': True, 'private_bath': True,
                         'has_image': True, 'search_distance': 1})

for result in housingQuery.get_results(sort_by='newest', geotagged=True):
    if count < 6: #TODO: use unicode length emailString < unicode 880
        print('making listing...')
        listing = result['name'] + '\n' + result['url'] + '\n\n'
        emailString += listing
        count += 1
    else:
        break


fromaddr = 'FROM EMAIL ADDRESS' #change to appropriate sender's email address
toaddr = 'TO EMAIL ADDRESS' #change to appropriate receiver's email address
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = 'CRAIGSLIST ROOMS FOR RENT'

msg.attach(MIMEText(emailString, 'plain'))
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, 'SENDERS EMAIL ACCOUNT PASSWORD') #change to include appropriate password
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()

queryResultsFile.close()
