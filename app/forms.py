from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class ProductForm(FlaskForm):
    product_id = StringField(
        "Podaj kod produktu z serwisu Ceneo.pl: ",
        validators=[
            DataRequired("Musisz podać kod produktu!"),
            Length(min=8, max=8, message="Kod produktu musi mieć 8 znaków!"),
            Regexp("^[0-9]+$", message="Kod produktu może zawierać tyko cyfry!")
        ]
    )
    submit = SubmitField("Pobierz")