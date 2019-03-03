from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
from flask_marshmallow import Marshmallow
import os
import json
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

cors = CORS(app)

ma = Marshmallow(app)

targets = db.Table('targets',
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                   db.Column('bodypart_id', db.Integer, db.ForeignKey('bodypart.id'), primary_key=True)
                   )

uses = db.Table('uses',
                db.Column('bodypart_id', db.Integer, db.ForeignKey("bodypart.id"), primary_key=True),
                db.Column('exercise_id', db.Integer, db.ForeignKey("exercise.id"), primary_key=True)
                )


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    level = db.Column(db.String(30))
    # password_hash = db.Column(db.String(128))
    targets = db.relationship('BodyPart', secondary=targets, lazy='dynamic',
                              backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.username


class BodyPart(db.Model):
    __tablename__ = 'bodypart'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


class Exercise(db.Model):
    __tablename__ = 'exercise'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    base_reps = db.Column(db.Integer, nullable=False)
    rep_incr = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250))
    uses = db.relationship('BodyPart', secondary=uses, lazy='subquery',
                           backref=db.backref('exercise', lazy=True))


class BodyPartSchema(ma.ModelSchema):
    class Meta:
        model = BodyPart


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        exclude = ("password",)


class ExerciseSchema(ma.ModelSchema):
    class Meta:
        model = Exercise


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        user_schema = UserSchema()
        return user_schema.jsonify(user)


class UsersResource(Resource):
    def get(self):
        user = User.query.all()
        users_schema = UserSchema(many=True)
        return users_schema.jsonify(user)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')
        parser.add_argument('level')
        parser.add_argument('bodypart', type=str, action='append')
        args = parser.parse_args()

        user_exists = User.query.filter_by(username=args["username"]).first()
        if user_exists:
            return "User already exists", 409

        new_user = User(username=args['username'], password=args['password'], level=args['level'])
        for bp in args['bodypart']:
            print(bp)
            new_bp = BodyPart.query.filter_by(name=bp.lower()).first()
            print(new_bp)
            if not new_bp:
                print("Could not find body part")
                return "Could not find body part", 409

            new_user.targets.append(new_bp)

        db.session.add(new_user)
        db.session.commit()

        user_schema = UserSchema()
        new_user = User.query.filter_by(username=args['username'])
        response = user_schema.jsonify(new_user)
        print(response)
        return "Added new user", 201


class ExercisesResource(Resource):
    def get(self):
        exercises = Exercise.query.all()
        exercises_schema = ExerciseSchema(many=True)
        return exercises_schema.jsonify(exercises)

    def post(self):
        return "In post method of Exercises Resource"


class ExerciseRecommendationResource(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        target_set = set(user.targets)

        #TODO: do this in a less hacky way
        user_exercises = []
        seen_exercises = set()
        for ex in Exercise.query.all():
            for bp in ex.uses:
                if bp in target_set:
                    if ex.name in seen_exercises:
                        continue

                    seen_exercises.add(ex.name)

                    curr_ex_dict = {'exercise':ex.name}
                    curr_ex_dict['reps'] = 10
                    if user.level == "beginner":
                        curr_ex_dict['reps'] = ex.base_reps
                    elif user.level == "intermediate":
                        curr_ex_dict['reps'] = ex.base_reps + ex.rep_incr
                    elif user.level == "advanced":
                        curr_ex_dict['reps'] = ex.base_reps + 2 * ex.rep_incr

                    user_exercises.append(curr_ex_dict)


        if user.level == "intermediate":
            user_exercises = user_exercises * 2
        elif user.level == "advanced":
            user_exercises = user_exercises * 3
            
        return json.dumps(user_exercises)


class UserIdResource(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return "Could not find user with that username", 409
        return json.dumps(user.id)


api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(UsersResource, '/users/')
api.add_resource(ExercisesResource, '/exercises/')
api.add_resource(ExerciseRecommendationResource, '/recommendation/<int:user_id>')
api.add_resource(UserIdResource, '/idfor/<string:username>')

if __name__ == '__main__':
    app.run(debug=True)
