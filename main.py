from flask import Flask, render_template, request, redirect, url_for, jsonify
import random

from flask_login import login_user, LoginManager, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

import passwords
from database import User, db, Article, Devise, give_points, get_points, total_points, reset_points

import datetime

from lists import sentences, info

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tables.db"
db.init_app(app)
with app.app_context():
    db.create_all()
login_manager = LoginManager(app)
app.secret_key = "secret "





texts = [
    "1: I am not one to hold a prejudice against any animal, but it is a plain fact that the spotted hyena is not well served by its appearance. It is ugly beyond redemption. Its shaggy, coarse coat is a bungled mix of colours, with the spots having none of the classy ostentation of a leopard's, they look rather like the symptoms of a skin disease. The head is broad and too massive, with a high forehead, like that of a bear, but suffering from a receding hairline, and with ears that look ridiculously mouse-like, large and round, when they haven't been torn off in battle. The mouth is forever open and panting. The nostrils are too big. The tail is scraggly and unwagging. All the parts put together look doglike, but like no dog anyone would want as a pet.",
    "2: Rosie had made a quick check of the unfamiliar garden before letting the children go out to play. The bottom half of the garden was an overgrown mess, a muddle of trees and shrubs. An ancient mulberry tree stood at the centre. Its massive twisted branches drooped to the ground in places, its knuckles in the earth like a gigantic malformed hand. The wintry sun hung low in the sky and the gnarled growth threw long twisted shadows across the undergrowth within its cage. The trunk of the tree was snarled with the tangled ivy that grew up through the broken bricks and chunks of cement, choking it. The path that led down towards the fence at the bottom, which marked the garden off from an orchard beyond, disappeared into a mass of nettles and brambles before it reached the padlocked door",
    "3: Ugwu did not believe that anybody, not even this master he was going to live with, ate meatevery day. He did not disagree with his aunty, though, because he was too choked withexpectation, too busy imagining his new life away from the village. They had been walking for a while now, since they got off the lorry at the motor park, and the afternoon sun burned the back of his neck. But he did not mind. He was prepared to walk hours more in even hotter sun. He had never seen anything like the streets that appeared after they went past the university gates, streets so smooth and tarred that he itched to lay his cheek down on them. He would never be able to describe to his sister Anulika how the bungalows here were painted the colour of the sky and sat side by side like polite well-dressed men, how the hedges separating them were trimmed so flat on top that they looked like tables wrapped with leaves."]

data = {0: {
    "question": texts[0],
    "answers": ["Simile", "Metaphor", "Oxymoron", "Hyperbole", "Personification", "Alliteration", "Onomatopoeia"],
    "correct_answers": ["Simile", "Metaphor", "Hyperbole", "Personification", "Alliteration"]
},
    1: {
        "question": texts[1],
        "answers": ["Simile", "Metaphor", "Oxymoron", "Hyperbole", "Personification", "Alliteration", "Onomatopoeia"],
        "correct_answers": ["Simile", "Metaphor", "Hyperbole", "Personification", "Alliteration"]
    },
    2: {
        "question": texts[2],
        "answers": ["Simile", "Metaphor", "Oxymoron", "Hyperbole", "Personification", "Alliteration",
                    "Onomatopoeia"],
        "correct_answers": ["Simile", "Metaphor", "Hyperbole", "Personification", "Alliteration"]

    }}

descriptions = ["qwertyui", "qzetzvtyv", "ukmdytuty", "qjdtjkulil,j", "tyrhjgnx", "serrer"]

languageDevises = ["Simile", "Metaphor", "Oxymoron", "Hyperbole", "Personification", "Alliteration", "Onomatopoeia"]


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@app.route("/addtext", methods=["POST", "GET"])
def SecondPage():
    # global articles
    if request.method == "POST":
        if "AddText" in request.form:
            name = request.form['name']
            title = request.form['title']
            text = request.form['test']
            if name == "" or title == "" or text == "":
                return "Error. you didn't right in some of the windows"
            else:
                # a1 = Article(name, title, text)
                # articles.append(a1)
                # print(request.form)
                return render_template("site.html", name=name, title=title, text=text)

        if "no" in request.form:
            return render_template("site.html")
        elif "yes" in request.form:
            name = request.form['name']
            title = request.form['title']
            text = request.form['text']
            try:
                a1 = Article(name, title, text, userid=current_user.id)
            except:
                return redirect(url_for("login"))
            db.session.add(a1)
            db.session.commit()
            print(request.form)
            return redirect(url_for("FirstPage"))

    return render_template("site.html", )


