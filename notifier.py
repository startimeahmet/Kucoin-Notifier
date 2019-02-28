import smtplib, ssl
from kucoin.client import Client
import json
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# connect to production
client = Client("api_key", "api_secret", "passphrase")


def send_mail(filled_amount, filled_coin):
	print(filled_amount, filled_coin)
	port = 465  # For SSL
	smtp_server = "smtp.gmail.com"
	sender_email = "receipent_email@email.com"  # Enter your address
	receiver_email = "sender_email@email.com"  # Enter receiver address
	password = "your_email_password"
	
	msg = MIMEMultipart("")
	
	msg["Subject"] = "Kucoin order fill"
	msg["From"] = sender_email
	msg["To"] = receiver_email
	
	for i in range(len(filled_amount)):
		text = """\
A """ + filled_coin[i] + """ order got filled with amount """ + filled_amount[i] + """\n"""
		msg.attach(MIMEText(text, "plain"))

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, msg.as_string())

fill_ids = []

fills_list = client.get_fills()["items"]

for i in range(len(fills_list)):
	fill_ids.append(fills_list[i]["orderId"])

while True:
	print("i am running don't worry")
	
	filled_orders = []
	
	new_fill_ids = []
	new_fill_list = client.get_fills()["items"]
	
	for i in range(len(new_fill_list)):
		new_fill_ids.append(new_fill_list[i]["orderId"])
		
	print(fill_ids)
	print(new_fill_ids)
	
	temp_fill_ids = new_fill_ids.copy()

	while True:
		if new_fill_ids != fill_ids:
			filled_orders.append(new_fill_ids.pop(0))
		else:
			break
		
	if filled_orders != []:
		
		filled_amount = []
		filled_coin = []
		
		for i in range(len(filled_orders)):
			filled_amount.append(client.get_fills(order_id=filled_orders[i])["items"][0]["size"])
			filled_coin.append(client.get_fills(order_id=filled_orders[i])["items"][0]["symbol"])
		
		print("An order is filled")
		fill_ids = new_fill_ids.copy()
		send_mail(filled_amount, filled_coin)
		
	fill_ids = temp_fill_ids.copy()
	time.sleep(15)
