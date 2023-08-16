from app.controller.ruangwa_image import RuangWaImage
from app.config.database import *
import sys
import os
import time
import datetime
import json

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.getenv('APP_PATH'))


connection = create_connection()


def bulk_send_wa_image():
    try:
        cursor = connection.cursor()
        query = "select * from wa_image where terkirim=0"
        cursor.execute(query)

        cursor2 = connection.cursor()

        rows = cursor.fetchall()
        ruangwa = RuangWaImage()

        counter = 0
        jml_nomor = cursor.rowcount
        length_no_hp = 12

        for row in rows:
            jml_spasi = 2
            result = ruangwa.send_wa_image(row[1], row[2], row[3])
            result_string = json.dumps(result)
            counter += 1
            tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            jml_nomor -= 1
            if (result['result'] == 'true'):
                status = 1
                message = f" Terkirim ke {row[1]}"
            else:
                status = 2
                message = f" Gagal terkirim ke {row[1]}"
            try:
                updateStatement = f"UPDATE wa_image set terkirim=1, waktu='{tanggal}', callback='{result_string}' where id={row[0]}"
                cursor.execute(updateStatement)
                connection.commit()
                print(message)
                if (counter == 5):
                    print(
                        '=============================================================================')
                    print(f'{jml_nomor} Nomor Lagi')
                    counter = 0
                    time.sleep(60)
            except Exception as e:
                print(f'Error Update database : {e}')
                if (counter == 5):
                    print(
                        '=============================================================================')
                    print(f'{jml_nomor} Nomor Lagi')
                    time.sleep(60)
                    counter = 0
    except Exception as e:
        print(f'Error: {e}')

# bulk_send_wa_image_image()
