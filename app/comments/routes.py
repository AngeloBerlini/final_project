from flask import redirect, url_for, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Comment, Post
from app.comments import comments_bp


@comments_bp.route('/new', methods=['POST'])
@login_required
def create():
    post_id = request.form.get('post_id', type=int)
    body = request.form.get('body', '').strip()
    post = Post.query.get_or_404(post_id)
    if post.team_id != current_user.team_id:
        abort(403)
    if body:
        comment = Comment(body=body, post_id=post_id, author_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('hub.index'))


@comments_bp.route('/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post = Post.query.get_or_404(comment.post_id)
    if post.team_id != current_user.team_id:
        abort(403)
    if comment.author_id != current_user.id and not current_user.is_admin():
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('hub.index'))
