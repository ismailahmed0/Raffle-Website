# Web-Purchase-Server
WARNING: Trying to add money to the user's account wil NOT be successful as it has to be done through a seperate program or manually(you have to make your own and make it editable with python. See link below.) Do NOT expect to get your money back if you try to add your money to the user's account. You have to go into the money.html and replace the button code with your own. Also, please make sure to add the email address and its password that you would like to use to send the raffle ticket number. They are located on lines 95 and 123 on views.py in the pages folder in the second mysite folder. The only ID number(username) and password that the provided program will accept are those on the examplelogin.txt. If you would like to use different usernames/passwords, you need to make your own google sheets.

This is a program that will allow a user to login and purchase a raffle ticket. The cost will be one dollar. They can add money to their account on the Add Money page. This is done on a webpage through a server on your computer. 

Required Modules: django, passlib, gspread, ouath2client, cryptography, and hashlib.
Place the code.py folder(un-zipped) into Windows (C:). Open command line or powershell from the start menu and cd to the folder your manage.py file is in. Then, type python manage.py runserver in the command line. After that, type localhost:8000 into the url entry  in your web browser and hit enter.

Good websites to connect python with google sheets: https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html, https://www.makeuseof.com/tag/read-write-google-sheets-python/. Switching between the two websites makes it easier to follow along.

Good video to download django: https://www.youtube.com/watch?v=yyt3tQYW3g0

Good video to host raffle program on PythonAnywhere: https://www.youtube.com/watch?v=Y4c4ickks2A
