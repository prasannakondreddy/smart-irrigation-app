from django.shortcuts import render,HttpResponse
import requests
import pymongo
import json
import os
from twilio.rest import Client
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,HttpResponsePermanentRedirect
# added(switch user)
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
# from fusioncharts import FusionCharts
# from django.views.decorators.csrf import csrf_exempt

from twilio.twiml.messaging_response import MessagingResponse

#added (switch user) fun

#signup fun
def sign_up(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request,'Account created Succesfully')
            fm.save()
        
    else:
        fm = SignUpForm()
    return render(request,'signup.html',{'form':fm})

#login fun
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upwd=fm.cleaned_data['password']
                user=authenticate(username=uname,password=upwd)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in successfully!')
                    return HttpResponsePermanentRedirect('/home')
        else:
            fm = AuthenticationForm()
        return render(request,'login.html',{'form':fm})
    else:
        return HttpResponseRedirect('/home')
#logout fun

def user_logout(request):
    logout(request)
    return HttpResponsePermanentRedirect('/login')

# from pymongo import MongoClient
# client = pymongo.MongoClient('mongodb://165.22.222.96:27017')
# db = client['our']

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request,'index.html')
    else:
        return HttpResponsePermanentRedirect('/login')
    # cursor=db.our.find()
    # print(cursor)
    # Dict={"day":[],"temp":[]}
    # for data in cursor:
    #     print(data)
    #     Dict["day"].append(data['_day'])
    #     Dict["temp"].append(data['temperature'])
           
    # print(Dict['day'][2])
    # context={
    #     "dict":Dict,
    #     "day":Dict['day'],
    #     "temp":Dict['temp']
    # }
    Dict={"aa":[],"bb":[]}
    for a in range(7):
        Dict["aa"].append(a)
        Dict["bb"].append(a+3)


    return render(request,'index.html')

# @csrf_exempt
# def reply(request):
#     resp = MessagingResponse()

#     # Add a text message
#     msg = resp.message("Check out this sweet owl!")

#     # Add a picture message
#     msg.media("https://demo.twilio.com/owl.png")

#     return HttpResponse(str(resp))

def forecast(request):
    key='STL47icGAl6RFMPwyoRexeRl34uLnzdZ'
    locKeyReq=requests.get('https://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey='+key+'&q=28%2C77')
    
    locdata=json.loads(locKeyReq.content)
    
    locKey=locdata['Key']
    print(locKey)

    req=requests.get('http://dataservice.accuweather.com/currentconditions/v1/'+locKey+'?apikey='+key+'&details=true')
    data=json.loads(req.content)
    temp=data[0]['Temperature']['Metric']['Value']
    precipitation=data[0]['PrecipitationSummary']['Precipitation']['Metric']['Value']
    humidity=data[0]['RelativeHumidity']
    uvIndex=data[0]['UVIndex']
    posts={
        "temp":temp,
        "precipitation":precipitation,
        "humidity":humidity,
        "uvIndex":uvIndex
    }
    account_sid = 'ACaac7876c9dd88571de990f5b39525293'
    auth_token = '0e360095573216920584fd6889182934'
    if(temp>10):
      client = Client(account_sid, auth_token)
  
      message = client.messages \
          .create(
              body="Alert! The temperature is "+str(temp),
              from_='+19377293887',
              to='+918341885927'
          )

      print(message.sid)
    
    return render(request,'forecast.html',posts)

def predict(request):
    return render(request,'predict.html')

def schedule(request):
    return render(request,'schedule.html')






    