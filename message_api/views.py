from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from message_api.models import Message, LoggedInUsers
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
import secrets

@csrf_exempt # Disable csrf authentication
## Send a message
def sendMessage(request):
    
    # Extracting json from request
    data = json.loads(request.body)

    # Defining response
    response = "message sent successfully"
    
    # Trying to save the message into the DB
    try:
        Message(
            sender = data["sender"], 
            receiver = data["receiver"], 
            subject = data["subject"], 
            message = data["message"]
        ).save()
    

    # Changing response incase of failure
    except:
        response = "Something went wrong while sending the message"
    
    # Returning response
    return HttpResponse(response)
    
@csrf_exempt # Disable csrf authentication
## Get all messages for a specific user
def getMessages(request):
    
    # Extracting json from request
    data = json.loads(request.body)

    # Checking if user logged in or having the right token
    if checkToken(data["user"], data["token"]):

        try:
            # Extracting specific message from DB
            message = Message.objects.filter(receiver = data["user"])

            # Converting model to json
            serializedJson = serializers.serialize('json', message)

            response =  HttpResponse(serializedJson, content_type="text/json-comment-filtered")

        except:

            response = HttpResponse("No messages have been found")

    else:

        response = HttpResponse("Please login first!")

    # Returning response
    return response
    

@csrf_exempt # Disable csrf authentication
## Get all unread messages for a specific user
def getUnreadMessages(request):

    # Extracting json from request
    data = json.loads(request.body)

    # Checking if user logged in or having the right token
    if checkToken(data["user"], data["token"]):

        # Extracting specific message from DB
        message = Message.objects.filter(receiver = data["user"]).filter(unread = True)

        # Converting model to json
        serializedJson = serializers.serialize('json', message)
            
        response =  HttpResponse(serializedJson, content_type="text/json-comment-filtered")

    else:

        response = HttpResponse("Please login first!")
    
    # Returning response
    return response
    
@csrf_exempt # Disable csrf authentication
## Get one message for a specific user
def readMessage(request):
  
    # Extracting json from request
    data = json.loads(request.body)

    try:

        # Extracting specific message from DB
        message = Message.objects.filter(pk = data["messageID"])

        # Mark the message as read
        markRead(message)

        response = HttpResponse(serializers.serialize('json', message), content_type="text/json-comment-filtered")
    
    except:

        response = HttpResponse("Message wasn't found")

    # Returning response
    return response

@csrf_exempt # Disable csrf authentication
## Delete one message for owner or receiver
def deleteMessage(request):
    
    # Extracting json from request
    data = json.loads(request.body)

    # Defining response
    response = HttpResponse("Message Deleted Successfully")
    
    # Extracting specific message from DB
    message = Message.objects.filter(pk = data["messageID"])

    # Converting model to json
    serializedJson = json.loads(serializers.serialize('json', message)[1:-1])

    # Trying to delete the message
    try:
        # Check if the user is the sender or reciever of the message
        if serializedJson["fields"]["sender"] == data["user"] or serializedJson["fields"]["receiver"] == data["user"]:
    
            message.delete()

    # Changing response incase of failure
    except:
        response = HttpResponse("Something went wrong while trying to delete the message")

    # Returning response
    return response


@csrf_exempt # Disable csrf authentication
## Register into the system for future login
def register(request):
    
    # Extracting json from request
    data = json.loads(request.body)

    # Defining response
    response = HttpResponse("You have registered successfully")

    # Trying to create a user
    try:
        User.objects.create_user(data["username"], data["email"], data["password"])

    except:
        response = HttpResponse("User already exists")

    # Returning Response
    return response


@csrf_exempt # Disable csrf authentication
## Login into the system to receive a token
def login(request):

    # Extracting json from request
    data = json.loads(request.body)

    # Defining response
    try:
        user_auth = authenticate(username = data["username"], password = data["password"])

        # Checking if user exists
        if user_auth is not None:

            # Creating a token
            token = secrets.token_hex(16)
            
            # Saving the token with the username to the DB
            saveLoginToken(data["username"], token)

            # Defining response with the token
            response = HttpResponse(token)

        else:

            # Defining response for error
            response = HttpResponse("username or password are incorrect")

    except e:
        response = HttpResponse(e)
    # Returning response
    return response

## Creating a token user connection for future login
def saveLoginToken(username, tk):

        # Creating a token - user connection in the DB
        LoggedInUsers(
            user = username,
            token = tk
        ).save()

## Checks if the token and user are connected
def checkToken(user, tk):

    try:
        # Trying to find user with token
        LoggedInUsers.objects.filter(user = user).filter(token = tk)

        return True

    except:

        return False

## Checks the date if 30 minutes have passed deletes the token
def deleteToken():

    print("m")

## Mark a specific message as read
def markRead(message):

    # Update the unread field to false
    message.update(unread = False)
    
