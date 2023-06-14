from app.controller.ruangwa import RuangWa
from app.config.database import *
import sys
import os
import time

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.getenv('APP_PATH'))


connection = create_connection()


def bulk_check_wa():
    try:
        cursor = connection.cursor()
        query = "select * from nasabah_hp where checked is null"
        cursor.execute(query)

        cursor2 = connection.cursor()

        rows = cursor.fetchall()
        ruangwa = RuangWa()

        counter = 0
        jml_nomor = cursor.rowcount
        length_no_hp = 12

        for row in rows:
            jml_spasi = 2
            result = ruangwa.cek_wa(row[7])
            counter += 1
            jml_nomor -= 1
            if (result['onwhatsapp'] == 'true'):
                status = 1
                message = " Terdaftar"
            else:
                status = 2
                message = " Tidak Terdaftar"
            try:
                updateStatement = f"UPDATE nasabah_hp set checked=1, status={status},keterangan='{result['message']}' where id={row[0]}"
                cursor.execute(updateStatement)
                connection.commit()
                jml_spasi += 37-len(row[3])
                if (len(row[7]) < length_no_hp):
                    jml_spasi += (length_no_hp-len(row[7]))
                elif (len(row[7]) > length_no_hp):
                    jml_spasi += (length_no_hp-len(row[7]))

                print(
                    f'Nomor HP {row[7]} a.n {row[3]} {" "*jml_spasi} | {message}')
                if (counter == 30):
                    print(
                        '=============================================================================')
                    print(f'{jml_nomor} nomor deui')
                    counter = 0
                    time.sleep(60)
            except Exception as e:
                print(f'Error Update database : {e}')
                if (counter == 30):
                    print(
                        '=============================================================================')
                    print(f'{jml_nomor} nomor deui')
                    time.sleep(60)
                    counter = 0
    except Exception as e:
        print(f'Error: {e}')

# bulk_check_wa()
