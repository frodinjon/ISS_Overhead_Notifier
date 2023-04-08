import requests
import datetime as dt
import smtplib
import time

ISS_URL = "http://api.open-notify.org/iss-now.json"
SUN_URL = "https://api.sunrise-sunset.org/json"

## ATLANTA, GA
MY_LAT = 33.748997
MY_LONG = -84.387985

sun_params = {
	"lat": MY_LAT,
	"lng": MY_LONG,
	"formatted": 0
}

def fetch_data(url, params={}):
	response = requests.get(url=url, params=params)
	response.raise_for_status()
	return response.json()

def is_dark():
	data = fetch_data(url=SUN_URL, params=sun_params)
	now = dt.datetime.now()
	if now.hour < int(data["results"]["sunset"].split("T")[1].split(":")[0]):
		return False
	elif now.hour > int(data["results"]["sunrise"].split("T")[1].split(":")[0]):
		return False
	else:
		return True

def is_overhead():
	data = fetch_data(url=ISS_URL)
	longitude = float(data["iss_position"]["longitude"])
	latitude = float(data["iss_position"]["latitude"])
	if longitude >= MY_LONG - 5 and longitude <= MY_LONG + 5:
		if latitude >= MY_LAT - 5 and latitude <= MY_LAT + 5:
			return True
	else:
		return False


SENDER_EMAIL = "sender_email"
HOST = "smtp.gmail.com"
PASSWORD = "password"
RECIPIENT = "email"
MESSAGE = "The ISS is overhead and it's super dark, bro! Look up!"

def send_message():
	if is_dark() and is_overhead():
		with smtplib.SMTP(host=HOST) as connection:
			connection.starttls()
			connection.login(user=SENDER_EMAIL, password=PASSWORD)
			connection.sendmail(from_addr=SENDER_EMAIL, to_addrs=RECIPIENT, msg=f"Subject: Look Up!\n\n{MESSAGE}")

while True:
	time.sleep(60)
	send_message()