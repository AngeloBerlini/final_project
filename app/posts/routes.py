from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Post, Circuit, Comment, Media
from app.utils import save_upload
from app.posts import posts_bp

CATEGORIES = ['analisi']


@posts_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    circuits = Circuit.query.order_by(Circuit.name).all()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        body = request.form.get('body', '').strip()
        circuit_id = request.form.get('circuit_id', type=int)

        if not all([title, body, circuit_id]):
            flash('Compila tutti i campi obbligatori.', 'danger')
            return render_template('posts/form.html', circuits=circuits)

        post = Post(title=title, body=body, category='analisi',
                    circuit_id=circuit_id, team_id=current_user.team_id,
                    author_id=current_user.id)
        db.session.add(post)
        db.session.commit()

        saved = sum(
            1 for f in request.files.getlist('media')
            if save_upload(f, post.id, current_user.id)
        )
        if saved:
            flash(f'{saved} file caricati.', 'success')

        flash('Post creato con successo.', 'success')
        return redirect(url_for('hub.index'))
    return render_template('posts/form.html', circuits=circuits, categories=CATEGORIES)



@posts_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if post.team_id != current_user.team_id:
        abort(403)
    if post.author_id != current_user.id and not current_user.is_admin():
        abort(403)

    circuits = Circuit.query.order_by(Circuit.name).all()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        body = request.form.get('body', '').strip()
        circuit_id = request.form.get('circuit_id', type=int)

        if not all([title, body, circuit_id]):
            flash('Compila tutti i campi obbligatori.', 'danger')
            return render_template('posts/form.html', post=post, circuits=circuits)

        post.title = title
        post.body = body
        post.circuit_id = circuit_id
        db.session.commit()
        flash('Analisi aggiornata.', 'success')
        return redirect(url_for('hub.index'))
    return render_template('posts/form.html', post=post, circuits=circuits,
                           categories=CATEGORIES)


@posts_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.team_id != current_user.team_id:
        abort(403)
    if post.author_id != current_user.id and not current_user.is_admin():
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post eliminato.', 'success')
    return redirect(url_for('hub.index'))


@posts_bp.route('/<int:post_id>/media', methods=['POST'])
@login_required
def add_media(post_id):
    post = Post.query.get_or_404(post_id)
    if post.team_id != current_user.team_id:
        abort(403)
    if post.author_id != current_user.id and not current_user.is_admin():
        abort(403)
    saved = sum(
        1 for f in request.files.getlist('media')
        if save_upload(f, post_id, current_user.id)
    )
    if saved:
        flash(f'{saved} file caricati con successo.', 'success')
    else:
        flash('Nessun file valido caricato. Formati accettati: PNG, JPG, PDF, CSV.', 'warning')
    return redirect(url_for('hub.index'))
