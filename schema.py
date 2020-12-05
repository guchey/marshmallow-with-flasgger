from typing import List, Tuple, Type

from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    user_name = fields.Str(required=True, validate=validate.Length(max=10))
    mail = fields.Str(required=True)
    age = fields.Int(required=False, validate=validate.Range(min=0))


def get_all_schemas() -> List[Tuple[str, Type[Schema]]]:
    """
    定義したスキーマの一覧を返す関数です。
    flasggerに登録してSwagger YAMLで利用可能にするために利用します。
    :return:
    """
    return [(UserSchema.__name__, UserSchema)]
