import requests
import os
import time
import platform
import sys
import json

PARAMS = CMD = USERNAME = PASSWORD = API = ROLE = ""
HOST = "127.0.0.1"
PORT = "1104"


def __postcr__():
    return "http://"+HOST+":"+PORT+"/"+CMD+"?"


def __api__():
    return "http://" + HOST + ":" + PORT + "/" + CMD + "/" + API


def __authgetcr__():
    return "http://"+HOST+":"+PORT+"/"+CMD+"/"+USERNAME+"/"+PASSWORD


def print_status_ticket(r):
    print(str(r['message']))


def print_tickets(r):
    z = 0
    num = int(r["tickets"].split('-')[1])
    ID = ''
    if num == 0:
        ID = 'back'
    else:
        while True:
            clear()
            x = []
            z = 0
            print('SHOW TICKETS : \n')
            while z < num:
                data = r["block {}".format(z)]
                print(str(data["id"]) + " - " + str(data["subject"]) + " @ " + str(data["date"]) + " \n")
                print("TICKET IS -->   " + str(data["body"]) + ":")
                if not str(data["answer"]) == 'None':
                    print("- ANSWER IS :" + str(data["answer"]))
                print("\n")
                print("-"*20)
                x.append(str(data["id"]))
                z += 1
            print("ENTER ID TICKET FOR BACK ENTER back : ")
            ID = sys.stdin.readline()[:-1]
            if ID in x:
                break
            elif ID == 'back':
                break
            else:
                print("ID IS INCORRECT TRY AGAIN")
                time.sleep(2)

    return str(ID)


def show_funk_ticket():
    print("ID TICKET : " + ID + "\n")
    if ROLE == '1' :
        print("""What Do You Prefer To Do :
        1. Answer Ticket
        2. Change Status Ticket
        3. Back
        """)
    else:
        print("""What Do You Prefer To Do :
        1. Close Ticket
        2. Back
        """)


def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def show_func():
    if ROLE == '2':
        print("USERNAME : "+USERNAME+"\n"+"API : " + API + "\n" + "!YOU ARE NORMAL USER !")
        print("""What Do You Prefer To Do :
        1. Send Ticket
        2. Show Tickets
        3. Logout
        4. Exit
        """)
    elif ROLE == '1':
        print("USERNAME : "+USERNAME+"\n"+"API : " + API + "\n" + "!YOU ARE ADMIN !")
        print("""What Do You Prefer To Do :
        1. Send Ticket
        2. Show Tickets
        3. Logout
        4. Exit
        """)


while True:
    clear()
    print("""WELCOME TO TICKET CLIENT
    Please Choose What You Want To Do :
    1. signin
    2. signup
    3. exit
    """)
    status = sys.stdin.readline()
    if status[:-1] == '1':
        clear()
        while True:
            print("USERNAME : ")
            USERNAME = sys.stdin.readline()[:-1]
            print("PASSWORD : ")
            PASSWORD = sys.stdin.readline()[:-1]
            CMD = "login"
            r = requests.get(__authgetcr__()).json()
            if str(r['status']) == '200':
                clear()
                print("USERNAME AND PASSWORD IS CORRECT\nLogging You in ...")
                API = str(r['api'])
                ROLE = str(r['role'])
                time.sleep(1)
                break
            else:
                clear()
                print("USERNAME AND PASSWORD IS INCORRECT\nTRY AGAIN ...")
                time.sleep(1)
        while True:
            clear()
            show_func()
            func_type = sys.stdin.readline()
            if func_type[:-1] == '1':
                clear()
                CMD = "sendticket"
                print("ENTER SUBJECT TICKETS : ")
                SUBJECT = sys.stdin.readline()[:-1]
                print("ENTER TICKET : ")
                BODY = sys.stdin.readline()[:-1]
                PARAMS = {'api': API, 'subject': SUBJECT, 'body': BODY}
                data = requests.post(__postcr__(), PARAMS).json()
                print_status_ticket(data)
                input("Press Any Key To Continue ...")
            if func_type[:-1] == '2':
                while True:
                    clear()
                    if ROLE == '1':
                        CMD = "getticketmod"
                    elif ROLE == '2':
                        CMD = "getticketcli"

                    data = requests.get(__api__()).json()

                    ID = print_tickets(data)
                    print(ID)
                    if ID == "back":
                        break
                    else:
                        while True:
                            clear()
                            show_funk_ticket()
                            func_type = sys.stdin.readline()
                            if ROLE == '1':
                                if func_type[:-1] == '1':
                                    clear()
                                    CMD = "restoticketmod"
                                    print("ENTER ANSWER : ")
                                    ANSWER = sys.stdin.readline()[:-1]
                                    PARAMS = {'api': API, 'id': int(ID), 'answer': ANSWER}
                                    data = requests.post(__postcr__(), PARAMS).json()
                                    print_status_ticket(data)
                                    input("Press Any Key To Continue ...")
                                elif func_type[:-1] == '2':
                                    clear()
                                    CMD = "changestatus"
                                    print("ENTER STATUS : ")
                                    STATUS = sys.stdin.readline()[:-1]
                                    PARAMS = {'api': API, 'id': int(ID), 'status': STATUS}
                                    data = requests.post(__postcr__(), PARAMS).json()
                                    print_status_ticket(data)
                                    input("Press Any Key To Continue ...")
                                else:
                                    break
                            else:
                                if func_type[:-1] == '1':
                                    clear()
                                    CMD = "closeticket"
                                    PARAMS = {'api': API, 'id': ID}
                                    data = requests.post(__postcr__(), PARAMS).json()
                                    print_status_ticket(data)
                                    input("Press Any Key To Continue ...")
                                elif func_type[:-1] == '2':
                                    break

            elif func_type[:-1] == '3':
                break
            elif func_type[:-1] == '4':
                sys.exit()

    elif status[:-1] == '2':
        clear()
        while True:
            print("To Create New Account Enter The Specifications")
            print("USERNAME : ")
            USERNAME = sys.stdin.readline()[:-1]
            print("PASSWORD : ")
            PASSWORD = sys.stdin.readline()[:-1]
            print("FIRST NAME : ")
            FIRST_NAME = sys.stdin.readline()[:-1]
            print("LAST NAME :")
            LAST_NAME = sys.stdin.readline()[:-1]
            CMD = "signup"
            clear()
            PARAMS = {'username': USERNAME, 'password': PASSWORD,
                      'first_name': FIRST_NAME, 'last_name': LAST_NAME}
            r = requests.post(__postcr__(), PARAMS).json()
            if str(r['status']) == "200":
                print("Your Acount Is Created\n"+"Your Username :"+USERNAME)
                time.sleep(2)
                break
            else:
                print(r['status']+"\n"+"Try Again")
                input("Press Any Key To Continue ...")
                clear()

    elif status[:-1] == '3':
        sys.exit()
    else:
        print("Wrong Choose Try Again")
