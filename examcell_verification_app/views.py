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
from django.core.mail import EmailMessage
#adding mail
from django.conf import settings 
from django.core.mail import send_mail 
from .models import Dash
#adding razorpay
#from payment.settings  import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
import razorpay
RAZORPAY_API_KEY='rzp_test_Q3BsAA1rvI7v3G'
RAZORPAY_API_SECRET_KEY='TIFbDeahcJtTjuo0nLWFnM6T'
client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
#from django.contrib.sessions.backends.db import SessionStore
# from examcell_verification_app.models import UserInsert
#path
from pathlib import Path
# sessions=Session()

conn = mcdb.connect(host="localhost", user="root", passwd="", database='examcell_v1')

print('Successfully connected to database')
cur = conn.cursor()

def payment(request):
    order_amount=50000
    order_currency='INR'
    payment_order=client.order.create(dict(amount=order_amount,currency=order_currency,payment_capture=1))
    payment_order_id=payment_order['id']
    context={
        'amount':500,
        'api_key':RAZORPAY_API_KEY,
        'order_id':payment_order_id
    }
    
       
        
    return render(request,'payment.html',context)
def InsertRecord(request):
    
    
    if request.method == 'POST':
       
        now=datetime.datetime.now()
        date=now.strftime("%y-%m-%d")
        id=now.strftime("%y-%m-%d_%H:%M:%S")
        ID=id
        print(id)
        name=request.POST.get('name')
        prn=request.POST.get('prn')
        email=request.POST.get('email')
        mob=request.POST.get('mob')
        addr=request.POST.get('addr')
        yos=request.POST.get('yos')
        branch=request.POST.get('branch')
        ack= ''.join(random.choice('0123456789ABCDEFGabcdefg') for i in range(16))
        ack=id+ack
        print(ack)
        # ack check for same ack
        request.session['ack_no']=ack
        request.session['id']=id
        request.session['email']=email
        #inserting in users
        #old query=""" INSERT INTO users VALUES(%s,%s,%s,%s,%s,%s)"""
        query=""" INSERT INTO form1(userid,ack,date,name,prn,branch,email,mob,yos,addr) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        #id	userid	ack	date	name	prn	branch	email	mob	yos	addr	
        recordTuple = (id,ack,date,name,prn,branch,email,mob,yos,addr)
        cur.execute(query, recordTuple)
        conn.commit()
        print("Record inserted successfully")
        #updating in status to pending
        query=""" INSERT INTO  `verification_status` (userid,ack,status) VALUES(%s,%s,%s)"""
        status="Phase-1:Form Filled"
        recordTuple = (id,ack,status)
        cur.execute(query, recordTuple)
        conn.commit()
        print("Record inserted successfully")

        #payment code here
        messages.success(request,'Successfully Inserted')
        #HttpResponseRedirect('<h1>Record Inserted Please Store Your ACK No: {}</h1>'.format(ack))
        
        
        
        
        #Sedning Mail to ENd user
        subject = 'Successfully resgistered for Phase-1 with user id: '+id
        message = ' Successfully Submitted With ACK no:'+ack+'with ID :'+id
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [email,]
        send_mail( subject, message, email_from, recipient_list ) 
        
        
       
        
        
        return redirect("/upload")
        # return render(request,'upload_doc.html')

    else:
        return render(request, 'index.html')



def home(request):
    return  render(request,'home.html')


# def list_users(request):
#     cur.execute("SELECT * FROM users")
#     data = cur.fetchall()
#     #return list(data)
#     print(list(data))
#     return render(request, 'view.html', {'categories': data})   






# def pendingusers(request):
#     cur.execute("Select * from 'users' u inner join  `verification status` v on v.user_ID = u.user_ID inner join 'verification status of user' s on v.user_ID = s.ID Where s.ID=1; ")
#     data = cur.fetchall()
#     #return list(data)
#     print(list(data))
#     return render(request, 'users_status.html', {'categories': data})  

# def upload(request):
#     if request.method='POST':
#         uploaded_file=requests.FILES['document'] 


def upload(request):
    print("Function called")
    
    id=request.session['id']
    print(id)
    ack=request.session['ack_no']
    print(ack)
    rand= ''.join(random.choice('0123456789ABCDEFGHIJKLMNOabcdefghijklmano') for i in range(9))
    
    if request.POST.get('upload_doc'):
        uploaded_file=request.FILES['doc1']
        print(uploaded_file.name)
        print(uploaded_file.size)
        fs=FileSystemStorage()
        name=fs.save((rand+uploaded_file.name),uploaded_file)
        url=fs.url(name)
        url=str(url)
        #doc1 insertion
        doc_nm="Degree/Provisional Certificate"
        query=""" INSERT INTO docs (`userid`,`ack`, `doc_name`, `doc_link`) VALUES('{0}','{1}','{2}','{3}')""".format(id,ack,doc_nm,url)
        
        recordTuple = (id,1,url)
        cur.execute(query)
        conn.commit()
        print("Doc 1 Inserted Successfully")
        #end

        #doc2 uploading
        uploaded_file=request.FILES['doc2']
        print(uploaded_file.name)
        print(uploaded_file.size)
        fs=FileSystemStorage()
        name=fs.save((rand+uploaded_file.name),uploaded_file)
        url=fs.url(name)
        url=str(url)
        #doc1 insertion
        doc_nm="Gradesheets(of all semesters)"
        query=""" INSERT INTO docs (`userid`,`ack`, `doc_name`, `doc_link`) VALUES('{0}','{1}','{2}','{3}')""".format(id,ack,doc_nm,url)
        cur.execute(query)
        conn.commit()
        print("Doc 1 Inserted Successfully")
    #end

#Photo uploading
        uploaded_file=request.FILES['photo']
        print(uploaded_file.name)
        print(uploaded_file.size)
        fs=FileSystemStorage()
        name=fs.save((rand+uploaded_file.name),uploaded_file)
        url=fs.url(name)
        url=str(url)
        #doc1 insertion
        doc_nm="Photograph"
        query=""" INSERT INTO docs (`userid`,`ack`, `doc_name`, `doc_link`) VALUES('{0}','{1}','{2}','{3}')""".format(id,ack,doc_nm,url)
        cur.execute(query)
        conn.commit()
        print("Doc 2 Inserted Successfully")
    #end

    #doc3 uploading
        uploaded_file=request.FILES['doc3']
        print(uploaded_file.name)
        print(uploaded_file.size)
        fs=FileSystemStorage()
        name=fs.save((rand+uploaded_file.name),uploaded_file)
        url=fs.url(name)
        url=str(url)
        
        doc_nm="Proof of Identity"
        query=""" INSERT INTO docs (`userid`,`ack`, `doc_name`, `doc_link`) VALUES('{0}','{1}','{2}','{3}')""".format(id,ack,doc_nm,url)
        cur.execute(query)
        conn.commit()
        print("Doc 3 Inserted Successfully")
        #dummy email
        email=request.session['email']
        # fp = open(url, 'rb')
        # # msgImage = MIMEImage(fp.read())
        # # fp.close()
        # url=Path(url)
        subject = 'Successfully resgistered for Phase 2: Uploading Documents with user id: '+id
        message = ' Successfully Submitted With ACK no:'+ack+'with ID :'+id
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [email,]
       
      
        f=request.FILES['doc2']
        mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
        mail.attach(f.name, f.read(), f.content_type)
        mail.send()
        

    #end
     
     
        return redirect("/payment")
    return render(request,'upload_doc.html')
    
   
def uploaded(request,id):
    status=id
    id=request.session['id']
    print(id)
    ack=request.session['ack_no']
    ori_status="SUCCESSFULLY PAID"
    query=""" INSERT INTO payment (`userid`,`ack`, `signature`, `status`) VALUES('{0}','{1}','{2}','{3}')""".format(id,ack,status,ori_status)
    cur.execute(query)
    conn.commit()
    return render(request,'uploaded.html')  

def login(request):
    
    
    if request.method == 'POST':
        return redirect("/login/dashboard")
        # uname=request.POST.get('uname')
        # passn=uname=request.POST.get('pass')
        # check="admin"
        # if(uname==check):
        #     if(passn=="123"):
        #         return redirect("/login/dashboard")
 
    else:
        return render(request, 'login.html')


def dashboard(request):
    # data=Dash()
    # query="""SELECT COUNT(*) from `verification status of users`"""
    # cur.execute(query)
    # total=cur.fetchone()
    # print (list(total))


    

    cur.execute("SELECT * FROM form1 ORDER BY id DESC ")
    #cur.execute("Select * from 'users' inner join  `verification status of user` on 'users'.user_ID = `verification status of user`.user_ID")
    data = cur.fetchall()
    # for i in data:
    #     total.append(i)
    

    
    #return list(data)
    # print(list(data))
    # cur.execute("Select * from `verification status of users`")
    # ver_count=cur.fetchall
    
    return render(request, './dashboard2.html', {'categories': data})   
    # return render(request, '')

def viewDocs(request,id):
    print(id)

    
    # query="""SELECT * FROM `user docs` where `user_ID`='{}'""".format(id)
    query="""SELECT * FROM docs where ack='{}' """.format(id)
    # query="""  `user docs`(`user_ID`, `doc_ID`, `doc_link`) VALUES('{0}',{1},'{2}')""".format(id,2,url)
     
    cur.execute(query)
    data = cur.fetchall()
    query="""select email from form1 where ack='{}'""".format(id)
    cur.execute(query)
    email=cur.fetchone() 
    print(email)
    #return list(data)
    print(list(data))
    # cur.execute("Select * from `verification status of users`")
    # ver_count=cur.fetchall
    context={
        'categories':data,
        'ack': id
    }
    return render(request, 'viewDocs1.html', context)

def verify(request,id):
    
    query="""SELECT * FROM form1 where ack='{}' """.format(id)
    # query="""  `user docs`(`user_ID`, `doc_ID`, `doc_link`) VALUES('{0}',{1},'{2}')""".format(id,2,url)
     
    cur.execute(query)
    data = cur.fetchall()
    query="""select email from form1 where ack='{}'""".format(id)
    cur.execute(query)
    email=cur.fetchone() 
    print(email)
    for i in email:
        demo=i
    #return list(data)
    print(list(data))
    # cur.execute("Select * from `verification status of users`")
    # ver_count=cur.fetchall
    context={
        'categories':data,
        
        'email':email
    }
    
    if request.POST:
        subject = 'Successfully Verified Your Document with user id: '+id
        message = 'Verified Your Document with ID :'+id
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [demo,]
        print('done')
       
        f=request.FILES['docF']
        mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [demo])
        mail.attach(f.name, f.read(), f.content_type)
        mail.send()


        print(id)
    return render(request,'verify.html',context)