
from math import prod
from flask import Flask, redirect , render_template ,jsonify, url_for, request
import pymongo
from bson.objectid import ObjectId
from requests import post
import json

app = Flask(__name__)

# configure secret key for session protection)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

# MONGOGB DATABASE CONNECTION
connection_url = "mongodb://localhost:27017/"
client = pymongo.MongoClient(connection_url)
# client.list_database_names()
database_name = "DryCleaner"
db = client[database_name]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shop-pricing")
def shop_pricing():
    return render_template("shop-pricing.html")

@app.route("/delivery-pricing")
def delivery_pricing():
    data = db.categories.find()
    categories=[]
    for i in data:
        i.update({"_id":str(i["_id"])})
        products = []
        x = db.pricing.find({"category_id":i["_id"]})
        for j in x:
            j.update({"_id":str(j["_id"])})
            products.append(j)
        i.update({"pricing":products})
        categories.append(i)
    # return jsonify({"categories":categories})
    return render_template("delivery-pricing.html",categories=categories)

@app.route("/contact-form", methods=['POST'])
def contact_form():
    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")
    print(name,email,subject,message)
    return "I am groot"
    return redirect("/?")

@app.route("/booking")
def booking():
    if "postcode" in request.args:
        postcode = request.args.get("postcode")
        city = request.args.get("city")
        address = request.args.get("address")
        return render_template("booking-index.html",pc=postcode,city=city,address=address)
    else:
        return render_template("booking-index.html")


@app.route("/booking-price")
def booking_price():    
    data = db.categories.find()
    categories=[]
    for i in data:
        i.update({"_id":str(i["_id"])})
        products = []
        x = db.pricing.find({"category_id":i["_id"]})
        for j in x:
            j.update({"_id":str(j["_id"])})
            products.append(j)
        i.update({"pricing":products})
        categories.append(i)
    if "city" in request.args:
        city=request.args.get("city")
        address= request.args.get("address")
        postcode = request.args.get("postcode")
        p_date = request.args.get("p_date")
        p_time = request.args.get("p_time")
        d_date = request.args.get("d_date")
        d_time = request.args.get("d_time")
        # return jsonify({"data":categories})
        return render_template("booking-price.html",categories=categories,city=city,address=address,postcode=postcode,p_date=p_date,p_time=p_time,d_date=d_date,d_time=d_time)
    else:
        return render_template("booking-price.html",categories=categories)

@app.route("/book-now", methods=['GET','POST'])
def book_now():    
    if request.method == "POST":
        try:
            name = request.form.get("name")
            email = request.form.get("email")
            address = request.form.get("address")
            city = request.form.get("city")
            postcode = request.form.get("postcode")
            example = request.form.get("example")
            p_date = request.form.get("p_date")
            p_time = request.form.get("p_time")
            d_date = request.form.get("d_date")
            d_time = request.form.get("d_time")
            total_amount = request.form.get("total_amount")
            products = request.form.get("products")
            products = json.loads(products)
            new_booking = {
                "name":name,
                "email":email,
                "address":address,
                "city":city,
                "postcode":postcode,
                "example":example,
                "p_date":p_date,
                "p_time":p_time,
                "d_date":d_date,
                "d_time":d_time,
                "products":products,
                "total_amount":total_amount
            }
            db.bookings.insert_one(new_booking)
            return "True"
        except Exception as e:
            print(e)
            return "False"
            return str(e)

        return str(name)
    if "city" in request.args:
        city=request.args.get("city")
        address= request.args.get("address")
        postcode = request.args.get("postcode")
        p_date = request.args.get("p_date")
        p_time = request.args.get("p_time")
        d_date = request.args.get("d_date")
        d_time = request.args.get("d_time")
        cart = request.args.get("cart")
        cart = cart.split(",")
        products = []
        total_amount = 0
        for i in cart:
            price = db.pricing.find_one({"_id":ObjectId(i)})
            p = price['price']
            total_amount = float(total_amount)+float(p)
            pr = price['name']
            products.append(pr)
        return render_template("book-now.html",city=city,address=address,postcode=postcode,p_date=p_date,p_time=p_time,d_date=d_date,d_time=d_time,total_amount=total_amount,products=products)
    else:
        return render_template("book-now.html")

