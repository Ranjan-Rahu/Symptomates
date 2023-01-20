from django.shortcuts import render, HttpResponse
from datetime import datetime
from home.models import Contact
from django.contrib import messages


import sqlite3

import os
from email.message import EmailMessage
import ssl
import smtplib
# Create your views here.
def index(request):
    context = {
        "variable1":"Harry is great",
        "variable2":"Rohan is great"
    } 
    return render(request, 'index.html', context)
    # return HttpResponse("this is homepage")

def about(request):
    return render(request, 'about.html') 
 

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        symptoms = request.POST.get('symptoms')
        # contact = Contact(name=name, email=email, phone=phone)
        contact = Contact(name=name, email=email, phone=phone, age=age,gender=gender, symptoms=symptoms)
        contact.save()
        messages.success(request, 'Your message has been sent!')
        conn=sqlite3.connect("diseases.db")
        c=conn.cursor()
        # first full text search
        
        arr=[]
        for row in c.execute('''SELECT disease_name FROM symptoms WHERE symptoms MATCH ?''',[symptoms]):
            arr.append(str(row))
        t=""
        
        disease=[]
        for i in range(0,len(arr)):
            f=arr[i]
            f=f.replace("(","")
            f=f.replace(")","")
            f=f.replace("'","")
            f=f.replace(",","")
            disease.append(f)
        dict={
            "noida":"ebola",
            "delhi":"dengue",
            "mumbai":"mpox"
        }
        bool=False
        for city in dict:
            if(city==phone):
                for i in range(0,len(disease)):
                    if(dict[city]==disease[i]):
                        main=dict[city]
                        bool = True

        for i in range(0,len(arr)):
            if(bool==True and i==0):
                t+="\n*"+main+" (priority)"
                t+="\n"
            f=arr[i]
            f=f.replace("(",f"{i+1}. ")
            f=f.replace(")","")
            f=f.replace("'","")
            f=f.replace(",","")
            t+=f
            t+="\n"
        email_sender = os.environ.get("EMAIL")
        email_password=os.environ.get("EMAIL PASSWORD")
        email_receiver=email
        subject = 'Your Complications from Symptoms'
        body=f'''Hello {name}
        \nYour provided details are :-
        \nAge : {age}
        \nGender : {gender}
        \nCity : {phone}
        \nSymptoms : {symptoms}\n
        \nBy analysing your symptoms, we have come to a conclusion:\nYou have the chances of the following diseases:\n{t}\n
        \n Thanks for using Symptomates
        '''
        em = EmailMessage()
        em['From']=email_sender
        em['To']=email_receiver
        em['Subject']=subject
        em.set_content(body)
        context=ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,em.as_string())

        
    return render(request, 'contact.html')
 
