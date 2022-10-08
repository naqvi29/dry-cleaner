from flask import Flask, redirect , render_template ,jsonify, url_for, request
from requests import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shop-pricing")
def shop_pricing():
    return render_template("shop-pricing.html")

@app.route("/delivery-pricing")
def delivery_pricing():
    return render_template("delivery-pricing.html")

@app.route("/contact-form", methods=['POST'])
def contact_form():
    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")
    print(name,email,subject,message)
    return "I am groot"
    return redirect("/?")

    

if __name__ == "__main__":
    app.run(debug=True)