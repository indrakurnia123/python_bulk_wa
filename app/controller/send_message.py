import sys
import os
import time
import datetime
import json

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.getenv('APP_PATH'))

from app.config.database import *
from app.controller.ruangwa import RuangWa

connection = create_connection()

def bulk_send_wa():
	try:
		cursor = connection.cursor()
		query = "select * from wa_message where terkirim=0"
		cursor.execute(query)

		cursor2 = connection.cursor()

		rows = cursor.fetchall()
		ruangwa = RuangWa()

		counter = 0
		jml_nomor = cursor.rowcount
		length_no_hp = 12

		for row in rows:	
			jml_spasi = 2;
			result = ruangwa.send_wa(row[1],row[2])
			result_string = json.dumps(result)
			counter+=1
			tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			jml_nomor-=1
			if (result['result']=='true'):
				status=1
				message=f" Terkirim ke {row[1]}"
			else:
				status=2
				message=f" Gagal terkirim ke {row[1]}"
			try:
				updateStatement = f"UPDATE wa_message set terkirim=1, waktu='{tanggal}', callback='{result_string}' where id={row[0]}"
				cursor.execute(updateStatement)
				connection.commit()
				print(message)
				if (counter==5):
					print('=============================================================================')
					print(f'{jml_nomor} nomor deui')
					counter=0
					time.sleep(60)
			except Exception as e:
				print(f'Error Update database : {e}')
				if (counter==5):
					print('=============================================================================')
					print(f'{jml_nomor} nomor deui')
					time.sleep(60)
					counter=0
	except Exception as e:
		print(f'Error: {e}')

# bulk_check_wa()