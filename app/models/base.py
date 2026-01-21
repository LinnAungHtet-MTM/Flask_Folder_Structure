from sqlalchemy.inspection import inspect

class BaseModel:
    def to_dict(self, exclude: list = None):
        exclude = exclude or []
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
            if c.key not in exclude
        }