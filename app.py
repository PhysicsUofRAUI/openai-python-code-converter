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


def generate_prompt(lang, code, lang_conv):
    try:
        return """##### Translate this function from C++ into Python

### {}
    {}
### {}
""".format(lang, code, lang_conv)
    except KeyError:
        return "Invalid C++ code"