@app.route("/", methods=["POST", "GET"])
def FirstPage():
    if request.method == "POST":
        if "addtext1" in request.form:
            return redirect(url_for("SecondPage"))
        elif "login" in request.form:
            return redirect(url_for("login"))
        elif "register" in request.form:
            return redirect(url_for("register"))
        elif "account" in request.form:
            return redirect(url_for("account"))
        elif "articles" in request.form:
            return redirect(url_for("articles"))
        elif "english" in request.form:
            return redirect(url_for("english"))
    return render_template("firstpage.html")


@app.route("/registration", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if "done" in request.form:
            nickname = request.form['email']
            password = request.form['password']
            username = request.form['nickname']
            password2 = request.form['password2.0']
            if password != password2:
                return "Incorrect password"
            try:
                if len(password) <= 8:
                    return "Incorrect length of the password"
                user = User(nickname, generate_password_hash(password), username)
                db.session.add(user)
                db.session.commit()
            except:
                return "Incorrect login"
            return redirect(url_for("FirstPage"))
    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if "done" in request.form:
            nickname = request.form['nickname']
            password = request.form['password']
            user = User.query.filter_by(login=nickname).first()
            if user is None:
                return "There are no such user"
            if not check_password_hash(user.password, password):
                return "Username and password didn't match"
            login_user(user, remember=True)
            return redirect(url_for("FirstPage"))
    return render_template("login.html")


@app.route("/account", methods=["POST", "GET"])
@login_required
def account():
    if request.method == "POST":
        if "logout" in request.form:
            logout_user()
            return redirect(url_for("FirstPage"))
        elif "delete" in request.form:
            data = request.form
            delete1 = data.get("delete")
            Article.query.filter_by(id=delete1).delete()
            db.session.commit()
        elif "edit" in request.form:
            data = request.form
            edit1 = data.get("edit")
            return redirect(url_for("edit", id=edit1))
    nickname = current_user.login
    user_name = current_user.user_name
    posts = Article.query.filter_by(userid=current_user.id).all()
    return render_template("account.html", nickname=nickname, user_name = user_name,  articles=posts)


@app.errorhandler(401)
def check(error):
    return "You did not login. If you dont have an account, please register"


@app.errorhandler(404)
def check2(error):
    return "The requested link was not found on the server."


@app.route("/articles", methods=["POST", "GET"])
def articles():
    posts = Article.query.all()
    return render_template("articles.html", articles=posts)


@app.route("/edit/<id>", methods=["POST", "GET"])
def edit(id):
    article = Article.query.filter_by(id=id).first()
    if request.method == "POST":
        if "edit" in request.form:
            name = request.form['name']
            title = request.form['title']
            text = request.form['test']
            article.name = name
            article.title = title
            article.text = text
            db.session.add(article)
            db.session.commit()
            return redirect(url_for("FirstPage"))
    return render_template("Edit.html", name=article.name, title=article.title, text=article.text)






@app.route("/computer_science", methods=["POST", "GET"])
def computer_science():
    if request.method == "POST":
        if "computer_science2.2" in request.form:
            return redirect(url_for("cyber_security_threats"))
        if "computer_science2.3" in request.form:
            print("no")
            return redirect(url_for("social_engineering"))
        if "computer_science2.4" in request.form:
            print("hi")
            return redirect(url_for("malicious_code"))
        if "computer_science2.5" in request.form:
            print("hi")
            return redirect(url_for("detecting_and_preventing_cyber_security_threats"))

    return render_template("computer_science.html")

@app.route("/computer_science/cyber_security_threats", methods=["POST", "GET"])
def cyber_security_threats():
    if request.method == "POST":
        if "previous" in request.form:
            return redirect(url_for("computer_science"))

    return render_template("computer_science11_1.html")

@app.route("/computer_science/social_engineering", methods=["POST", "GET"])
def social_engineering():
    if request.method == "POST":
        if "previous" in request.form:
            return redirect(url_for("computer_science"))

    return render_template("computer_science11_2.html")

@app.route("/computer_science/malicious_code", methods=["POST", "GET"])
def malicious_code():
    if request.method == "POST":
        if "previous" in request.form:
            return redirect(url_for("computer_science"))

    return render_template("computer_science11_3.html")

@app.route("/computer_science/detecting_and_preventing_cyber_security_threats", methods=["POST", "GET"])
def detecting_and_preventing_cyber_security_threats():
    if request.method == "POST":
        if "previous" in request.form:
            return redirect(url_for("computer_science"))

    return render_template("computer_science11_4.html")


@app.route("/computer_science/cyber_security_threats/2", methods=["POST", "GET"])
def cyber_security_threats2():
    if request.method == "POST":
        if "next" in request.form:
            number = random.randint(0, len(texts) - 1)
            return redirect(url_for("english_P1_Q2_T2", number=number))
    print(update_task_date("Test2"))
    info = []
    passwords_copy = passwords.copy()
    for i in range(5):
        rq = random.choice(passwords_copy)
        passwords_copy.remove(rq)
        info.append(rq)

    return render_template("computer_science11_1_2.html", info=info)






@app.route("/english", methods=["POST", "GET"])
def english():
    if request.method == "POST":
        if "english1.2" in request.form:
            return redirect(url_for("english_P1_Q2_T1"))
        if "english1.1" in request.form:
            return redirect(url_for("english_P1_Q1_T1"))
    return render_template("english.html")


def update_task_status(test_number):
    update_task_date(test_number, 1)

def update_task_date(test_number, status = 0 ):
    today = datetime.date.today()
    user_id = current_user.id
    user = User.query.filter_by(id=user_id).first()
    date = user.task_date.split("/")
    print(date)
    for data_tmp in date:
        if test_number in data_tmp:
            n = f"{test_number} {today} {status}"
            ind = date.index(data_tmp)
            date[ind] = n
            break
    else:
        n = f"{test_number} {today} {status}"
        date.append(n)
    user.task_date = "/".join(date)
    db.session.add(user)
    db.session.commit()


@app.route("/english/language_1_1_1", methods=["POST", "GET"])
def english_P1_Q1_T1():
    print(update_task_date("Test1"))

    return render_template("paper1_1_1.html")

class Answer:
    variant = ''
    description = ''
    color = ''

@app.route("/english/language_1_2_1", methods=["POST", "GET"])
def english_P1_Q2_T1():
    if request.method == "POST":
        if "check" in request.form:

            points = 0
            result_answers = []
            dictionary= dict(list(dict(request.form).items())[:-1])
            for i in dictionary:

                index = sentences.index(i)
                text = info[index]["correct_answers"][0]
                if dictionary[i] == text:
                    answer = Answer()
                    answer.variant = dictionary[i]
                    answer.description = 'correct'
                    points += 1
                    answer.color = "p-3 mb-2 bg-success text-dark"
                    result_answers.append(answer)
                else:
                    answer = Answer()
                    answer.variant = dictionary[i]
                    answer.description = 'incorrect'
                    answer.color = "p-3 mb-2 bg-danger text-dark"
                    result_answers.append(answer)



            total_points = len(dictionary)
            user_id = current_user.id
            give_points(user_id, total_points, points)
            return render_template("paper1_2_1.html", result_answers=result_answers)

            print(dict(request.form))
        if "next" in request.form:
            number = random.randint(0, len(texts) - 1)
            return redirect(url_for("english_P1_Q2_T2", number=number))
    print(update_task_date("Test2"))
    info2 = []
    sentences_copy = sentences.copy()
    for i in range(5):
        rq = random.choice(sentences_copy)
        sentences_copy.remove(rq)
        info2.append(rq)


    return render_template("paper1_2_1.html", info=info2)



@app.route("/english/language_1_2_2/<number>", methods=["POST", "GET"])
def english_P1_Q2_T2(number):
    if request.method == "POST":
        if "next" in request.form:
            return redirect(url_for("english_P1_Q2_T3"))
        elif "check" in request.form:
            user_answer = list(request.form)[:-1]
            correct_answers = data[int(number)]["correct_answers"]
            result_answers = []
            points = 0
            for i in user_answer:
                if i not in correct_answers:
                    answer = Answer()
                    answer.variant = i
                    answer.description = 'incorrect'
                    answer.color = "p-3 mb-2 bg-danger text-dark"
                    result_answers.append(answer)
                else:

                    answer = Answer()
                    answer.variant = i
                    answer.description = 'correct'
                    points += 1
                    answer.color = "p-3 mb-2 bg-success text-dark"
                    result_answers.append(answer)
            for i in correct_answers:
                if i not in user_answer:
                    answer = Answer()
                    answer.variant = i
                    answer.description = 'must be chosen as correct'
                    answer.color = "p-3 mb-2 bg-warning text-dark"
                    result_answers.append(answer)
            text = data[int(number)]["question"]

            total_points = len(correct_answers)
            user_id = current_user.id
            give_points(user_id, total_points, points)

            print(result_answers, user_answer, correct_answers)

            return render_template("paper1_2_2.html", text=text, result_answers=result_answers)
    text = data[int(number)]["question"]
    answers = data[int(number)]["answers"]
    return render_template("paper1_2_2.html", text=text, answers=answers)


@app.route("/english/language_1_2_3", methods=["POST", "GET"])
def english_P1_Q2_T3():
    elements = []
    if request.method == "POST":
        if "check" in request.form:
            user_input = []

            output = request.form
            for k, v in output.items():
                user_input.append(v)
            user_answers = {}
            print(user_input)
            user_input = user_input[:-1]
            for i in range(0, len(user_input) -1, 2):
                if user_input[i] == "":
                    user_answers[user_input[i+1]] = user_input[i + 1]
                else:
                    user_answers[user_input[i]] = user_input[i + 1]
            print(user_answers)
            points = 0

            correct = ["qwertyui", "qzetzvtyv", "ukmdytuty", "qjdtjkulil,j", "tyrhjgnx", "serrer"]
            g=0
            for number in user_answers:
                element = Devise(user_answers[number], languageDevises[g])
                if number == str(correct.index(user_answers[number])+1):
                    element.color = "p-3 mb-2 bg-success text-dark"
                    element.answer = number
                    points += 1
                else:
                    element.color = "p-3 mb-2 bg-danger text-dark"
                    element.answer = number
                elements.append(element)
                g+= 1
            total_points = len(correct)
            user_id = current_user.id
            give_points(user_id, total_points, points)
            return render_template("paper1_2_3.html", elements=elements)

        if "next" in request.form:
            return redirect(url_for("english_P1_Q2_T4"))
    random.shuffle(descriptions)

    for i in range(len(descriptions)):
        element = Devise(descriptions[i], languageDevises[i])
        elements.append(element)
    return render_template("paper1_2_3.html", elements=elements)

list1 = ["Apple1", "Banana1", "Cherry1"]
list2 = ["Red1", "Yellow1", "Pink1"]
correct_matches = {"Apple1": "Red1", "Banana1": "Yellow1", "Cherry1": "Pink1", "Peach1":"Orange1"}
numtry = False


@app.route("/english/language_1_2_4", methods=["POST", "GET"])
def english_P1_Q2_T4():
    global numtry
    if request.method == "POST":
        points = 0

        data = request.json.get("matches", [])
        data1 = request.json.get("correctMatches", {})


        is_correct = True
        for pair in data:
            word1 = pair.get("word1")
            word2 = pair.get("word2")
            if correct_matches.get(word1) != word2:
                is_correct = False
                break
            else:
                points+=1
        if len(data) == 1:
            numtry = False

        print("Correct matches:", correct_matches)
        print("Validation result:", is_correct)
        go_to_results = False

        if numtry :
            go_to_results = True

        if len(data) == len(list1):
            numtry = True

        print(go_to_results)
        if go_to_results:

            total_points = len(list1)
            user_id = current_user.id
            give_points(user_id, total_points, points)
            return jsonify({ "success": True, "correct": is_correct, "matches": data, "correctMatches":correct_matches, "redirect": url_for("results")})

        return jsonify({"success": True, "correct": is_correct, "matches": data, "correctMatches": correct_matches})
    print("ehgu")
        # В случае GET-запроса отдаем HTML-страницу
    return render_template("paper1_2_4.html", list1=list1, list2=list2)

@app.route("/english/language_devises_results", methods=["POST", "GET"])
def results():
    user_name = current_user.user_name
    user_id = current_user.id
    total_user_correct_answers, total_possible_correct_answers = get_points(user_id)
    if total_possible_correct_answers != 0 :
        percentage = total_user_correct_answers/total_possible_correct_answers * 100

    else:
        percentage = 0
    if request.method == "POST":
        if "Go_to_the_main_page" in request.form:
            reset_points(user_id)
            update_task_status("Test2")
            return redirect(url_for("FirstPage"))
    points = round(percentage/10)
    total_points(user_id, points)

    return render_template("results.html", total_user_correct_answers = total_user_correct_answers, total_possible_correct_answers = total_possible_correct_answers, user_name = user_name, percentage=percentage)

print("hi")

app.run(debug=True)
