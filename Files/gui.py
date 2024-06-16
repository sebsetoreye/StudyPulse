import tkinter as tk
import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import ollama 

classnames = []
classhours = []
Studyplan = ""

def create_class_inputs():
    num_classes = int(entry_num_classes.get())
    
    # Clear any previous inputs
    for widget in frame_class_inputs.winfo_children():
        widget.destroy()
    
    # Create inputs for each class
    for i in range(num_classes):
        label_class_name = tk.Label(frame_class_inputs, text=f"Class {i+1} name:")
        label_class_name.grid(row=i, column=0, sticky="w")
        
        entry_class_name = tk.Entry(frame_class_inputs)
        entry_class_name.grid(row=i, column=1)
        class_name_entries.append(entry_class_name)
        
        label_study_hours = tk.Label(frame_class_inputs, text="Study hours per week:")
        label_study_hours.grid(row=i, column=2, sticky="w")
        
        entry_study_hours = tk.Entry(frame_class_inputs)
        entry_study_hours.grid(row=i, column=3)
        study_hours_entries.append(entry_study_hours)

def create_study_plan():
    #setting up veriables 
    get_home_time = entry_get_home_time.get()
    num_classes = int(entry_num_classes.get())
    for i in range(num_classes):
      class_name = class_name_entries[i].get()
      classnames.append(class_name)

      class_hours = study_hours_entries[i].get()
      classhours.append(class_hours)

    global Studyplan

    Prompts = f"create a weekly study plan with classes, {classnames}, in the order given the amount of hours that will be given for each class per week is, {classhours}, on week days the time that study starts on is, {get_home_time}, split this into a day by day format"

    print("Creating Plan")
    #connecting to server AI
    StudyPulse = ollama.generate(model='phi3', prompt=Prompts)
    response = StudyPulse['response']
    print(response)
    Studyplan += str(response)


def get_schedule():
    get_home_time = entry_get_home_time.get()
    num_classes = int(entry_num_classes.get())
    print("Number of classes:", num_classes)
    for i in range(num_classes):
        class_name = class_name_entries[i].get()
        classnames.append(class_name)  # Append class name to the list
        print("Class:", class_name)
        class_hours = study_hours_entries[i].get()
        classhours.append(class_hours) # appending class hours to list
        print("class names", classnames)
        print("class hours", classhours)

    print("Time you get home:", get_home_time)
    # Return the list of class names

def Upload():
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    def main():
      """Shows basic usage of the Google Calendar API.
      Prints the start and name of the next 10 events on the user's calendar.
      """
      creds = None
      # The file token.json stores the user's access and refresh tokens, and is
      # created automatically when the authorization flow completes for the first
      # time.
      if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
      # If there are no (valid) credentials available, let the user log in.
      if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
        else:
          flow = InstalledAppFlow.from_client_secrets_file("/home/server/Desktop/StudyPulse/Files/credentials.json", SCOPES)
          creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
          token.write(creds.to_json())

      try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        event = {
            "summary": "Weekly plan",
            "location": "Home",
            "description": Studyplan,
            "colorId": 6,
            "start": {
                "dateTime": "2024-05-29T10:00:00+00:00",
                "timeZone": "Australia/Sydney",
            },
            "end": {
                "dateTime": "2024-05-29T11:00:00+00:00",
                "timeZone": "Australia/Sydney",
            }
        }
        event = service.events().insert(calendarId="primary", body=event).execute()

        print(f"Weekly Planer created {event.get('htmlLink')}")

      except HttpError as error:
        print(f"An error occurred: {error}")

    if __name__ == "__main__":
      main()

def View_study_plan():
    print(Studyplan)

def debugging():
    print(classhours)
    print(classnames)
    get_home_time = entry_get_home_time.get()
    print(get_home_time)


# Create main window
root = tk.Tk()
root.title("Class Schedule")

# Frame for class inputs
frame_class_inputs = tk.Frame(root)
frame_class_inputs.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Number of classes input
label_num_classes = tk.Label(root, text="Number of classes:")
label_num_classes.grid(row=1, column=0, sticky="e")
entry_num_classes = tk.Entry(root)
entry_num_classes.grid(row=1, column=1)

# Button to create class inputs
button_create_inputs = tk.Button(root, text="Create Class Inputs", command=create_class_inputs)
button_create_inputs.grid(row=2, column=0, columnspan=2, pady=5)

# Time you get home input
label_get_home_time = tk.Label(root, text="Time you get home:")
label_get_home_time.grid(row=3, column=0, sticky="e")
entry_get_home_time = tk.Entry(root)
entry_get_home_time.grid(row=3, column=1)

# Button to get data
button_get_schedule = tk.Button(root, text="Get Data", command=get_schedule)
button_get_schedule.grid(row=4, column=0, columnspan=2, pady=10)

# Button to create study plan
button_get_schedule = tk.Button(root, text="Create Study Plan", command=create_study_plan)
button_get_schedule.grid(row=5, column=0, columnspan=2, pady=10)

# Button to view study plan
button_get_schedule = tk.Button(root, text="View Study guide", command=View_study_plan)
button_get_schedule.grid(row=6, column=0, columnspan=2, pady=10)

# Button to upload study plan
button_get_schedule = tk.Button(root, text="Upload study Plan", command=Upload)
button_get_schedule.grid(row=7, column=0, columnspan=2, pady=10)

# Button for Debugging
button_get_schedule = tk.Button(root, text="Debug", command=debugging)
button_get_schedule.grid(row=8, column=0, columnspan=2, pady=10)

# Lists to store dynamically created widgets
class_name_entries = []
study_hours_entries = []

root.mainloop()

