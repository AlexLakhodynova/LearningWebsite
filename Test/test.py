from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Заранее определённые списки и правильные пары
list1 = ["Apple", "Banana", "Cherry"]
list2 = ["Red", "Yellow", "Pink"]
correct_matches = {"Apple": "Red", "Banana": "Yellow", "Cherry": "Pink"}

@app.route("/english/language_1_2_4", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Получение данных из POST-запроса
        data = request.json.get("matches", [])

        # Лог полученных данных для отладки
        print("Received matches:", data)

        # Проверка совпадений
        is_correct = True
        for pair in data:
            word1 = pair.get("word1")
            word2 = pair.get("word2")
            if correct_matches.get(word1) != word2:
                is_correct = False
                break

        # Лог результата проверки
        print("Correct matches:", correct_matches)
        print("Validation result:", is_correct)

        # Возвращаем результат
        return jsonify({"success": True, "correct": is_correct, "matches": data})

    # В случае GET-запроса отдаем HTML-страницу
    return render_template("index.html", list1=list1, list2=list2)

if __name__ == "__main__":
    app.run(debug=True)
