from flask import Flask, render_template, redirect, url_for
import csv
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
import os
from dotenv import find_dotenv, load_dotenv


app = Flask(__name__)
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
SECRET_KEY = os.getenv("SECRET_KEY")
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap5(app)

class RestForm(FlaskForm):
    restaurant = StringField('Restaurant name', validators=[DataRequired()])
    style = StringField("Style/Type", validators=[DataRequired()])
    location = StringField("Restaurant Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    open = StringField("Opening Time e.g. 8AM", validators=[DataRequired()])
    close = StringField("Closing Time e.g. 5:30PM", validators=[DataRequired()])
    rating = StringField("Rating 1-5",  validators=[DataRequired()])
    image = StringField('Image url', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')



@app.route('/')
def restaurants():
    with open('restaurant_data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.DictReader(csv_file)
        list_of_rows = list(csv_data)
    return render_template('index.html', restaurants=list_of_rows)


@app.route("/add", methods=["GET", "POST"])
def add_rest():
    form = RestForm()
    if form.validate_on_submit():
        with open("restaurant_data.csv", mode="a", encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.restaurant.data},"
                           f"{form.style.data},"
                           f"{form.location.data},"
                           f"{form.open.data},"
                           f"{form.close.data},"
                           f"{form.rating.data},"
                           f"{form.image.data},"
                           )
        return redirect(url_for('restaurants'))
    return render_template('add.html', form=form)





if __name__ == "__main__":
    app.run(debug=True, port=5002)


