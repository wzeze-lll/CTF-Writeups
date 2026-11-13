"""Invert the table-swapped Base64 transformation recorded for usualCrypt."""
import base64

standard = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
custom = list(standard)
for i in range(6, 15):
    custom[i], custom[i + 10] = custom[i + 10], custom[i]
custom = ''.join(custom)

cipher = 'zMXHz3TIgnxLxJhFAdtZn2fFk3lYCrtPC2l9'
base64_text = ''.join(standard[custom.index(ch)] for ch in cipher.swapcase())
print(base64.b64decode(base64_text).decode('ascii'))
