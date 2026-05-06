import qrcode

url = "https://stock-price-prediction-vx4hauarkhntccnhhhxcez.streamlit.app/"

qr = qrcode.make(url)
qr.save("streamlit_qr.png")

print("QR Code Generated!")