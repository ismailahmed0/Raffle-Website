'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
#####
Ismail A Ahmed/Hanzala N Siddiqui
views.py
Version 4.0
'''
from django.http import HttpResponseRedirect
from django.shortcuts import render
import passlib
import getpass
from passlib.hash import pbkdf2_sha256
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.mime.text import MIMEText
from cryptography.fernet import Fernet
import hashlib
from passlib.hash import sha256_crypt

#key = Fernet.generate_key()
lines1 = open('raffle_key.txt').readlines()  #encrypted raffle number has a certain key that is required to decrypt it
content1 = lines1[0]
content1 = content1.strip('b').strip("'") #gets rid of the trash
content1 = content1[:-2]
content1=str.encode(content1)
cipher_suite = Fernet(content1)

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))  # fastest
    return str(len(str_list) + 1)


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_DAB.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("userlist").sheet1
next_row = next_available_row(sheet)

global lst
lst = []

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
for x in list_of_hashes:
    lst.append(x['Username'] + ' ' + str(x['Password']))

global lsttest
lsttest = []
global userlist
userlist = []
moneyval = []
senderemail = []
from .forms import NameForm
def Purchase(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            global username
            username = request.POST.get('username', '')
            global password
            password = request.POST.get('password', '')

            worked=rd()
            if worked=='True':
                usermoney = moneyval[0]
                del moneyval[:] #clears values in list for restart
                del userlist[:] #clears values in list for restart
                del lsttest[:] #clears values in list for restart
                #smtp_server_name = 'smtp.gmail.com'
                #port = '465'  # for secure messages
                # port = '587' # for normal messages

                #sender = 'PUT YOUR USERNAME HERE@gmail.com'
                #receiver = senderemail[0]+'@gmail.com' #cause instructions on page tell not to add the @gmail, we automatically add it here, assuming they use gmail(which we can do this this is not for full professional use)

                with open('raffle_numbers.txt') as baselines: #gets raffle numbers
                    lines = baselines.readlines()
                content = lines[0] #gets only one raffle number from list, easiest way is to get the first value in list(0th index)
                content0 = content.strip('b').strip("'")  # gets rid of the trash
                content0 = content0[:-2] # gets rid of unnessary stuff
                content0 = str.encode(content0)

                plain_text = cipher_suite.decrypt(content0) #decrypts raffle number
                plain_text = str(plain_text)
                plain_text = plain_text.strip('b').strip("'")  # gets rid of the trash
                plain_text = ('Your raffle ticket number is: '+plain_text +'\n'+'\n'+'Thanks again for your purchase!\n'+'\n'+'Sincerely,'+'\n'+'\tThe Computer Science Team'+'\n'+'\n'+'Please do not reply to this message. This email is unmonitored. If you have any questions, please contact CONTACT NAME at CONTACT EMAIL@gmail.com.')

                newFile = open('raffle_bought.txt', 'a') #stores raffles bought in text file for later use.
                newFile.write(content)
                newFile.close()
                #msg = MIMEText(plain_text)
                #msg['From'] = sender
                #msg['To'] = receiver
                #msg['Subject'] = 'Raffle Ticket'
                #if port == '465':
                #    server = smtplib.SMTP_SSL('{}:{}'.format(smtp_server_name, port))
                #else:
                #    server = smtplib.SMTP('{}:{}'.format(smtp_server_name, port))
                #    server.starttls()  # this is for secure reason

                #server.login(sender, "PUT YOUR PASSWORD HERE")
                #server.send_message(msg)
                #server.quit()

                with open('raffle_numbers.txt', 'w') as f: #writes all the raffle numbers into the text file with the exception of the one that was bought
                    f.writelines(lines[1:])
                del senderemail[:]
                return render(request, "purchase.html", {"my_stuff": usermoney}) #GO to the html file in the templates folder for this
                #return HttpResponseRedirect('/about/')
            elif worked=='False':
                del moneyval[:] #restarts the list for next purchase
                del userlist[:] #restarts the list for next purchase
                del lsttest[:] #restarts the list for next purchase
                return render(request, "purchase.html", {"notmy_stuff": 'Insufficient Credit!'}) #GO to the html file in the templates folder for this
            else:
                del moneyval[:] #restarts the list for next purchase
                del userlist[:] #restarts the list for next purchase
                del lsttest[:] #restarts the list for next purchase
                return render(request, "purchase.html", {"defnotmy_stuff": 'Username or password incorrect!'}) #GO to the html file in the templates folder for this
        else:
            del moneyval[:]  #restarts the list for next purchase
            del userlist[:] #restarts the list for next purchase
            del lsttest[:] #restarts the list for next purchase
            return render(request, "purchase.html", {"bad_input": 'Please enter both the username and password!'}) #GO to the html file in the templates folder for this


    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'purchase.html', {'form': form})

def check_password(hashed_password, user_password): #checks to see if username entered matches the username in google sheet
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
def check_password1(hashed_password, user_password): #checks to see if password entered matches the password in google sheet
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

def goodhash():
    global username
    global password

    for x in lst:  # goes through a encrypted list that contains username/password
        x = x.split(' ')  # splits up the username/password into their own list and puts username as x[0] and pass as x[1]
        #test1 = sha256_crypt.verify(username, x[0])
        #test1 = pbkdf2_sha256.verify(username, x[0])  # checks to see if the username client entered matches encrypted version at x[0]
        #userlist.append(x[0])
        #test2 = sha256_crypt.verify(password, x[1])

        if check_password(x[0], username):
            #test2 = pbkdf2_sha256.verify(password, x[1])  # checks to see if the password client entered matches encrypted version at x[1]
            if check_password1(x[1], password):  # if both match, this means that the user exists, so do the following
                x[0] = username  # replace the encrypted username with the unencrypted username(the username the client entered)
                x[1] = password  # replace the encrypted password with the unencrypted password(the password the client entered)
                xx = (x[0] + ' ' + x[1])  # now make the CORRECT username/password right next to each other but with a space seperating them, like it it originally was(albeit unencrpted)
                lsttest.append(xx)  # check comments in rd() function to see how this is useful
                break
            else:  # look at foor loop that deosnt have the list(for x in z). this is what happens if the "x" is not the one
                xx = (x[0] + ' ' + x[1])  # restores the other username/passwords back to their original state before .split(' ')
                lsttest.append(xx)  # check comments in rd() function to see how this is useful
        else:  # look at foor loop that deosnt have the list(for x in z). this is what happens if the "x" is not the one
            xx = (x[0] + ' ' + x[1])  # restores the other username/passwords back to their original state before .split(' ')
            lsttest.append(xx)  # check comments in rd() function to see how this is useful

        #def purchase(request):
 #   return render(request, "purchase.html", {})


def rd(*kargs):
    global username
    global password


    goodhash()

    count = 2 #2 is the row the first salt hash usernames/passwords are stored
    file = (username + ' ' + password)  # gets the username and password client entered and adds space in between like in lsttest list
    if file not in lsttest:
        # showinfo("Error", "Incorrect username or password!")

        return 'N/A'
    else:

        for x in lsttest:  # checks to see if what the client entered is in lsttest list
            if x == file:

                userbalance = sheet.cell(count, 3).value
                #userbalance = hashlib.sha256((userbalance).encode('utf-8')).hexdigest()
                if userbalance=='':
                    userbalance='0'
                #outfile = open("testing.txt", 'a')
                #outfile.write(userbalance)
                #outfile.close()
                userbalance = int(userbalance)
                userbalance -= 1
                # row,column
                if userbalance >= 0:
                    userbalance = str(userbalance)
                    moneyval.append(userbalance)


                    sheet.update_cell(count, 3, userbalance)
                    senderemail.append(username) #puts the username inside of list so that it can be sent in the Purchase function
                    # showinfo("Purchase Succsessful","Your Balance is $" + str(userbalance) + ".00!")
                    return 'True'
                else:
                    # showinfo("Purchase Failed", "Insufficient Credit!")
                    #outfile = open("testing.txt", 'a')
                    #outfile.write("FALSE")
                    #outfile.close()
                    return 'False'

            count += 1





def home(request):
    return render(request, "home.html", {})

def Money(request):
    return render(request, "money.html", {})
def about(request):
    #from pages.namer import bob
    return render(request, "about.html", {})

'''
    usermoney = moneyval[0]
    del moneyval[:]

    #my_name = "Hello, My Name is John Elder"
    return render(request, "about.html", {"my_stuff": usermoney})

def contact(request):
    return render(request, "contact.html", {})

def testpage(request):
    return render(request, "testpage.py", {})
'''