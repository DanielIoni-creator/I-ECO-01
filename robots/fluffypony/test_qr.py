#!/usr/bin/env python3
import qrcode
from PIL import Image

# Genera il QR
address = "45M4DW1ug8bdQowWpxucTpgsfjLbVxbYaAra79VewmBobuuhgqTjyD4R3DzpqLM2veiphcB16n24qN1QbLg3y2PYGK3Qkoe"
amount = 0.01
uri = f"monero:{address}?amount={amount}"

qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(uri)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("test_qr.png")

print(f"✅ QR Code generato: test_qr.png")
print(f"📱 URI: {uri}")
print("🖼️ Apri test_qr.png per verificare")
