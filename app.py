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

RESPONSES = []

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

