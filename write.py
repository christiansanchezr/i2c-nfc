import board
import busio
import time
from adafruit_pn532.i2c import PN532_I2C

# Inicializar I2C y PN532
i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)

# Obtener versión
ic, ver, rev, support = pn532.firmware_version
print(f"✅ PN532 detectado - Firmware v{ver}.{rev}")

# Configurar lectura
pn532.SAM_configuration()

# Leer texto desde consola
texto = input("📥 Ingresa el texto a escribir (máx. 16 caracteres): ")
texto = texto[:16]  # máximo 16 caracteres
datos = texto.ljust(16).encode("utf-8")  # rellenar a 16 bytes

# Separar en bloques de 4 bytes (NTAG215 usa bloques de 4 bytes)
bloques = [datos[i:i+4] for i in range(0, 16, 4)]

print("📡 Esperando una tarjeta NTAG215...")

while True:
    uid = pn532.read_passive_target(timeout=0.5)
    if uid is None:
        continue

    print("🎯 Tag detectado. UID:", [hex(i) for i in uid])

    try:
        # NTAG215 tiene datos de usuario desde bloque 4 en adelante
        for i, bloque in enumerate(bloques):
            bloque_num = 4 + i
            if pn532.ntag2xx_write_block(bloque_num, bloque):
                print(f"✅ Escrito en bloque {bloque_num}: {bloque}")
            else:
                print(f"❌ Fallo al escribir en bloque {bloque_num}")

        break  # Salir tras escritura
    except Exception as e:
        print("❌ Error durante escritura:", e)
        time.sleep(1)
