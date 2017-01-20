from flask import Flask, render_template, url_for, request
from app import app
import redis

# Connect to redis data store
r = redis.StrictRedis(host='localhost',port=6379,db=0,charset="utf-8",decode_responses=True)

@app.route("/", methods=['GET', 'POST'])
def hello():
    bootstrapCSS = url_for('static', filename='css/bootstrap.min.css')
    favicon = url_for('static', filename='favicon.ico')
    createLink = url_for('create')
    modifyLink = url_for('modify')
    return render_template("main.html", **locals())

@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        # send the user the form
        return render_template('CreateQuestion.html')
    elif request.method == 'POST':
        # read form data and save it 
        title = request.form['title']
        question = request.form['question']
        answer = request.form['answer']

        # Store data in data store
        # Key name will be whatever title they typed in : Question
        # e.g. music:question  countries:question
        # e.g. music:answer countries:answer
        r.set(title + ':question', question)
        r.set(title + ':answer', answer)

        return render_template('CreatedQuestion.html', question = question)
    else:
        return "<h2>Invalid request</h2>"

@app.route("/modify", methods=['GET', 'POST'])
def modify():
    return "<h2>Modify Page</h2>"

@app.route('/question/<title>', methods=['GET', 'POST'])
def question(title):
    if request.method == 'GET':
        # send the user the form

        # Read question from data store
        question = r.get(title + ':question')

        return render_template('AnswerQuestion.html', question = question)
    elif request.method == 'POST':
        # User has attempted to answer. Check if they're correct
        submittedAnswer = request.form['answer']

        # Read answer from data store
        answer = r.get(title + ':answer')

        if submittedAnswer.strip() == answer:
            return render_template('Correct.html')
        else:
            return render_template('Incorrect.html', 
                submittedAnswer = submittedAnswer, 
                answer = answer)
    else:
        return "<h2>Invalid request</h2>"