from flask import Blueprint, render_template
from flask_login import login_required
from ..models import Anuncio

bp = Blueprint("main", __name__)

@bp.route("/")
@login_required
def index():
    anuncios = Anuncio.query.order_by(Anuncio.fecha_publicacion.desc()).limit(10).all()
    return render_template("index.html", anuncios=anuncios)