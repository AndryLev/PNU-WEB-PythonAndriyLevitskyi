
from http.cookies import SimpleCookie
import sys

new_cookie = SimpleCookie()
new_cookie["counter"] = ""
new_cookie["counter"]["expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"

print("Status: 302 Found")
print("Location: /form.html")
print(new_cookie.output())
print()

sys.exit()


