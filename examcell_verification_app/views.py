from django.shortcuts import render,redirect
from django.http import HttpResponse
import random,string
import mysql.connector as mcdb
import datetime
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
import  pytz
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.contrib import messages


#from django.contrib.sessions.backends.db import SessionStore
# from examcell_verification_app.models import UserInsert

# sessions=Session()

conn = mcdb.connect(host="localhost", user="root", passwd="", database='exam_cell')

print('Successfully connected to database')
cur = conn.cursor()

def InsertRecord(request):
    
    
    if request.method == 'POST':
       
        now=datetime.datetime.now()
        date=now.strftime("%y-%m-%d")
        id=now.strftime("%y-%m-%d_%H:%M:%S")
        ID=id
        name=request.POST.get('name')
        prn=request.POST.get('PRN')
        email=request.POST.get('email')
        ack= id.join(random.choice('0123456789ABCDEFGabcdefg') for i in range(16))
        print(ack)
        # ack check for same ack
        request.session['ack_no']=ack
        request.session['id']=id
        #inserting in users
        query=""" INSERT INTO users VALUES(%s,%s,%s,%s,%s,%s)"""
        
        recordTuple = (id,ack,name,prn,email,date)
        cur.execute(query, recordTuple)
        conn.commit()
        print("Record inserted successfully")
        #updating in status to pending
        query=""" INSERT INTO  `verification status of users` (user_ID,verification_ID) VALUES(%s,%s)"""
        
        recordTuple = (id,1)
        cur.execute(query, recordTuple)
        conn.commit()
        print("Record inserted successfully")
        messages.success(request,'Successfully Inserted')
        HttpResponseRedirect('<h1>Record Inserted Please Store Your ACK No: {}</h1>'.format(ack))

       

        
        return redirect("/upload")
        # return render(request,'upload_doc.html')

    else:
        return render(request, 'index.html')



def home(request):
    return  render(request,'home.html')


def list_users(request):
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    #return list(data)
    print(list(data))
    return render(request, 'view.html', {'categories': data})   






def pendingusers(request):
    cur.execute("Select * from 'users' u inner join  `verification status` v on v.user_ID = u.user_ID inner join 'verification status of user' s on v.user_ID = s.ID Where s.ID=1; ")
    data = cur.fetchall()
    #return list(data)
    print(list(data))
    return render(request, 'users_status.html', {'categories': data})  

# def upload(request):
#     if request.method='POST':
#         uploaded_file=requests.FILES['document'] 


def upload(request):
    print("Function called")
    
    id=request.session['id']
    print(id)
    ack=request.session['ack_no']
    print(ack)
    HttpResponseRedirect('<h1>Your ACK No: {}</h1>'.format(ack))
    if request.POST.get('upload_doc'):
        uploaded_file=request.FILES['doc']
        print(uploaded_file.name)
        print(uploaded_file.size)
        fs=FileSystemStorage()
        name=fs.save(uploaded_file.name,uploaded_file)
        url=fs.url(name)
        url=str(url)
        #doc1 insertion
        query=""" INSERT INTO `user docs`(`user_ID`, `doc_ID`, `doc_link`) VALUES('{0}',{1},'{2}')""".format(id,1,url)
        
        # recordTuple = (id,1,url)
        cur.execute(query)
        conn.commit()
        print("Doc 1 Inserted Successfully")
        #end

        #doc2 uploading

        uploaded_file=request.FILES['doc2']
        print(uploaded_file.name)
        print(uploaded_file.size)
        fs=FileSystemStorage()
        name=fs.save(uploaded_file.name,uploaded_file)
        url=fs.url(name)
        url=str(url)
        # print(name)
        # print(ack_no)
        
       #doc1 insertion
        query=""" INSERT INTO `user docs`(`user_ID`, `doc_ID`, `doc_link`) VALUES('{0}',{1},'{2}')""".format(id,2,url)
        
        # recordTuple = (id,1,url)
        cur.execute(query)
        conn.commit()
        print("Doc 1 Inserted Successfully")
        #end


     
        return redirect("/uploaded")
    return render(request,'upload_doc.html')
    
   
def uploaded(request):
    return render(request,'uploaded.html')  
