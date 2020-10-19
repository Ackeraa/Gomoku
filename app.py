from flask import Flask, render_template, request, jsonify
from ai import Acker

app = Flask(__name__)
ai = None

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/start', methods=['GET', 'POST'])
def start():
   message = request.args.get('message')
   global ai
   # 0: white
   # 1: black
   if message == 'first':
       ai = Acker(0)
   else:
       ai = Acker(1)

   #print(message)
   return message

@app.route('/move', methods=['GET', 'POST'])
def move():
    message = request.args.get('message')
    pos = message.split(',')
    
    return ai.move(pos)

if __name__ == '__main__':
    app.run(debug = True)
