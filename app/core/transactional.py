from functools import wraps
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from app.extension import db
from app.exceptions.business_exception import BusinessException


def transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result

        except ValidationError as e:
            return jsonify(
                [{"loc": err["loc"], "msg": err["msg"]} for err in e.errors()]
            ), 422

        except BusinessException as e:
            db.session.rollback()
            return jsonify(
                [{"loc": [e.field], "msg": e.message}]
            ), 400

        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return jsonify(
                [{"loc": ["database"], "msg": "Database error occurred"}]
            ), 500

    return wrapper
