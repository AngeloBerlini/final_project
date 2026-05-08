import os
from flask import current_app, send_file, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Media, Post
from app.media import media_bp


@media_bp.route('/<int:media_id>/download')
@login_required
def download(media_id):
    media = Media.query.get_or_404(media_id)
    post = Post.query.get_or_404(media.post_id)
    if post.team_id != current_user.team_id:
        abort(403)
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], media.filename)
    if not os.path.exists(path):
        abort(404)
    return send_file(path, download_name=media.original_name, as_attachment=True)


@media_bp.route('/<int:media_id>/delete', methods=['POST'])
@login_required
def delete(media_id):
    media = Media.query.get_or_404(media_id)
    post = Post.query.get_or_404(media.post_id)
    if post.team_id != current_user.team_id:
        abort(403)
    if post.author_id != current_user.id and not current_user.is_admin():
        abort(403)
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], media.filename)
    if os.path.exists(path):
        os.remove(path)
    db.session.delete(media)
    db.session.commit()
    flash('File eliminato.', 'success')
    return redirect(url_for('posts.detail', post_id=post.id))
