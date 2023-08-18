import requests
import os
import json
import datetime
from dotenv import load_dotenv

# Load variabel lingkungan dari file .env
load_dotenv()


class RuangWa(object):
    def __init__(self):
        self.api_url = os.getenv('API_URL')
        self.api_access_key = os.getenv('API_ACCESS_KEY')
        self.api_token = os.getenv('API_TOKEN')

    def cek_wa(self, number):
        url = self.api_url+'/check_number'
        token = self.api_token
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'token': token,
            'number': number
        }
        try:
            response = requests.post(url, data, headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None

    def send_wa(self, number, message):
        url = self.api_url+'/send_message'
        tanggal = datetime.datetime.now()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'token': self.api_token,
            'number': number,
            'message': message,
            'date': tanggal.strftime("%Y-%m-%d"),
            'time': tanggal.strftime("%H:%M:%S")
        }
        try:
            response = requests.post(url, data, headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None

    def send_wa_image(self, number, file, caption):
        url = self.api_url+'/send_image'
        tanggal = datetime.datetime.now()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'token': self.api_token,
            'number': number,
            'file': file,
            'caption': caption,
            'date': tanggal.strftime("%Y-%m-%d"),
            'time': tanggal.strftime("%H:%M:%S")
        }
        try:
            response = requests.post(url, data, headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None
