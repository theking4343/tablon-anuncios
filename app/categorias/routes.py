from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from ..extensions import db
from ..models import Categoria

bp = Blueprint("categorias", __name__)

@bp.route("/")
@login_required
def lista():
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template("categorias/lista.html", categorias=categorias)

@bp.route("/nueva", methods=["GET", "POST"])
@login_required
def nueva():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        descripcion = request.form["descripcion"].strip()

        if Categoria.query.filter_by(nombre=nombre).first():
            flash("Ya existe una categoría con ese nombre", "danger")
            return render_template("categorias/formulario.html", categoria=None)

        db.session.add(Categoria(nombre=nombre, descripcion=descripcion))
        db.session.commit()
        flash("Categoría registrada correctamente", "success")
        return redirect(url_for("categorias.lista"))

    return render_template("categorias/formulario.html", categoria=None)

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar(id):
    categoria = db.get_or_404(Categoria, id)

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        existe = Categoria.query.filter(Categoria.nombre == nombre, Categoria.id != id).first()
        if existe:
            flash("Ya existe otra categoría con ese nombre", "danger")
            return render_template("categorias/formulario.html", categoria=categoria)

        categoria.nombre = nombre
        categoria.descripcion = request.form["descripcion"].strip()
        db.session.commit()
        flash("Categoría modificada correctamente", "success")
        return redirect(url_for("categorias.lista"))

    return render_template("categorias/formulario.html", categoria=categoria)

@bp.route("/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar(id):
    categoria = db.get_or_404(Categoria, id)

    if categoria.anuncios:
        flash("No se puede eliminar: la categoría tiene anuncios asociados", "warning")
        return redirect(url_for("categorias.lista"))

    db.session.delete(categoria)
    db.session.commit()
    flash("Categoría eliminada correctamente", "success")
    return redirect(url_for("categorias.lista"))