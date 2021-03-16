from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "mahmod salami"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sajad_user:09154438666@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


@app.route("/")
def index():
    all_data = Data.query.all()
    return render_template("index.html", employees=all_data)


@app.route("/insert", methods=['POST'])
def insert():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    new_data = Data(name=name, email=email, phone=phone)
    db.session.add(new_data)
    db.session.commit()

    flash("Employee Inserted Successfully.")

    return redirect(url_for("index"))


@app.route("/update", methods=["POST"])
def update():
    data = Data.query.filter_by(id=request.form.get("id")).first()
    data.name = request.form.get("name")
    data.email = request.form.get("email")
    data.phone = request.form.get("phone")
    db.session.commit()

    flash("Employee Updated Successfully.")

    return redirect(url_for("index"))


@app.route("/delete/<id>")
def delete(id):
    data = Data.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()

    flash("Employee Deleted Successfully")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
