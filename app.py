from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

#we have an instance of satisfaction_survey renamed as survey
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

#session: used to store information from a previous request, relies
# on the super key


@app.get("/")
def start_survey():
    """Shows title and instructions of survey and button"""
    title = survey.title
    instructions = survey.instructions

    return render_template(
        "survey_start.html",
        title=title,
        instructions=instructions

    )


@app.post('/begin')
def handle_start_button():
    """When user hits start button, redirects to start of questions."""
    return redirect ("/questions/0")


@app.get('/questions/<int:question_num>')
def question_router(question_num):
    """Grabs desired route and sends user to desired question."""


    question = survey.questions[question_num]


    # loop in question.html via Jinja loop for those choicces

    return render_template(
        "question.html",
        question=question,
        question_num=question_num
    )

@app.post('/answer')
def get_answer():
    session['answer'] = request.form['answer']
    print("session is:", session)

    question_num = int(request.form['question-num'])
    print('question_num is', question_num)
    next_question_num = question_num + 1

    if survey.questions.get(next_question_num, False):
        # If there is another question, send user to it
        return redirect(f"/questions/{next_question_num}")
    else:
        # Otherwise, redirect user to thank-you
        return redirect('/completion.html')


@app.get('/completion.html')
def thank_user():
    

