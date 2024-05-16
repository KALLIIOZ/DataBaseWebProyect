from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT r.ID, Usuario_ID, u.Correo_electronico AS Correo_electronico, Videojuego_ID, Calificación, Comentario, v.Nombre AS Nombre_videojuego'
        ' FROM Reseñas r' 
        ' JOIN Usuarios u ON r.Usuario_ID = u.ID' 
        ' JOIN Videojuegos v ON r.Videojuego_ID = v.ID'
    ).fetchall()

    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        calificacion = request.form['Calificación']
        body = request.form['body']
        videojuego_nombre = request.form['videojuego'] 
        error = None

        if not calificacion:
            error = 'Rate is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()

            videojuego_id = db.execute('SELECT ID FROM Videojuegos WHERE Nombre = ?', (videojuego_nombre,)).fetchone()['ID']
            db.execute(
                'INSERT INTO Reseñas (Calificación, Comentario, Usuario_ID, Videojuego_ID)'
                ' VALUES (?, ?, ?, ?)',
                (calificacion, body, g.user['ID'], videojuego_id) 
            )
            db.commit()
            return redirect(url_for('index'))

    db = get_db()
    videojuegos = db.execute('SELECT Nombre FROM Videojuegos').fetchall()

    return render_template('blog/create.html', videojuegos=videojuegos)



def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT r.ID, Calificación, Comentario, Usuario_ID, Nombre_usuario'
        ' FROM Reseñas r JOIN Usuarios u ON r.Usuario_ID = u.ID'
        ' WHERE r.ID = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['Usuario_ID'] != g.user['ID']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        calificacion = request.form['Calificación']
        body = request.form['body']
        error = None

        if not calificacion:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE Reseñas SET Calificación = ?, Comentario = ?'
                ' WHERE ID = ?',
                (calificacion, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM Reseñas WHERE ID = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        db = get_db()
        error = None

        # Verificar si el correo electrónico ya está siendo utilizado por otro usuario
        existing_user = db.execute(
            'SELECT ID FROM Usuarios WHERE Correo_electronico = ? AND ID != ?',
            (new_email, g.user['ID'])
        ).fetchone()

        if existing_user is not None:
            error = f'The email {new_email} is already in use by another user.'

        if error is None:
            db.execute(
                'UPDATE Usuarios SET Nombre_usuario = ?, Correo_electronico = ? WHERE ID = ?',
                (new_username, new_email, g.user['ID'])
            )
            db.commit()
            flash('Your profile has been updated.')
            return redirect(url_for('blog.profile'))

        flash(error)

    return render_template('blog/profile.html')

@bp.route('/addgame', methods=['GET', 'POST'])
@login_required
def add_game():
    if request.method == 'POST':
        nombre = request.form['nombre']
        desarrolladora_nombre = request.form['desarrolladora']
        plataforma_nombre = request.form['plataforma']
        genero_nombre = request.form['genero']
        fecha_lanzamiento = request.form['fecha_lanzamiento']
        precio = request.form['precio']

        error = None

        if not nombre:
            error = 'Nombre del juego es requerido.'
        elif not desarrolladora_nombre:
            error = 'Desarrolladora es requerida.'
        elif not plataforma_nombre:
            error = 'Plataforma es requerida.'
        elif not genero_nombre:
            error = 'Género es requerido.'
        elif not fecha_lanzamiento:
            error = 'Fecha de lanzamiento es requerida.'
        elif not precio:
            error = 'Precio es requerido.'

        if error is None:
            db = get_db()
            desarrolladora = db.execute(
                'SELECT ID FROM Desarrolladores WHERE Nombre = ?',
                (desarrolladora_nombre,)
            ).fetchone()

            if desarrolladora is None:
                error = 'Desarrolladora no encontrada.'
            else:
                plataforma = db.execute(
                    'SELECT ID FROM Plataformas WHERE Nombre = ?',
                    (plataforma_nombre,)
                ).fetchone()

                if plataforma is None:
                    error = 'Plataforma no encontrada.'
                else:
                    genero = db.execute(
                        'SELECT ID FROM Generos WHERE Nombre = ?',
                        (genero_nombre,)
                    ).fetchone()

                    if genero is None:
                        error = 'Género no encontrado.'
                    else:
                        db.execute(
                            'INSERT INTO Videojuegos (Nombre, Desarrollador_ID, Plataforma_ID, Genero_ID, Fecha_lanzamiento, Precio)'
                            ' VALUES (?, ?, ?, ?, ?, ?)',
                            (nombre, desarrolladora['ID'], plataforma['ID'], genero['ID'], fecha_lanzamiento, precio)
                        )
                        db.commit()
                        flash('Juego agregado exitosamente.')
                        return redirect(url_for('blog.add_game'))

        flash(error)

    db = get_db()
    desarrolladoras = db.execute('SELECT Nombre FROM Desarrolladores').fetchall()
    plataformas = db.execute('SELECT Nombre FROM Plataformas').fetchall()
    generos = db.execute('SELECT Nombre FROM Generos').fetchall()

    return render_template('blog/add_game.html', desarrolladoras=desarrolladoras, plataformas=plataformas, generos=generos)

@bp.route('/viewgames')
@login_required
def view_games():
    db = get_db()
    games = db.execute(
        'SELECT v.ID, v.Nombre, d.Nombre AS Desarrollador, d.Contacto AS Contacto, p.Nombre AS Plataforma, g.Nombre AS Genero, v.Fecha_lanzamiento, v.Precio'
        ' FROM Videojuegos v'
        ' JOIN Desarrolladores d ON v.Desarrollador_ID = d.ID'
        ' JOIN Plataformas p ON v.Plataforma_ID = p.ID'
        ' JOIN Generos g ON v.Genero_ID = g.ID'
    ).fetchall()
    return render_template('blog/view_games.html', games=games)
