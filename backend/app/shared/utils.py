from sqlalchemy.orm import class_mapper


def to_dict(obj):
    """Convert a SQLAlchemy ORM object to a dictionary."""
    if obj is None:
        return None

    # Retrieve the mapper for the ORM class
    mapper = class_mapper(obj.__class__)

    # Create a dictionary of column names and their values
    return {column.key: getattr(obj, column.key) for column in mapper.columns}
