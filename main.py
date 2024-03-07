from flask import Flask, render_template, request
import random

app = Flask(__name__)

articles = []
class Article:
    def __init__(self,name, title, text):
        self.title = title
        self.text = text
        self.name = name



@app.route("/", methods = ["POST","GET"])
def FirstPage ():
    #global articles
    if request.method == "POST":
        if "AddText" in request.form:
            name = request.form['name']
            title = request.form['title']
            text = request.form['test']
            if name == "" or title == "" or text =="":
                return "Error. you didn't right some of the windows"
            else:
                a1 = Article(name, title, text)
                articles.append(a1)
                print(request.form)
                return render_template("site.html", articles = articles)

    return render_template("site.html", articles = articles)


app.run (debug=True)