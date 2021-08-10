from django.shortcuts import render
import mysql.connector as sql
from django.http import JsonResponse
from django.http import HttpResponseRedirect
import base64
# Create your views here.
login_failed=False
fname=""
def farmerChatbot(request):
    if request.session.get('FID',None)is None:
        return HttpResponseRedirect('/home')
    fid = request.session['FID']
    fname = request.session['fname']
    query = 'SELECT notification from chats where FID=%s'
    response = ""
    noti=False
    try:
        conn = sql.connect(host="localhost",user="root",password="",database="agroxpert")
        cur = conn.cursor()
        cur.execute(query,(fid,))
        result=cur.fetchall()
        for chat in result:
            if chat[0] == "Mail" :
                response="You have New Mail!! Expert have replied to your query"
                noti=True
            elif chat[0] == "Edit":
                response="Expert have Edited Response Please View mail again"
                noti=True
    except Exception as ex:
        print(ex)
        return render(request,"farmer.html",{"res":"Connection is not available"})
    return render(request,'chatbot.html',{"notification":response,"noti":noti,"user":fname})
def expertchat(request):
    if request.session.get('FID',None) is None:
        return HttpResponseRedirect('/home')
    fid=request.session['FID']
    query='SELECT * from chats where FID=%s'
    response=[]
    try:
        conn = sql.connect(host="localhost",user="root",password="",database="agroxpert")
        cur = conn.cursor()
        print(True)
        cur.execute(query,(fid,))
        result=cur.fetchall()
        up = "UPDATE chats set notification=%s where FID=%s"
        curr = conn.cursor()
        curr.execute(up, ("checked", fid))
        for chat in result:
            if chat[1] is not None:
                response.append((chat[3],chat[4],chat[5]))
            else:
                response.append((chat[3],chat[4],"-a"))
    except Exception as ex:
        print(ex)
        conn.commit()
        conn.close()
        return render(request,"farmer.html",{"res":"Connection is not available"})
    conn.commit()
    conn.close()
    return (render(request,"expertchat.html",{"response":response}))
def reply(request):
    if request.session.get('FID',None) is None:
        return render(request,'farmer.html',{"res": "Please Login again Session expired ", "failed": True})
    fid=request.session['FID']
    s_query="SELECT  * from chats where FID= %s"
    response=[]
    try:
        conn = sql.connect(host="localhost",
                           user="root",
                           password="",
                           database="agroxpert")
        cur=conn.cursor()
        cur.execute(s_query,(fid,))
        result=cur.fetchall()
        for chat in result:
            if chat[1] is not None or chat[len(chat)-1] is not None:
                response.append((chat[3],chat[4],chat[5]))
            else:
                response.append((chat[3],chat[4],"-a"))
        print(response)
    except Exception as ex:
        response = str(ex)
    sub="Re: "+request.POST['sub']+ " Question -"+request.POST['qns']+" Reply -"+request.POST['reply']

    return render(request,"expertchat.html",{"response":response,"sub":sub})
def chat(request):
    Reply="none"
    query=""
    if request.session.get('FID', None) is not None:
        fid = request.session['FID']
        fids=(fid,)
        Reply="inside session"
        sqlq="SELECT * from chats where FID=%s"
        try:
            conn = sql.connect(host="localhost",
                               user="root",
                               password="",
                               database="agroxpert")
            cur = conn.cursor()
            cur.execute(sqlq,fids)
            result=cur.fetchall()
            Reply=result
            cur.close()
            request = request.POST
            curs=conn.cursor()
            sqli="INSERT into chats (FID, subject ,chat) values (%s,%s,%s)"
            curs.execute(sqli,(fid,request['sub'],request['Search']))
            conn.commit()
        except Exception as ex:
            Reply=str(ex)
        conn.commit()
        conn.close()
    return JsonResponse({"query":request['Search'],"Reply":Reply})
def home(request):
    if request.session.get('FID',None) is not None:
        del request.session['FID']
        return HttpResponseRedirect('home')
    if request.session.get('AID',None) is not None:
        del request.session['AID']
        return HttpResponseRedirect('home')
    return render(request,'home.html')

def admin(request):
    return render(request,'admin.html')
