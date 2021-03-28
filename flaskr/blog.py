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
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    try:
        if check_author and post['author_id'] != g.user['id']:
            abort(403)
    except:
        return post
    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id))
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    return redirect(url_for('blog.index'))


@bp.route('/<int:id>/view')
def view(id):
    post = get_post(id)
    likes = count_likes(id)
    return render_template('blog/view.html', post=post, likes=likes)

def count_likes(post_id):
    db = get_db()
    r = db.execute( "SELECT COUNT(1) FROM likes where post_id =? ", (post_id,))
    count = r.fetchone()[0]
    print(f"Number of liked for post {post_id} is {count}")
    return count

@bp.route('/<int:id>/like')
def like(id):
    db = get_db()
    #print(f"g.user_id is: {g.user['id']}")
    cur = db.execute("SELECT * FROM likes WHERE post_id=? AND user_id=?", (id, g.user['id']))
    rv = cur.fetchall()
    cur.close()
    print(f"rv is:{rv}")
    #print (rv[0] if rv else None) 
    if not rv:
        db.execute(
                    'INSERT INTO likes (post_id, user_id) VALUES (?, ?)'
                , (id, g.user['id']))
        db.commit()
    else:
        db.execute(
                    'DELETE FROM likes WHERE post_id=? AND user_id=?'
                , (id, g.user['id'])
                )
        db.commit()
    return redirect(url_for('blog.view', id=id))