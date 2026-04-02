from django.shortcuts import render
import MySQLdb
from django.http import HttpResponse
import random

# Create your views here.

def home(request):
    return render(request,'home.html')

def create_acc(request):
    if request.method=='POST':
        full_name=request.POST.get('fullname')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        address = request.POST.get('address')
        account_type=request.POST.get('accountType')
        deposit = request.POST.get('deposit')

        account_number= str(random.randint(1000000000,999999999999))

        con=MySQLdb.Connect(user="root",
                        host="localhost",
                        database="django",
                        password="Gopal@123")
        
        cursor=con.cursor()
        sql= '''create table if not exists account(id int auto_increment primary key,
        account_number varchar(50) unique, 
        full_name varchar(20),
        dob DATE,
        gender varchar(20),
        mobile varchar(15),
        email varchar(20),
        address TEXT,
        account_type varchar(20),
        deposit DECIMAL(10,2) )
            
            '''
        cursor.execute(sql)

        data=''' insert into account( account_number,full_name,dob,gender,mobile,email,address,account_type,deposit) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
        
        values= (account_number,full_name,dob,gender,mobile,email,address,account_type,deposit)

        cursor.execute(data,values)
        con.commit()
        cursor.close()
        con.close()
        return HttpResponse(f'<h1>account created. Account number is {account_number}</h1> ')
    
    return render(request,'form.html')
    


def deposite(request):
    if request.method=='POST':
        account_number = request.POST.get('account_number')
        amount = int(request.POST.get('amount'))

        con=MySQLdb.Connect(user="root",
                        host="localhost",
                        database="django",
                        password="Gopal@123")
        
        cursor =con.cursor()
        cursor.execute('select deposit from account where account_number =%s',(account_number,))

        res=cursor.fetchone()
        if not res:
            return HttpResponse('<h1>Account not found</h1>')
        
        balance=float(res[0])
        up_balance = balance + amount

        cursor.execute('update account set deposit = %s where account_number =%s',(up_balance,account_number))

        con.commit()
        cursor.close()
        con.close()

        return HttpResponse(f'<h1>Deposite Successfull,, UPDATE Balance:{up_balance}')
    
    return render(request,'deposit_form.html')
    


def withdraw(request):
    if request.method=='POST':
        account_number = request.POST.get('account_number')
        amount = int(request.POST.get('amount'))


        con=MySQLdb.Connect(user="root",
                        host="localhost",
                        database="django",
                        password="Gopal@123")

        cursor = con.cursor()
        cursor.execute('select deposit from account where account_number=%s',(account_number,))

        res=cursor.fetchone()
        if not res:
            return HttpResponse('<h1>Account not fount</h1>')

        balance=float(res[0])

        if amount > balance:
            return HttpResponse('<h1> Insufficient Balance')

        up_balance= balance - amount 

        cursor.execute('update account set deposit =%s where account_number=%s',(up_balance,account_number))

        con.commit()

        cursor.close()
        con.close()

        return HttpResponse(f'<h1>Withdraw successfull and Reamaining Balance: {up_balance}')
    
    return render(request,'withdraw_form.html')

