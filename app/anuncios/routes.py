from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Anuncio, Categoria, Usuario

bp = Blueprint("anuncios", __name__)

@bp.route("/")
@login_required
def lista():
    anuncios = Anuncio.query.order_by(Anuncio.fecha_publicacion.desc()).all()
    return render_template("anuncios/lista.html", anuncios=anuncios)

@bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    usuarios = Usuario.query.order_by(Usuario.nombre).all()

    if not categorias:
        flash("Primero debes registrar al menos una categoría", "warning")
        return redirect(url_for("categorias.nueva"))

    if request.method == "POST":
        anuncio = Anuncio(
            titulo=request.form["titulo"].strip(),
            contenido=request.form["contenido"].strip(),
            categoria_id=int(request.form["categoria_id"]),
            usuario_id=int(request.form["usuario_id"]),
        )
        db.session.add(anuncio)
        db.session.commit()
        flash("Anuncio registrado correctamente", "success")
        return redirect(url_for("anuncios.lista"))

    return render_template("anuncios/formulario.html", anuncio=None,
                           categorias=categorias, usuarios=usuarios)

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar(id):
    anuncio = db.get_or_404(Anuncio, id)
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    usuarios = Usuario.query.order_by(Usuario.nombre).all()

    if request.method == "POST":
        anuncio.titulo = request.form["titulo"].strip()
        anuncio.contenido = request.form["contenido"].strip()
        anuncio.categoria_id = int(request.form["categoria_id"])
        anuncio.usuario_id = int(request.form["usuario_id"])
        db.session.commit()
        flash("Anuncio modificado correctamente", "success")
        return redirect(url_for("anuncios.lista"))

    return render_template("anuncios/formulario.html", anuncio=anuncio,
                           categorias=categorias, usuarios=usuarios)

@bp.route("/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar(id):
    anuncio = db.get_or_404(Anuncio, id)
    db.session.delete(anuncio)
    db.session.commit()
    flash("Anuncio eliminado correctamente", "success")
    return redirect(url_for("anuncios.lista"))