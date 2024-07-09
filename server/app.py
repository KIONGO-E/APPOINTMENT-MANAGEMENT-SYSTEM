from models import db, User, Appointment, Profession
from flask_migrate import Migrate
from flask import Flask, request, make_response ,jsonify
from flask_restful import Api, Resource
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route("/")
def index():
    return "<h1>Appointment Management System</h1>"

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict(rules=('-password', '-appointments.user')) for user in users])


# GET a single user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict(rules=('-password', '-appointments.user')))
    return jsonify({"error": "User not found"}), 404


# DELETE a user by ID
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return '', 204
    return jsonify({"error": "User not found"}), 404


# POST create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        new_user = User(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            location=data.get('location')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict(rules=('-password', '-appointments.user'))), 201
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400


# GET all professions
@app.route('/professions', methods=['GET'])
def get_professions():
    professions = Profession.query.all()
    return jsonify([profession.to_dict(rules=('-appointments.profession',)) for profession in professions])


# POST create a new profession
@app.route('/professions', methods=['POST'])
def create_profession():
    data = request.get_json()
    try:
        new_profession = Profession(
            name=data['name']
        )
        db.session.add(new_profession)
        db.session.commit()
        return jsonify(new_profession.to_dict(rules=('-appointments.profession',))), 201
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400


# GET all appointments
@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([appointment.to_dict(rules=('-user.appointments', '-profession.appointments')) for appointment in appointments])


# POST create a new appointment
@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    try:
        new_appointment = Appointment(
            user_id=data['user_id'],
            profession_id=data['profession_id'],
            date=data['date'],
            time=data['time'],
            status=data.get('status', 'Pending')
        )
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify(new_appointment.to_dict(rules=('-user.appointments', '-profession.appointments'))), 201
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)


