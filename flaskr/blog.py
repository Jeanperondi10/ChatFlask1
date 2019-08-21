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



#def pegarDadosPilha():
    #cont=len(msgunidpilha)
    #while (pilha.qsize() != 0):
    #    msgunidpilha = pilha.get()
    #    msgpilha[cont]=msgunidpilha
    #    cont+=1
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

@bp.route('/data')
def data():
    #loop persistente que renderizará o template local
    #FUNCOES: get()-retorna um valor, retirando da pilha
    #         qsize()-retorna o tamanho da pilha

    #variavel texto q será retornada
    #template=""

    #print(msgpilha.nome, " | ", g.user['id'])
    #for msg in msgpilha:
    #    if msg.nome==g.user['id']:
    #       print("\n\nPEGANDO MENSAGEM!\nUsuario=", msg.nome, "\n msg= ", msg.msg, "\nTamanho da pilha= ",pilha.qsize())
    #       template += "<article class='post-normal'><p class='pessoa-msg'><b>" + msg.nome + "</b></p><p class='body-msg'>" + msg.msg + "</p></article>"


    #retornar o texto HTML ja formatado
    return ""

@bp.route('/index', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':

        body = request.form['body']
        error = None
        conta=True

        #Objeto que irá fazer o armazenamento dos dados
        #ATRIBUTOS: Nome do usuario, Corpo da msg e hora
        #Adicionar na pilha global

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

            ##########################
            # Pegar o nome do usuario
            #mensagem.nome=g.user['id']
            #mensagem.msg = body
            #pilha.put(mensagem)
            #data()
            #print("NOVA MENSAGEM!\nUsuario=",mensagem.nome,"\n msg= ",mensagem.msg,"\nTamanho da pilha= ",pilha.qsize())
            ##########################

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

    #if check_author and post['author_id'] != g.user['id']:
     #   abort(403)

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
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))