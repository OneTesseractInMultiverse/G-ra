from gora import app
from gora.security.iam import get_user_by_username
from gora.models.graph import (
    Band, 
    User
)
from flask_login import login_user, login_required, current_user
from flask import jsonify, request, render_template, redirect, url_for

import uuid

# --------------------------------------------------------------------------
# GET: /BAND/ADD
# --------------------------------------------------------------------------
@app.route('/band/add', methods=['GET'])
@login_required
def get_add_band():
    return render_template(
        "band/add.html"
    )
    
# --------------------------------------------------------------------------
# POST: /BAND/ADD
# --------------------------------------------------------------------------
@app.route('/band/add', methods=['POST'])
@login_required
def post_add_band():
    
    try:

        band = Band(
            band_id = uuid.uuid4(),
            name = request.form['name'],
            description = request.form['description'],
            genres = request.form['genres'],
            logo_url = request.form['logo']
            
        )
        
        band.set_founded(
            day = request.form['day'],
            month = request.form['month'],
            year = request.form['year']
        )
        band.save()
        user = get_user_by_username(current_user.username)
        user.bands.connect(band)
        user.save()
        band.members.connect(user)
        band.save()
        return redirect(url_for('get_dashboard_root'))
    except Exception as e:
        print(e)
        return render_template(
            "band/add.html", 
            error= "Error processing request"
        )