from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse,HttpResponseRedirect
from sklearn.preprocessing import LabelEncoder,StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesRegressor
from django.core.mail import send_mail
from django.core.mail import EmailMessage
#import os
#import numpy as np
import sqlite3
# Create your views here.
def take_data(request):
    if "GET" == request.method:
        return render(request,"data/index.html")
    elif request.POST:
        #csvfile = request.FILES['csv_file']
        
        name0 = request.POST['name0']
        age0 = request.POST['age0']
        
        sex= request.POST.get('sex0')
        child0 = request.POST['child0']
        smoker = request.POST.get('smoker')
        region = request.POST.get('region')
        bmi = request.POST['bmi0']
        
        email0 = request.POST['email0']
        mob0 = request.POST['mob0']
        city = request.POST['city']
        zip_code = request.POST['zip_code']
        #df = pd.read_csv(csvfile)
        df = pd.read_csv('D:/EDUCATION/STUDY/django/medp0/new_dataset.csv')
        df0 = df.dropna()
        df0['bmi_int'] = df0['bmi'].apply(lambda x: int(x))
        le_sex = LabelEncoder()
        le_smoker = LabelEncoder()
        le_region = LabelEncoder()
        
        df0['sex'] = le_sex.fit_transform(df['sex'])
        df0['smoker'] = le_smoker.fit_transform(df['smoker'])
        df0['region'] = le_region.fit_transform(df['region'])
        variables=['sex','smoker','region','age','bmi','children']
        X = df0[variables]
        sc = StandardScaler()
        X = sc.fit_transform(X) 
        Y = df0['charges']
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
        
        regressor0 = ExtraTreesRegressor(n_estimators = 200)
        regressor0.fit(X_train,y_train)
        
        #y_train_pred = regressor0.predict(X_train)
        #y_test_pred = regressor0.predict(X_test)
        
        #importances = regressor0.feature_importances_
        #std = np.std([tree.feature_importances_ for tree in regressor0.estimators_],axis=0)
        #indices = np.argsort(importances)[::-1]
        #importance_list = []
        
        data0 = [sex,smoker,region,age0,bmi,child0]
        #billy=billy.insert(0,le_region.transform(region))
        #billy=billy.insert(0,le_smoker.transform(smoker))
        #billy=billy.insert(0,le_sex.transform(gender))
        #billy[0] = le_sex.transform([billy[0]])[0]
        #billy[1] = le_smoker.transform([billy[1]])[0]
        #billy[2] = le_region.transform([billy[2]])[0]
        
        X = sc.transform([data0])
        
        data0 = regressor0.predict(X)[0]
        #name1 = 'Cost for '+name0+' is : ',data0
        name2 = 'YOUR COST IS :',data0

        sex0=int(sex)
        smoker0=int(smoker)
        region0 = int(region)
        
        sex_map = {0:'male',1:'female'};smoker_map = {0:'yes',1:'no'};region_map = {0:'southwest',1:'southeast',2:'northwest',3:'northeast'}
        sex1 = sex_map[sex0];smoker1 = smoker_map[smoker0];region1 = region_map[region0]
        my_db =sqlite3.connect('person_details.sqlite3')
        my_cur = my_db.cursor()
        sql1="INSERT INTO person(name,age,children,gender,smoker,region,bmi,email,mobile,city,zip_code) VALUES('"+name0+"','"+age0+"','"+child0+"','"+sex1+"','"+smoker1+"','"+region1+"','"+bmi+"','"+email0+"','"+mob0+"','"+city+"','"+zip_code+"');"
        my_cur.execute(sql1)

        my_db.commit()
        import smtplib
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login("technomancer7629@gmail.com","naz@technomancer7629")
        message = 'Hello this is AVITS SOLUTIONS ',name2
        message1 = repr(message)
        message2 = "HELLO THIS IS AVITS SOLUTIONS.YOUR COST IS",str(data0)
        s.sendmail("technomancer7629@gmail.com",email0,str(message2))
        '''message0 = 'Hello this is AVITS SOLUTIONS ',name2
        email2 = EmailMessage('insurance cost',message0,to=['safakat@avitssolutions.com'])'''

        return HttpResponse(message2)
    
def upload_data(request):
    if "GET" == request.method:
        return render(request,"data/upload_data.html")
    elif request.POST and request.FILES:
        csvfile = request.FILES['csv_file']
        df = pd.read_csv(csvfile)
        df.to_csv('new_dataset.csv')
        return HttpResponse("File upload done..")
        
        

def log_in(request):
    if "GET" == request.method:
        return render(request,"data/login.html")
    elif request.POST:
        user_id = str(request.POST['user_id'])
        passwd = str(request.POST['passwd'])
        admin_db=sqlite3.connect('admin_details.sqlite3')
        admin_curs=admin_db.cursor()
        admin_curs.execute('''SELECT userid FROM details;''')
        record0 = admin_curs.fetchall()
        user_id0 = str(record0[0][0])
        admin_curs.execute('''SELECT password FROM details;''')
        record1=admin_curs.fetchall()
        passwd0 = str(record1[0][0])
        
        if user_id == user_id0:
            if passwd == passwd0:
                return render(request,"data/template.html")
            return render(request,"data/login.html")
        else:
            return render(request,"data/login.html")

def login(request):
    if "GET" == request.method:
        return render(request,"data/login.html")

def template(request):
    if "GET" == request.method:
        return render(request,"data/template.html")