def farmer(request):
    fname=request.session['fname']
    print(fname,"122")
    return render(request,'farmer.html',{"user" : fname})
def farmerlogin(request):
    res = ""
    login_failed=False
    if request.method=="POST":
        print()
        try:
            conn = sql.connect(host="localhost",user="root",password="",database="agroxpert")
            cur = conn.cursor()
            print(True)
        except Exception as ex:
            print(False)
            return render(request,"farmer.html",{"res":"Connection is not available"})
        met=request.POST
        fid = met['fid']
        pas = met['pas']
        sample_string_bytes = pas.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        password = base64_bytes.decode("ascii")
        print(f"Encoded string: {password}")
        inp = (fid, password)
        sqlq='SELECT * from farmer where FID=%s and pas=%s'
        cur.execute(sqlq,inp)
        fetchRes=cur.fetchall()
        if len(fetchRes) == 1:
            login_failed = False
            request.session['FID']=fid
            print(fetchRes[0][1])
            request.session['fname']=fetchRes[0][1]
            return HttpResponseRedirect('farmer')

        else:
            login_failed=True
            res = "Unable to Signin Password or farmer Id entered is incorrect"
        print(res,login_failed)
        conn.commit()
        conn.close()
    return render(request,'farmer.html',{"res": res,"failed":login_failed})
def signin(request):
    res=""
    login_failed = False

    if request.method=="POST":
        print()
        try:
            conn = sql.connect(host="localhost",user="root",password="",database="agroxpert")
            cur = conn.cursor()
            print(True)
        except Exception as ex:
            print(False)
            return render(request,"admin.html",{"res":"Connection is ot available"})
        met=request.POST
        aid=met['aid']
        pas=met['pas']
        print("Encoded Password, AID",pas , aid)
        sample_string_bytes = pas.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        password = base64_bytes.decode("ascii")
        print(f"Encoded string: {password}")
        inp=(aid,password)
        sqlq='SELECT * from admin where AID=%s and pas =%s'
        cur.execute(sqlq,inp)
        fetchRes=cur.fetchall()
        print(fetchRes)
        if len(fetchRes)==1:
            login_failed = False
            request.session['AID']=aid
            return HttpResponseRedirect('administration/')
        else:
            login_failed=True
            res = "Unable to Signin Password or farmer Id entered is incorrect"
        print(res,login_failed)
        conn.commit()
        conn.close()
    return render(request,'admin.html',{"res":res,"failed":login_failed})
def farmerRegister(request):
    res = ""
    failed=False
    if request.method == "POST":
        try:
            conn = sql.connect(host="localhost",
                               user="root",
                               password="",
                               database="agroxpert")
            cur = conn.cursor()
            met = request.POST
            fid = met['fid']
            fname = met['fname']
            pas = met['pas']
            phone = met['phone']
            sample_string_bytes = pas.encode("ascii")
            base64_bytes = base64.b64encode(sample_string_bytes)
            password = base64_bytes.decode("ascii")
            cur.execute('insert into farmer values(%s, %s, %s, %s)', (fid, fname, phone, password))
            conn.commit()
            conn.close()
            request.session['FID'] = fid
            return HttpResponseRedirect('farmerLogin')
        except Exception as ex:
            failed = True
            res="Farmer ID already Registred Please Login again"
    return render(request,'farmerLogin',{"res": res, "failed": failed})

def signup(request):
    res = ""
    failed=False
    if request.method == "POST":
        try:
            conn=sql.connect(host="localhost",user="root",password="",database="agroxpert")
            cur = conn.cursor()
            met = request.POST
            aid = met['aid']
            email = met['email']
            pas = met['pas']
            name = met['name']
            sample_string_bytes = pas.encode("ascii")
            base64_bytes = base64.b64encode(sample_string_bytes)
            password = base64_bytes.decode("ascii")
            print(f"Encoded string: {password}")
            inp = (aid, name, email, password)
            cur.execute('insert into admin values(%s,%s,%s,%s)', inp)
            conn.commit()
            conn.close()
            request.session['AID'] = aid
            return HttpResponseRedirect('adminLogin')
        except Exception as ex:
            failed = True
            res = "Expert ID already Registred Please Login again"
    return render(request,'/adminLogin',{"res": res, "failed": failed})
