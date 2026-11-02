from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Usuario

bp = Blueprint("usuarios", __name__)

@bp.route("/")
@login_required
def lista():
    usuarios = Usuario.query.order_by(Usuario.nombre).all()
    return render_template("usuarios/lista.html", usuarios=usuarios)

@bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        if Usuario.query.filter_by(email=email).first():
            flash("Ya existe un usuario con ese correo", "danger")
            return render_template("usuarios/formulario.html", usuario=None)

        usuario = Usuario(nombre=nombre, email=email)
        usuario.set_password(password)
        db.session.add(usuario)
        db.session.commit()
        flash("Usuario registrado correctamente", "success")
        return redirect(url_for("usuarios.lista"))

    return render_template("usuarios/formulario.html", usuario=None)

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar(id):
    usuario = db.get_or_404(Usuario, id)

    if request.method == "POST":
        email = request.form["email"].strip()
        existe = Usuario.query.filter(Usuario.email == email, Usuario.id != id).first()
        if existe:
            flash("Ya existe otro usuario con ese correo", "danger")
            return render_template("usuarios/formulario.html", usuario=usuario)

        usuario.nombre = request.form["nombre"].strip()
        usuario.email = email
        password = request.form["password"]
        if password:
            usuario.set_password(password)

        db.session.commit()
        flash("Usuario modificado correctamente", "success")
        return redirect(url_for("usuarios.lista"))

    return render_template("usuarios/formulario.html", usuario=usuario)

@bp.route("/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar(id):
    usuario = db.get_or_404(Usuario, id)

    if usuario.id == current_user.id:
        flash("No puedes eliminar tu propio usuario mientras estás conectado", "warning")
        return redirect(url_for("usuarios.lista"))

    db.session.delete(usuario)
    db.session.commit()
    flash("Usuario eliminado correctamente (y sus anuncios)", "success")
    return redirect(url_for("usuarios.lista"))