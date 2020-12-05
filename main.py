from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger
from flask import Flask, redirect, request, jsonify
from marshmallow import ValidationError

import db
from schema import get_all_schemas, UserSchema

spec = APISpec(
    title="marshmallow-with-flasgger",
    version="0.1.0",
    openapi_version="2.0",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

flask_app = Flask(__name__)
flask_app.config["JSON_AS_ASCII"] = False
flask_app.config["SWAGGER"] = {"uiversion": 3}
flask_app.config["SECRET_KEY"] = "secret key"

_template = spec.to_flasgger(flask_app, definitions=get_all_schemas())
_swag = Swagger(flask_app, template=_template)


@flask_app.route("/", methods=["GET"])
def index():
    return redirect("apidocs")


@flask_app.route("/users", methods=["GET"])
def get_users():
    """
    get users
    ---
    tags:
      - user
    produces:
      - application/json
    responses:
      200:
        description: Successful operation
        schema:
          type: array
          items:
            $ref: "#/definitions/UserSchema"
    """
    schema = UserSchema()
    return jsonify([schema.dump(u) for u in db.Users.all()])


@flask_app.route("/users", methods=["POST"])
def post_users():
    """
    post user
    ---
    tags:
      - user
    produces:
      - application/json
    parameters:
      - in: body
        name: user
        schema:
          $ref: '#/definitions/UserSchema'
    responses:
      200:
        description: Successful operation
        schema:
          $ref: "#/definitions/UserSchema"
    """
    payload = request.json

    # 入力値の検証を行います。入力値がSchemaと一致しない場合はValidationErrorがraiseされます。
    schema = UserSchema()
    schema.load(payload)

    # バリデーションが完了したら何らかのロジックを実行するでしょう。
    db.Users.save(schema.dump(payload))

    return jsonify(payload)


@flask_app.errorhandler(ValidationError)
def handle_schema_validation_error(e: ValidationError):
    return jsonify(e.messages), 400


if __name__ == "__main__":
    flask_app.run(host="127.0.0.1", port=8080, debug=True)
