import pyotp
import qrcode
import io


key = pyotp.random_base32()
otp_string=f"otpauth://totp/axia?secret={key}&issuer=A4B%20AXIA"

qr = qrcode.QRCode()
qr.add_data(otp_string)
f = io.StringIO()
qr.print_ascii(out=f)
f.seek(0)
print(f.read())
print(key)