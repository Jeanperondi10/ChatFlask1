from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

bp = Blueprint('blog', __name__)

@bp.route('/')
def inicio():
    return render_template('blog/home.html')

@bp.route('/index')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created ASC '
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/index', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':

        body = request.form['body']
        error = None
        conta=True

        #db = get_db()
        #autor = db.execute(
        #    'SELECT author_id'
        #    ' FROM post p JOIN user u ON p.author_id = u.id'
        #    ' ORDER BY created ASC '
        #).fetchone()
        #print(autor)


            #sif posts[len(posts)-1].author_id == g.user("id"):
             #   conta=False
            #else:
             #   conta=True


        if not body:
            error = 'Mensagem Vazia'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (body, author_id, cont)'
                ' VALUES (?, ?, ?)',
                (body, g.user['id'], conta)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')




def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        body = request.form['body']
        error = None

        if not body:
            error = 'Mensagem vazia'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET body = ?'
                ' WHERE id = ?',
                (body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))