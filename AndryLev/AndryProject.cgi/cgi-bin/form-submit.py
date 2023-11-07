
import cgi
from os import environ
from http.cookies import SimpleCookie

cookie = SimpleCookie(environ.get("HTTP_COOKIE"))
counter = cookie.get("counter")

if counter is None:
    
    counter = 0
else:
    try:
       
        counter = int(counter.value)
    except ValueError:
        
        counter = 0

new_counter = counter + 1


form = cgi.FieldStorage()
f_name = form.getfirst("f_name", "First name is blank")
s_name = form.getfirst("s_name", "Last name is blank")
r1 = form.getfirst("r1", "No selection of Sex")
my_group = form.getfirst("my_group", "No group")

print(f"Set-cookie: counter={new_counter};")
print("Content-type: text/html")
print()
print("<br><b>First Name:</b>", f_name)
print("<br><b>Last Name:</b>", s_name)
print("<br><b>Sex:</b>", r1)
print("<br><b>Group:</b>", my_group)
print("<br><b>Form:</b> ", new_counter)



print("<br><br><br><a href='/form.html'>Back to Form</a>")
