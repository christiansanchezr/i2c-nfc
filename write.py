import board
import busio
import time
from adafruit_pn532.i2c import PN532_I2C

i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)

pn532.SAM_configuration()

texto = input("Texto (máx 4 caracteres): ").ljust(4)[:4]
datos = bytearray(texto.encode('utf-8'))

print("Acerca un NTAG213 para escribir...")

while True:
    uid = pn532.read_passive_target(timeout=None)
    if uid:
        print("✅ Tag detectado. UID:", [hex(x) for x in uid])

        try:
            pn532.ntag2xx_write_page(4, datos)  # Página 4 es la primera disponible
            print(f"✅ Escrito '{texto}' en página 4")
        except RuntimeError as e:
            print("❌ Error al escribir:", e)
        
        break
