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

pn532.SAM_configuration()

print("📡 Esperando una tarjeta NTAG215...")

while True:
    uid = pn532.read_passive_target(timeout=0.5)
    if uid is None:
        continue

    print("🎯 Tag detectado. UID:", [hex(i) for i in uid])

    try:
        # Leer bloques 4, 5, 6 y 7 (16 bytes)
        datos = bytearray()
        for bloque_num in range(4, 8):
            bloque = pn532.ntag2xx_read_block(bloque_num)
            if bloque is None:
                print(f"❌ No se pudo leer el bloque {bloque_num}")
                break
            datos.extend(bloque)

        texto = datos.decode("utf-8", errors="ignore").strip()
        print(f"📖 Texto leído: '{texto}'")

        break  # Salir después de leer
    except Exception as e:
        print("❌ Error durante lectura:", e)
        time.sleep(1)
