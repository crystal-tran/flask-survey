from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

#we have an instance of satisfaction_survey renamed as survey
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# session: used to store information from a previous request, relies
# on the super key


@app.get("/")
def start_survey():
    """Dispalys title and instructions for survey"""
    title = survey.title
    instructions = survey.instructions

    return render_template(
        "survey_start.html",
        title=title, # could do title=survey.title here
        instructions=instructions
    )


@app.post('/begin')
def handle_start_button():
    """When user hits start button, clears session cookie and
    redirects to first question."""

    # add session.clear() when making the post request
    session.clear()
    # good to think about for later: for our uses this is okay but we might
    # want to have an app where we store some data and only get rid of the
    # survey answers.

    # Check out their solution because we implemented sessions prior to flow
    # of assignment

    return redirect ("/questions/0")


@app.get('/questions/<int:question_num>')
def question_router(question_num):
    """Grabs desired route and sends user to associated question."""
    # "Render the html for the question specified in the route" -- more
    # accurate docstring (we're not sending the user anywhere)
    question = survey.questions[question_num]

    return render_template(
        "question.html",
        question=question,
        question_num=question_num
    )


@app.post('/answer')
def get_answer():
    """
    Store question id and question answer in session data.
    Find idx of next question and see if that question exists.
    If that question idx exists, reroute to that question.
    Otherwise, reroute to completion page.
    """

    question_num = int(request.form['question-num'])

    session[f"{question_num}"] = request.form['answer']

    next_question_num = question_num + 1
    num_questions = len(survey.questions) - 1
    # num_questions currently isn't an accurate variable name (could just do
    # calculation in the if statement)

    if next_question_num <= num_questions:
        return redirect(f"/questions/{next_question_num}")
    else:
        return redirect('/completion.html')


@app.get('/completion.html')
def thank_user():
    """Display completion page of survey and list survey questions and
    user input answers."""

    return render_template(
        'completion.html',
        questions=survey.questions
    ) # Remember to line ')' up with return statement

