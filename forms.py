from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField
from wtforms.validators import InputRequired, Optional, URL

class AddCupcakeForm(FlaskForm):
    flavor = StringField("Flavor", validators=[InputRequired(message="Flavor can't be empty")])
    #size = StringField("Size", validators=[InputRequired(message="Size can't be empty")])
    
    size = SelectField("Size", choices=[('mini', 'mini'), ('small', 'small'), ('medium', 'medium'), ('big', 'big')])
    rating = FloatField("Rating", validators=[InputRequired(message="Rating can't be empty")])
    image = StringField("Photo URL", validators=[Optional(), URL()])
