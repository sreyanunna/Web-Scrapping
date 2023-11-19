#!/usr/bin/env python
# coding: utf-8

# # Domain - Online Food app 

# ## About this application - 
#     So let me introduce you to the community of food!
#     Here you are allowed to write your own stories, share your recipes and discuss your food 
#     opinions with the world. 
#     But wait their is more!!
#     We have launched our very own merchandise from kitchen utensils to seasonings. 

# # BeautifulSoup + MIME (Sending Emails)

# Problem Statement : Its national Taco day! Extract taco recipes from a website and email these recipes to your subscriber encouraging them to cook tacos at home. Make the Email look apealing with taco image and proper structure to the email 

# In[28]:


import urllib.request
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
server = smtplib.SMTP_SSL("smtp.gmail.com",465)
server.login("sreya.nunna@gmail.com","sreeja9608")

msg=MIMEMultipart()
msg['From']='TACO101<sreya.nunna@gmail.com>'
msg['To'] ='SN<nunna.sreya@science.christuniversity.in>'
msg['Subject']="TACO RECIPES TO CELEBRATE WORLD TACO DAY!"
intro='''Dear Subscriber,
Happy World Taco Day!!
We have some exciting news for you today ...
Here are our top recipes for making Tacos for you to celebrate this occassion with us! If you make tacos today using any of these
recipes do tag us- @tacoworld123 with #worldtacoday
MUNCH AWAY:)))
'''

msg.attach(MIMEText(intro,'plain'))
filename='.jpg'
f=open('crop.jpg','rb')
b=MIMEBase('application','octet-stream')
b.set_payload((f).read())
encoders.encode_base64(b)
b.add_header("Content-Disposition",f"attachment; filename=crop.jpg")
msg.attach(b)

data = urllib.request.urlopen("http://taco-randomizer.herokuapp.com/").read().decode()
soup = BeautifulSoup(data,'html.parser')

a=soup.find_all('div' , class_ ='recipe')
for i in a:
    main=i.get_text()
    body=main
    
    msg.attach(MIMEText(main,'plain'))  

message =msg.as_string()
server = smtplib.SMTP_SSL("smtp.gmail.com",465)
server.login("sreya.nunna@gmail.com","1234")
server.sendmail("sreya.nunna@gmail.com","nunna.sreya@science.christuniversity.in",message)
server.quit()

    



# # API + Json + urllib

# Problem statement: Create a recipe generater. Allow the user to search the tyoe of food they want according to the area(eg. Italian, Indian etc). Once they enter the type of food they are interested in give a list of dishes from that region that you recommend them to try. After that, allow them to search the recipe they desire. Note that the dish whose recipe the user searches for finally, can also be different from the desired region selected by user.  

# In[2]:



import urllib.request,urllib.parse
import json

print('Welcome to bakemymeal.com ')
print('What would you like to cook today?')


def find():
    furl= "https://www.themealdb.com/api/json/v1/1/filter.php?"

    cat= input('Search by area(eg. Italian)')
    
    apurl=urllib.parse.urlencode({"a":cat})
    url=furl+apurl
    print(url)
    data=urllib.request.urlopen(url)
    jdata=data.read().decode()
    
    d=json.loads(jdata)

    for i in d['meals']:
        print(i['strMeal'])
    
    

def recipe():
   
    furl2="https://www.themealdb.com/api/json/v1/1/search.php?"

    c=input("Enter the recipe of food you want")
    
    apurl2=urllib.parse.urlencode({"s":c})
    url2=furl2+apurl2
    print(url2)
    data=urllib.request.urlopen(url2)
    jdata=data.read().decode()
    
    d=json.loads(jdata)
    

    
    for i in d['meals']:
        print(i['strMeal'])
        print(i["strInstructions"])
    
    


find()
recipe()


# # XML +  Fifo Queue 

# Problem Statement: You have an XML document of all the customers' details who have purchased kitchen/food related products from your website in a given month. Calculate the total revenue of that month. Also, your company has conducted a RainFest for its customers where selected customers of that month will be awarded by saying their next purchase from this store will be completely free. Take the first 4 customers to be the lucky winners and announce their names on the website 

# In[13]:


import xml.etree.ElementTree as ET
from functools import reduce 
import threading 
import time 
import queue 
#for getting it from xml file
root = ET.parse('purchase1.xml')
r=root.getroot()
st=root.find('customers')

a=root.findall('customer')
    
list1=[]
for i in a:

    list1.append(int((i).find("amt").text))
            

#finding total revenue
def reducefun(list1,b):
    return list1+b
obj1 = reduce(reducefun,list1)
print('Total Revenue for the month:',obj1)

