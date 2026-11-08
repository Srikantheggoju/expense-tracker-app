from flask import Flask, render_template, request

app = Flask(__name__)

expenses = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        item = request.form["item"]
        amount = request.form["amount"]

        expenses.append({
            "item": item,
            "amount": amount
        })

    total = sum(float(exp["amount"]) for exp in expenses) if expenses else 0

    return render_template(
        "index.html",
        expenses=expenses,
        total=total
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
