import board
import busio
import time
from adafruit_pn532.i2c import PN532_I2C

# Inicializar I2C y PN532
i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)

# Obtener versión del firmware
ic, ver, rev, support = pn532.firmware_version
print(f"PN532 firmware v{ver}.{rev}")

# Configurar para leer tarjetas
pn532.SAM_configuration()

print("Acerca una tarjeta NFC para leer...")

while True:
    uid = pn532.read_passive_target(timeout=0.5)
    if uid is None:
        continue

    print("Tarjeta detectada. UID:", [hex(i) for i in uid])

    # Autenticar con el bloque 4 (sector 1, bloque 0)
    default_key = b'\xFF\xFF\xFF\xFF\xFF\xFF'
    if not pn532.mifare_classic_authenticate_block(uid, 4, PN532_I2C.MIFARE_CMD_AUTH_A, default_key):
        print("Fallo al autenticar el bloque 4")
        continue

    data = pn532.mifare_classic_read_block(4)
    if data:
        print("Datos del bloque 4:", data.decode(errors='ignore'))
    else:
        print("No se pudo leer el bloque")
    
    time.sleep(2)
