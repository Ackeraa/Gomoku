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
   if message == 'first':
       ai = Acker()
   else:
       ai = Acker()

   #print(message)
   return message

@app.route('/move', methods=['GET', 'POST'])
def move():
    message = request.args.get('message')
    pos = message.split(',')
    
    return ai.move(pos)

if __name__ == '__main__':
    app.run(debug = True)
