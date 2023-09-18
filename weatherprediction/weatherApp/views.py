from django.shortcuts import render
from weatherApp.models import users
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,confusion_matrix
# Create your views here.
def loginview(request): 
    return render(request,'login.html')

def registerview(request):
    return render(request,'register.html')

def saveuser_view(request):
    userName=request.POST["username"]
    passWord=request.POST["password"]
    Name=request.POST["name"]
    phoneNumber=request.POST["phone"]
    email=request.POST["email"]
    address=request.POST["address"]

    newuser=users(username=userName,password=passWord,name=Name,phone=phoneNumber,email=email,address=address)
    newuser.save()
    return render(request,'login.html')

def userlogin_view(request):
    userName=request.POST["username"]
    passWord=request.POST["password"]

    uname=users.objects.filter(username=userName)

    for u in uname:
        if u.password == passWord:
            return render(request,'home.html')
        else:
            
            return render(request,'login.html')

def checkweatherview(request):
    Precipitation=request.POST["precipitation"]
    Maxtemp=request.POST["maxtemp"]
    Mintemp=request.POST["mintemp"]
    Wind=request.POST["wind"]

    dset=pd.read_csv("seattle-weather.csv")
    x=dset.iloc[:,1:-1]
    y=dset.iloc[:,-1]
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.10) 
    model=RandomForestClassifier(random_state=48)
    model.fit(x_train,y_train)
    y_predicted=model.predict(x_test)
    rf_cm=confusion_matrix(y_predicted,y_test)
    data=[Precipitation,Maxtemp,Mintemp,Wind]
    reshaped_data=np.reshape(data,(1,-1))
    predicted_result=model.predict(reshaped_data)
    print(predicted_result)

    return render(request,'home.html',{'result':predicted_result[0]})

