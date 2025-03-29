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

# Pedir al usuario el texto a escribir
texto = input("Ingresa el texto a escribir en el tag (máx. 16 caracteres): ")
texto = texto[:16]  # Limitar a 16 caracteres
datos = bytearray(texto.ljust(16).encode('utf-8'))  # Rellenar a 16 bytes con espacios

print("Ahora acerca una tarjeta NFC para escribir...")

while True:
    uid = pn532.read_passive_target(timeout=0.5)
    if uid is None:
        continue

    print("Tarjeta detectada. UID:", [hex(i) for i in uid])

    # Autenticación con clave por defecto
    default_key = b'\xFF\xFF\xFF\xFF\xFF\xFF'
    if not pn532.mifare_classic_authenticate_block(uid, 4, PN532_I2C.MIFARE_CMD_AUTH_A, default_key):
        print("Fallo al autenticar el bloque 4")
        continue

    # Intentar escribir
    if pn532.mifare_classic_write_block(4, datos):
        print(f"✅ Texto '{texto}' escrito correctamente en el bloque 4")
    else:
        print("❌ Falló la escritura")

    break  # Salir después de una escritura exitosa o fallida
