"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, render_template
from models import db, connect_db, Cupcake

from forms import AddCupcakeForm

DEFAULT = "https://tinyurl.com/demo-cupcake"

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "key" #in production in a different file...
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["WTF_CSRF_ENABLED"] = False

connect_db(app)


class BadRequest(Exception):
    """Custom exception class to be thrown when local error occurs."""
    
    def __init__(self, message, status=400, payload=None):
        self.message = message
        self.status = status
        self.payload = payload
        
        
@app.route('/')
def index_page():
    """Renders html template that includes some JS - NOT PART OF JSON API!"""
    form = AddCupcakeForm()
    
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes, form=form)


# *******************
#  RESTFUL JSON API
# *******************

@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns JSON with all cupcakes
    
        Returns JSON like: {cupcakes: [{id, flavor, rating, size, image}, ...]}
    """
    
    all_cupcakes = [ cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)
    
@app.route('/api/cupcakes/<int:cupcake_id>')
def get_todo(cupcake_id):
    """Returns JSON for one todo in particular
    
        Returns JSON like:  {cupcake: [{id, flavor, rating, size, image}]}
    """
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Creates a new capcake and returns JSON of that created capcake
    
        Returns JSON like: {cupcake: [{id, flavor, rating, size, image}]}
    """

    if not request.json["flavor"] and not request.json["size"] and not request.json["rating"]:
        raise BadRequest('A nullable value cannot be empty', 401)
    else:
        image = request.json.get('image', DEFAULT)
        new_cupcake = Cupcake(flavor = request.json["flavor"], 
                                size = request.json["size"], 
                                rating = request.json["rating"],
                                image = request.json["image"])
        db.session.add(new_cupcake)
        db.session.commit()
        response_json = jsonify(cupcake=new_cupcake.serialize())
        return (response_json, 201)
    
@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Updates a specific cupcake and responds with JSON of that updated cupcake
    
        Returns JSON like: {cupcake: [{id, flavor, rating, size, image}]}
    """ 
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', DEFAULT)
    return jsonify(cupcake=cupcake.serialize())
    

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Deletes a specific cupcake
    
        Returns JSON of {message: "Deleted"}
    """
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")