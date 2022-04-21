import http.server
import json
import os
import asyncio
import websockets

#sets the active directory to the directory of the server.py file
os.chdir(os.path.dirname(os.path.realpath(__file__)))

quiz = open("Quiz.html", "r")
quiz = quiz.read()
totalAnswersCorrect = 0
teamAnswersCorrect = {1:0,2:0}
questionBankName = "questionBank.json"
userCorrectData = {}

# creates an http handler that sends the client the quiz html file
class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):#This is 
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        splitrq = self.requestline.split()
        
        questionBank = open(questionBankName, "r")
        quiz = open("Quiz.html", "r")
        questions = questionBank.read()
        quiz = quiz.read()
        quiz = quiz.replace("[{THISTEXTISREPLACEDLATERBYSTUFF:'ok?'}]", questions)
        self.wfile.write(bytes(quiz, "utf-8"))
        #prints the message content
        print("GET request received")
        print("Request line:" + self.requestline)
        print(f"")
        
        
    def do_POST(self):#this is the function that handles POST requests sent from clients
        global userCorrectData
        global totalAnswersCorrect
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        quiz = open("Quiz.html", "r")
        questionBank = open(questionBankName, "r")
        questions = questionBank.read()
        quiz = quiz.read()
        quiz = quiz.replace("[{THISTEXTISREPLACEDLATERBYSTUFF:'ok?'}]", questions)
        self.wfile.write(bytes(quiz, "utf-8"))
        print("POST request received")
        print("Request line:" + self.requestline)
        #prints the message content
        content_length = int(self.headers['Content-Length'])
        messageData = str(self.rfile.read(content_length))
        print(messageData)
        if messageData.startswith("b'"):
            messageData = messageData.replace("b'", "")
        if messageData[-1] == "'":
            messageData = messageData[0:-1]
        print(messageData)
        formattedData = json.loads(messageData)
        print(formattedData)
        
        if formattedData["answerCorrect"]:
            userCorrectData[formattedData["name"]] = formattedData["score"]
            teamAnswersCorrect[formattedData["team"]] += 1
            totalAnswersCorrect += 1
            print(f"{totalAnswersCorrect} correct answers \n Team 1: {teamAnswersCorrect[1]} \n Team 2: {teamAnswersCorrect[2]}")
            for key in userCorrectData.keys():
                print(f"{key}: {userCorrectData[key]}")
        
        
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()



# creates the user server that listens on port 80
server = http.server.HTTPServer(('', 80), MyHandler)



# starts the server
server.serve_forever()

