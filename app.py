import flask
from flask import request

from api.validate import validate_finite_values_entity, validate_numeric_entity

app = flask.Flask(__name__)
app.config['Debug'] = True


@app.route('/validate/finite_values_entity', methods=['GET'])
def finite_values_entity():
    values = request.json
    result = validate_finite_values_entity(values.get('values'), values.get('supported_values'),
                                         values.get('invalid_trigger'), values.get('key'),
                                         values.get('support_multiple'), values.get('pick_first'), values.get('type'))

    return result


@app.route('/validate/numeric_entity', methods=['GET'])
def numeric_entity():
    values = request.json
    result = validate_numeric_entity(values=values.get('values'), invalid_trigger=values.get('invalid_trigger'),
                                     key=values.get('key'), support_multiple=values.get('support_multiple'),
                                     pick_first=values.get('pick_first'), constraint=values.get('constraint'),
                                     var_name=values.get('var_name'), value_type=values.get('type'))

    return result


app.run()
