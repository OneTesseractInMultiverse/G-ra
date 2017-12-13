from gora import app
from gora.security.iam import get_user_by_username
from gora.models.graph import (
    Band, 
    User
)
from flask_login import login_user, login_required, current_user
from flask import jsonify, request, render_template


# --------------------------------------------------------------------------
# GET: /ACCOUNT
# --------------------------------------------------------------------------
@app.route('/', methods=['GET'])
@login_required
def get_dashboard_root():
    """
        Gets the main application dashboard view if the user is already 
        authenticated.
        :return: Status response json
    """
    
    user = get_user_by_username(current_user.username)
    bands = user.bands.all()
    
    return render_template(
        "dashboard/index.html",
        bands=bands
    )
    
    