# ----------------------------ADMIN DASH---------------------------------
@app.route("/admin")
def admin():
    return render_template("admin-index.html")
@app.route("/admin-cat")
def admin_cat():
    data = db.categories.find()
    categories= []
    for i in data:
        i.update({"_id":str(i["_id"])})
        categories.append(i)
    return render_template("admin-cat.html",cat=categories)
@app.route("/admin-pricing")
def admin_pricing():
    data = db.pricing.find()
    pricing= []
    for i in data:
        i.update({"_id":str(i["_id"])})
        pricing.append(i)
    return render_template("admin-pricing.html",pricing=pricing)

@app.route("/admin-bookings")
def admin_booking():
    data = db.bookings.find()
    bookings= []
    for i in data:
        i.update({"_id":str(i["_id"])})
        bookings.append(i)
    return render_template("admin-booking.html",bookings=bookings)

@app.route("/admin-add/<string:type>",methods=['GET','POST'])
def admin_add(type):
    if request.method=='POST':
        error= False
        name=request.form.get("name")
        if type=="pricing":
            price=request.form.get("price")
            category_id=request.form.get("category_id")
            category_name=db.categories.find_one({"_id":ObjectId(category_id)})
            category_name=category_name['name']
            

            exists = db.pricing.find_one({"name":name})
            if exists:
                error=True
                msg = "Already added!"
            else:
                db.pricing.insert_one({"name":name,"categoryname":category_name,"category_id":category_id,"price":price})
                msg = "Added successfully!"
            data = db.categories.find()
            categories= []
            for i in data:
                i.update({"_id":str(i["_id"])})
                categories.append(i)
            return render_template("admin-add.html",type=type,error=error,msg=msg,categories=categories)
            
        elif type=="category":

            exists = db.categories.find_one({"name":name})
            if exists:
                error=True
                msg = "Already added!"
            else:
                db.categories.insert_one({"name":name})
                msg = "Added successfully!"
            data = db.categories.find()
            categories= []
            for i in data:
                i.update({"_id":str(i["_id"])})
                categories.append(i)
            return render_template("admin-add.html",type=type,error=error,msg=msg,categories=categories)
            
    data = db.categories.find()
    categories= []
    for i in data:
        i.update({"_id":str(i["_id"])})
        categories.append(i)
    return render_template("admin-add.html",type=type,categories=categories)

@app.route("/admin-del/<string:type>/<string:id>")
def admin_del(type,id):
    if type=="category":
        db.categories.delete_one({"_id":ObjectId(cat_id)})
        return redirect(url_for("admin_cat"))
    elif type=="pricing":
        db.pricing.delete_one({"_id":ObjectId(cat_id)})
        return redirect(url_for("admin_pricing"))

@app.route("/admin-edit/<string:type>/<string:id>",methods=['GET','POST'])
def admin_edit(type,id):
    if request.method=='POST':
        name=request.form.get("name")        
        filter={"_id":ObjectId(id)}
        if type=="pricing":
            price=request.form.get("price")
            category_id=request.form.get("category_id")
            category_name=db.categories.find_one({"_id":ObjectId(category_id)})
            category_name=category_name['name']
            new_values = {
                    '$set': {"name":name,"categoryname":category_name,"category_id":category_id,"price":price}
                }
            db.pricing.update_one(filter, new_values)
            return redirect(url_for('admin_pricing'))
        elif type=="category":
            new_values = {
                    '$set': {"name":name}
                }
            db.categories.update_one(filter, new_values)
            return redirect(url_for('admin_cat'))
    if type=="category":
        data = db.categories.find_one({"_id":ObjectId(id)})
        return render_template("admin-edit.html",data=data,type=type)
    elif type == "pricing":        
        data = db.categories.find()
        categories= []
        for i in data:
            i.update({"_id":str(i["_id"])})
            categories.append(i)

        data = db.pricing.find_one({"_id":ObjectId(id)})
        return render_template("admin-edit.html",data=data,type=type,categories=categories)

# test route 
@app.route("/api")
def api():
    return render_template("api.html")

    

if __name__ == "__main__":
    app.run(debug=True)