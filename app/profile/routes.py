from flask import render_template
from flask_login import login_required, current_user
from app.models import Post, Comment, Media
from app.profile import profile_bp


@profile_bp.route('/')
@login_required
def index():
    posts = Post.query.filter_by(author_id=current_user.id)\
                      .order_by(Post.created_at.desc()).all()
    comments = Comment.query.filter_by(author_id=current_user.id)\
                            .order_by(Comment.created_at.desc()).all()
    media_files = Media.query.filter_by(uploaded_by=current_user.id)\
                             .order_by(Media.created_at.desc()).all()
    return render_template('profile/index.html', posts=posts,
                           comments=comments, media_files=media_files)
