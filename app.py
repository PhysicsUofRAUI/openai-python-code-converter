import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        code = request.form["code"]
        lang = request.form["lang"]
        lang_conv = request.form["lang_conv"]
        response = openai.Completion.create(
        model="code-davinci-002",
        prompt=generate_prompt(lang, code, lang_conv),
        temperature=0.1,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["###"]
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


@app.route("/test_writer", methods=("GET", "POST"))
def test_writer():
    if request.method == "POST":
        code = request.form["code"]
        lang = request.form["lang"]
        response = openai.Completion.create(
        model="code-davinci-002",
        prompt=generate_unit_test(lang, code),
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["###"]
        )
        return redirect(url_for("test_writer", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("test_writer.html", result=result)

@app.route("/code_explainer", methods=("GET", "POST"))
def code_explainer():
    if request.method == "POST":
        code = request.form["code"]
        response = openai.Completion.create(
        model="code-davinci-002",
        prompt=generate_general_prompt(code),
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["###"]
        )
        return redirect(url_for("code_explainer", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("code_explainer.html", result=result)

@app.route("/code_rewriter", methods=("GET", "POST"))
def code_rewriter():
    if request.method == "POST":
        code = request.form["code"]
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_general_prompt(code),
        temperature=0.2,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        return redirect(url_for("code_rewriter", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("code_rewriter.html", result=result)

def generate_prompt(lang, code, lang_conv):
    try:
        return """##### Translate this function from C++ into Python

### {}
{}
### {}
""".format(lang, code, lang_conv)
    except KeyError:
        return "Invalid C++ code"


def generate_unit_test(lang, code):
    try:
        return """# {}
{}

# Unit test""".format(lang, code)

    except KeyError:
        return "Invalid code"

def generate_general_prompt(code):
    try:
        return """{}""".format(code)

    except KeyError:
        return "Invalid code"
