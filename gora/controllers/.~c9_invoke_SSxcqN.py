from gora import app

from gora.models.graph import (
    Band, 
    User
)
from flask_login import login_user, login_required
from flask import jsonify, request, render_template

# --------------------------------------------------------------------------
# GET: /ACCOUNT
# --------------------------------------------------------------------------
@app.route('/band/add', methods=['GET'])
@login_required
def get_add_band():
    return render_template(
        "band/c.html"
    )
































































