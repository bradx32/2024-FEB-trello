import functools

from flask_jwt_extended import get_jwt_identity

from init import db
from models.user import User

# function will return TRUE if user is admin and FALSE if not    
def authorise_as_admin():
    # get the user's id from get_jwt_identity
    user_id = get_jwt_identity()
    # fetch the user from the db
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # check whether the user is an admin or not
    return user.is_admin

# The lesson 06/07/2024 Saturday explanation and implementation of the decorator function used to make a function more simple? As apose to the above function ^
# This references to the auth_controller.py section on lines 92 - 110.
def auth_as_admin_decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # get the user's id from get_jwt_identity
        user_id = get_jwt_identity()
        # fetch the entire user using the id
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        # if user is an admin
        if user.is_admin:
            # allow the decorated function to execute
            return fn(*args, **kwargs)
        # else (user is not an admin)
        else:
            # return error
            return {"error": "Only admin can perform this action"}, 403

    return wrapper