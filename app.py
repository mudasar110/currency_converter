from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

API_KEY = "6aef023f0ffa4a3cce9f1790"

CURRENCIES = [
    "USD","PKR","GBP","EUR","INR","SAR","AED","AUD","CAD","JPY","CNY"
]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Currency Converter</title>
    <style>
        body {
            font-family: Arial;
            background: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .box {
            background: white;
            padding: 25px;
            border-radius: 10px;
            width: 380px;
            box-shadow: 0 0 10px #aaa;
        }
        h2 { text-align: center; }
        input, select {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            font-size: 15px;
        }
        .row {
            display: flex;
            gap: 10px;
        }
        .result {
            margin-top: 15px;
            text-align: center;
            font-weight: bold;
            font-size: 17px;
            color: green;
        }
    </style>
</head>
<body>

<div class="box">
    <h2>💱 Currency Converter</h2>

    <input type="number" id="amount" placeholder="Amount">

    <div class="row">
        <select id="from">
            {% for c in currencies %}
                <option value="{{c}}">{{c}}</option>
            {% endfor %}
        </select>

        <select id="to">
            {% for c in currencies %}
                <option value="{{c}}">{{c}}</option>
            {% endfor %}
        </select>
    </div>

    <div class="result" id="result"></div>
</div>

<script>
async function convert() {
    let amount = document.getElementById("amount").value;
    let from = document.getElementById("from").value;
    let to = document.getElementById("to").value;

    if (!amount || amount <= 0) {
        document.getElementById("result").innerText = "";
        return;
    }

    let res = await fetch(`/convert?amount=${amount}&from=${from}&to=${to}`);
    let data = await res.json();

    if (data.success) {
        document.getElementById("result").innerText =
            `${amount} ${from} = ${data.result.toFixed(4)} ${to}`;
    } else {
        document.getElementById("result").innerText = "Conversion failed";
    }
}

document.getElementById("amount").addEventListener("input", convert);
document.getElementById("from").addEventListener("change", convert);
document.getElementById("to").addEventListener("change", convert);
</script>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML, currencies=CURRENCIES)

@app.route("/convert")
def convert():
    try:
        amount = float(request.args.get("amount"))
        from_currency = request.args.get("from")
        to_currency = request.args.get("to")

        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}"
        data = requests.get(url, timeout=10).json()

        rate = data["conversion_rates"][to_currency]
        return jsonify(success=True, result=amount * rate)

    except Exception as e:
        return jsonify(success=False)

if __name__ == "__main__":
    app.run(debug=True)