#Declaring winners
#the first 4 customers will win 
print('Welcome to our Website. We will declare the winners for RainFest 2021 shortly')
list2=[]
for i in a:
    list2.append((i).find("name").text)
 

def put():
    for i in list2[1:5]:
        q.put(i)
        
def cons():
    print("The following customers are winners for the RainFest 2021")
    print("Congratulations and thank you for buying from us :) Your next purchase will be completely free")
                
    while True:
        
        print(q.get())
        time.sleep(1)
    
q= queue.Queue()        
                
t1 = threading.Thread(target = put)
t2 = threading.Thread(target = cons)
t1.start()
t2.start()

   


# # Event thread
# 

# Problem Statement : There are 2 lists of the available products and their prices respectively. A customer is entering your website to purchase a product. Make sure to display the avaliable products. Once they enter the productthey desire to buy, Start the billing process. While their billing is in the process, display advertisements of other products available (except the one they purchased) until the bill is done processed. Once its processed, display the amount.

# In[36]:


import threading
import time
print("Welcome to our Store here are our available products")
list1=['Wok','Pan','Spice Mix','OTG','Air fryer','Stove','Microwave','Heater']
list2=[300,600,130,5000,4000,2000,3456,7891]

def bill():
    
    print("Print - available items",list1)
    n=input('Enter the product you like to buy')
    e.set()
    time.sleep(0.1)
    j=list1.index(n)
    print(j)
    print('Bill is being generated')
    
    e.clear()
    print("Your bill for this product is",list2[j])
    
def ads():
    e.wait()
    print("While your Bill is being generated please check out our other products available")
    while e.isSet():
        for i in list1:
            if i==n:
                pass
            else:
                print(i)
                
e = threading.Event()
t1= threading.Thread(target = bill)
t2= threading.Thread(target = ads)
t1.start()
t2.start()


# # Condition Thread

# Problem Statement: A user is on the login page. Allow them to accept the terms and conditions and enter their email and usename for access.After they have given their email, send an email to their id introducing your brand and promo codes.
#     

# In[6]:


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import threading
import time

def intro():
    
    
    print("Welcome to ChilliCream! Sign Up today for exciting promos and delicious recipes")
    c.acquire()
    time.sleep(0.1)
    print("Please accept our Terms and conditions")
    c.notify()
    c.release()
    
def email():
    c.acquire()
    c.wait()
    email = input("Enter your email")
    name= input("Enter your name")
    msg=MIMEMultipart()
    msg['From']='ChilliCream<sreya.nunna@gmail.com>'

    msg['To']='{}<{}>'.format(name,email)

    msg['Subject']="Welcome to ChilliCream"

    body ="""
    Dear Subscriber,
    We are so excited to have you here!
    You have officially unlocked the door to amazing recipes written by people from all over the world
    You must be wondering what goes on here.. So let me introduce you to the community of food!
    Here you are allowed to write your own stories, share your recipes and discuss your food 
    opinions with the world. 
    But wait their is more!!
    We have launched our very own merchandise from kitchen utensils to seasonings. 
    Check out our content because we assure that you will enjoy it!
    Have a wonderful day and happy cooking :)
    
    USE PROMOCODE : NEWME50 for 50% off on your first purchase

    """ 
    msg.attach(MIMEText(body,'plain'))
    st=smtplib.SMTP_SSL('smtp.gmail.com',465)
    st.login('sreya.nunna@gmail.com',1234)
    message=msg.as_string()
    st.sendmail('sreya.nunna@gmail.com'.format(email),message)
    st.quit()
    
c= threading.Condition()
t1=threading.Thread(target=intro)
t2=threading.Thread(target=email)
t1.start()
t2.start()


# # Queue (lifo)

# Problem Statement - Your company conducted a Donation Camp for COVID support. The following XML data has the customer details. from them the 4,5,6 th customers donated to this camp. Mention their names and appreciate their offer (order should be in who payed the most to least). 
# Also mention that they are going to receive 50% off on their next purchase for the same.

# In[12]:


import xml.etree.ElementTree as ET
from functools import reduce 
import threading 
import time 
import queue 
#for getting it from xml file
root = ET.parse('purchase1.xml')
r=root.getroot()
st=root.find('customers')

a=root.findall('customer')
    



print('Welcome to ChilliCream.' )
list2=[]
for i in a:
    list2.append((i).find("name").text)
 

def put():
    for i in list2[4:7]:
        q.put(i)
        
def cons():
    print("The following customers are winners for the Donation Camp 2021")
    print("Thank you so much for your contribution :) Your next purchase will be 50% OFF")
                
    while True:
        
        print(q.get())
        time.sleep(1)
    
q= queue.LifoQueue()        
                
t1 = threading.Thread(target = put)
t2 = threading.Thread(target = cons)
t1.start()
t2.start()

   


# In[ ]:




