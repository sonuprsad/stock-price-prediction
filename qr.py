import qrcode

url = "https://your-app-name.streamlit.app"

qr = qrcode.make(url)
qr.save("streamlit_qr.png")

print("QR Code Generated!")