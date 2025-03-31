import board
import busio
import time
from adafruit_pn532.i2c import PN532_I2C

# Inicializar
i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)

ic, ver, rev, support = pn532.firmware_version
print(f"PN532 firmware v{ver}.{rev}")
pn532.SAM_configuration()

print("Acerca el tag NTAG213...")

while True:
    uid = pn532.read_passive_target(timeout=None)
    if uid:
        print("✅ Tag detectado. UID:", [hex(x) for x in uid])

        # Leer páginas 4 a 7 (4 páginas, 4 bytes cada una)
        try:
            for page in range(4, 8):
                data = pn532.ntag2xx_read_page(page)
                print(f"Página {page}: {data}")
        except RuntimeError as e:
            print("⚠️ Error al leer página:", e)

        break
