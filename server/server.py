import os.path

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os
from binascii import hexlify
import tornado.web
from tornado.options import define, options
import mysql.connector
import datetime
import json

define("port", default=1104, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1", help="database host")
define("mysql_database", default="tickets", help="database name")
define("mysql_user", default="admin", help="database user")
define("mysql_password", default="12345689", help="database password")

mydb = mysql.connector.connect(
    host=options.mysql_host,
    user=options.mysql_user,
    passwd=options.mysql_password,
    database=options.mysql_database
)
mycursor = mydb.cursor(dictionary=True, buffered=True)


class Application(tornado.web.Application):
    def __init__(self):
        # GET METHOD :
        handlers = [
            (r"/getticketmod/([^/]+)", getticketmod),
            (r"/getticketcli/([^/]+)", getticketcli),
            (r"/login/([^/]+)/([^/]+)", login),
            (r"/logout/([^/]+)/([^/]+)", logout),
            # POST METHOD :
            (r"/signup", signup),
            (r"/sendticket", sendticket),
            (r"/restoticketmod", restoticketmod),
            (r"/changestatus", changestatus),
            (r"/closeticket", closeticket),
            (r".*", defaulthandler),
        ]
        settings = dict()
        super(Application, self).__init__(handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def check_user(self,user):
        mycursor.execute("SELECT * from users where username = %s", (user,))
        resuser = mycursor.fetchone()
        if resuser:
            return True
        else:
            return False

    def check_api(self, api):
        mycursor.execute("SELECT * from users where api = %s", (api,))
        resuser = mycursor.fetchone()
        if resuser:
            return resuser['username']
        else:
            return False

    def check_auth(self, username, password):
        mycursor.execute("SELECT * from users where username = %s and password = %s", (username, password))
        resuser = mycursor.fetchone()
        if resuser:
            return True
        else:
            return False

    def check_role(self, api):
        mycursor.execute("SELECT * from users where api = %s", (api,))
        user = mycursor.fetchone()
        if user['role'] == 1:
            return '1'
        elif user['role'] == 2:
            return '2'

class defaulthandler(BaseHandler):
    def get(self):
        output = {'status': 'Wrong Command'}
        self.write(output)

    def post(self, *args, **kwargs):
        output = {'status':'Wrong Command'}
        self.write(output)


class signup(BaseHandler):
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        first_name = self.get_argument('first_name')
        last_name = self.get_argument('last_name')
        if not self.check_user(username):
            api_token = str(hexlify(os.urandom(16)).decode())
            mycursor.execute("INSERT INTO users (username, password, first_name, last_name, api)"
                             " VALUES (%s,%s,%s,%s,%s) ", (username, password, first_name, last_name, api_token))
            mydb.commit()
            user_id = mycursor.lastrowid

            output = {"message": "Signed Up Successfully",
                      "api": api_token,
                      "status": '200'}
            self.write(output)
        else:
            output = {'status': '401'}
            self.write(output)


class login(BaseHandler):
    def get(self, *args, **kwargs):
        if self.check_auth(args[0], args[1]):
            mycursor.execute("SELECT * from users where username = %s and password = %s", (args[0], args[1]))
            user = mycursor.fetchone()
            output = {'status': '200',
                      'api': user['api'],
                      'role': user['role'],
                      'message': 'Logged in Successfully'}
            self.write(output)
        else:
            output = {'status': '401'}
            self.write(output)


class logout(BaseHandler):
    def get(self, *args, **kwargs):
        if self.check_auth(args[0], args[1]):
            output = {'status': '200',
                      'message': 'Logged Out Successfully'}
            self.write(output)
        else:
            output = {'status': '401'}
            self.write(output)


class getticketcli(BaseHandler):
    def get(self, *args, **kwargs):
        if self.check_role(args[0]) == '2':
            username = self.check_api(args[0])
            mycursor.execute("SELECT * from tickets where username = %s", (username, ))
            ticket = mycursor.fetchall()
            number_ticket = len(ticket)

            def myconverter(o):
                if isinstance(o, datetime.datetime):
                    return o.__str__()

            if number_ticket == '0':
                output = {'status': '401'}
                self.write(output)
            else:
                output = {
                    "tickets": "There Are -" + str(number_ticket) + "- Ticket",
                    "code": "200",
                }
                y = 0
                for x in ticket:
                    output['block ' + str(y)] = x
                    y += 1
                self.write(json.dumps(output, default=myconverter))


class getticketmod(BaseHandler):
    def get(self, *args, **kwargs):
        if self.check_role(args[0]) == '1':
            mycursor.execute("SELECT * from tickets")
            ticket = mycursor.fetchall()
            number_ticket = len(ticket)

            if number_ticket == '0':
                output = {'status': '401'}
                self.write(output)
            else:
                output = {
                    "tickets": "There Are -" + str(number_ticket) + "- Ticket",
                    "code": "200",
                }
                y = 0
                for x in ticket:

                    a = {}
                    a["subject"] = x["subject"]
                    a["body"] = x["body"]
                    a["id"] = x["id"]
                    a["answer"] = x["answer"]
                    a["date"] = str(x["date"])
                    a["status"] = x["status"]
                    output['block ' + str(y)] = a
                    y += 1
                print(output)
                self.write(output)


class sendticket(BaseHandler):
    def post(self, *args, **kwargs):
        token = self.get_argument('api')
        subject = self.get_argument('subject')
        body = self.get_argument('body')
        username = self.check_api(token)
        if self.check_user(username):
            mycursor.execute("INSERT INTO tickets (username, subject, body, status,date)"
                             " VALUES (%s,%s,%s,%s,%s) ", (username, subject, body, 'open', datetime.datetime.now()))
            mydb.commit()
            user_id = mycursor.lastrowid

            output = {"message": "Ticket Sent Successfully",
                      "id": str(user_id), "code": "200"}
            self.write(output)
        else:
            output = {'status': '401'}
            self.write(output)


class restoticketmod(BaseHandler):
    def post(self, *args, **kwargs):
        token = self.get_argument('api')
        id = self.get_argument('id')
        answer = self.get_argument('answer')
        username = self.check_api(token)
        if self.check_user(username):
            mycursor.execute("UPDATE tickets set answer= %s where id = %s", (answer, id))
            mydb.commit()

            output = {
                "message": "Response to Ticket With id -" + str(id) + "- Sent Successfully",
                "code": "200",
            }
            self.write(output)
        else:
            output = {'status': '401'}
            self.write(output)


class changestatus(BaseHandler):
    def post(self, *args, **kwargs):
        token = self.get_argument('api')
        id = self.get_argument('id')
        status = self.get_argument('status')
        username = self.check_api(token)
        if self.check_user(username):
            mycursor.execute("UPDATE tickets SET status = %s where id = %s", (status, id))
            mydb.commit()

            output = {
                        "message": "Status Ticket With id -" + str(id) + "- Changed Successfully",
                        "code": "200"
                }
            self.write(output)
        else:
            output = {'status': '401'}
            self.write(output)


class closeticket(BaseHandler):
    def post(self, *args, **kwargs):
        token = self.get_argument('api')
        id = self.get_argument('id')
        username = self.check_api(token)
        if self.check_user(username):
            mycursor.execute("UPDATE tickets SET status = %s where id = %s", ('Close', id))
            mydb.commit()

            output = {
                "message": "Status Ticket With id -" + str(id) + "- Closed Successfully",
                "code": "200"
            }
            self.write(output)
        else:
            output = {'status': '401'}
            self.write(output)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

