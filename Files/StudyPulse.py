import os
import openai
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import ollama

#creating an array for the amount of classes
Classes = []
Class_name = []
Class_due = []
Study_time = []
Time_home = []


#Veriables
X = 0
SP = "  "
Studyplan = ""


print("Hello are you getting already saved data or creating a new study plan?")
print("if it is the first option type in 1, if you are creating a new study plan type in 2")
Ac = input(": ")

if Ac == "1":
    (
        print("test")
    )

else:
        print("Creating a new Account, enter a name")
        Account = input(": ")
        

        #Getting the Time you are home
        print("Enter the Time you would get home every day, EG: 3pm")
        T = input(": ")
        Time_home.append(T)
        print(SP)


        #Getting the class number
        print("How many classes do you have? ")
        C = input(": ")
        C = int(C)

        #inputting into the array
        while X < C:
            Classes.append(int(X))
            X += 1

        X = 0
        CN = 1
        print(SP)

        for x in Classes:
            print("Enter the name of your", CN, "Class")
            N = input(": ")
            Class_name.append(N)
            print(SP)
            CN += 1

        print(SP)

        for x in Classes:
            print(SP)
            print("Enter the Due-date/Test-date for", Class_name[X], "EG: 9/6, M/D")
            D = input(": ")
            X += 1
            Class_due.append(D)
    
        X = 0
        print(SP)

        for x in Classes:
            print(SP)
            print("How many hours a week do you want to study", Class_name[X],"?")
            H = input(": ")
            X += 1
            Study_time.append(H)
    




        #Debugging
        print("##### DEBUGGING ######")
        print(Time_home)
        print("The class number array is: ", Classes)
        print("The class name array is: ", Class_name)
        print("The class due array is: ", Class_due)
        print("Number of hours array is ", Study_time)
        print("Account is", Account)



        #AI creating a weekly calender list
        global Studyplan

        Prompts = f"create a weekly study plan with classes, {Class_name}, in the order given the amount of hours that will be given for each class per week is, {Study_time}, on week days the time that study starts on is, {Time_home}, split this into a day by day format"

        print("Creating Plan")
        #connecting to server AI
        StudyPulse = ollama.generate(model='phi3', prompt=Prompts)
        response = StudyPulse['response']
        print(response)
        Studyplan += str(response)

        # If modifying these scopes, delete the file token.json.
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file(r"C:\Users\sebas\OneDrive\Desktop\StudyPulse\Files\credentials.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            service = build("calendar", "v3", credentials=creds)

            event = {
                "summary": "Weekly plan",
                "location": "Home",
                "description": Studyplan,
                "colorId": 6,
                "start": {
                    "dateTime": "2024-05-29T10:00:00+00:00",
                    "timeZone": "Australia/ACT",
                },
                "end": {
                    "dateTime": "2024-05-29T11:00:00+00:00",
                    "timeZone": "Australia/ACT",
                }
            }
            event = service.events().insert(calendarId="primary", body=event).execute()

            print(f"Weekly Planer created {event.get('htmlLink')}")


        except HttpError as error:
            print(f"An error occurred: {error}")
