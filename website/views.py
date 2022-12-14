import os

from website.auth import login
from . import db
from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from .models import Post, Comment, Like
from datetime import datetime
import uuid
filename = uuid.uuid4().hex

# pathpics = os.path.join()
# print(pathpics)

views = Blueprint("views", __name__)

@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    # print(current_user.id, current_user.email)
    current_time = datetime.utcnow()
    return render_template('home.html', user = current_user, posts=posts, current_time=current_time)

@views.route('/create-blog', methods=['GET', 'POST'])
@login_required
def create_blog():
    if request.method=="POST":
        blogtitle = request.form.get('blogtitle')
        blogdesc = request.form.get('blogdesc')
        blogtype = request.form.get('blogtype')
        blogimage = request.files['blogimage']

        if not blogimage:
            blogimage.filename = 'blog-default.png'
        else:
            pathdir = os.path.abspath(os.path.dirname(__file__))
            pathpics = os.path.join(pathdir, "static/assets/Blog-post")
            blogimage.filename = uuid.uuid4().hex + ".png"
            blogimage.save(os.path.join(pathpics, blogimage.filename))

        post = Post(blogtitle=blogtitle, blogdesc=blogdesc, blogtype=blogtype, blogimage=blogimage.filename, author=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Post Created!", category='success')
        # return redirect(url_for('views.home'))

    return render_template('create_blog.html', user=current_user)

@views.route('/each-blog/<int:blogid>', methods=['GET', 'POST'])
@login_required
def show_blog(blogid):
    if request.method == 'POST':
        commentdesc = request.form.get('commentdesc')
        comment = Comment(commentdesc=commentdesc, author=current_user.id, post_id=blogid)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('views.show_blog', blogid=blogid))
    post = Post.query.filter_by(blogid=blogid).first()
    return render_template('eachblog.html', user=current_user,post=post)

@views.route('update-blog/<int:blogid>', methods=['GET', 'POST'])
@login_required
def update_blog(blogid):
    if request.method == 'POST':
        blogtitle = request.form.get('blogtitle')
        blogdesc = request.form.get('blogdesc')
        blogtype = request.form.get('blogtype')
        blogimage = request.files['blogimage']
        print("----------------------------------------------------")
        print(blogtitle, blogdesc, blogtype, blogimage.filename)
        print("----------------------------------------------------")
        post = Post.query.filter_by(blogid=blogid).first()
        print(post.blogid, post.blogtitle, post.blogdesc, post.blogtype, post.blogimage)
        if not post:
            flash("post does not exist.", category='error')
        elif current_user.id != post.author:
            flash('You do not have permission to update this post.', category='error')
        else:
            post.blogtitle = blogtitle
            post.blogdesc = blogdesc 
            post.blogtype = blogtype 
            if blogimage:
                pathdir = os.path.abspath(os.path.dirname(__file__))
                pathpics = os.path.join(pathdir, "static/assets/Blog-post")
                blogimage.filename = uuid.uuid4().hex + ".png"
                blogimage.save(os.path.join(pathpics, blogimage.filename))
                if post.blogimage != 'blog-default.png':
                    os.remove(os.path.join(pathpics, post.blogimage))
                post.blogimage = blogimage.filename
            db.session.commit()
            flash('Updated successfully', category='success')
            # redirect('')

    post = Post.query.filter_by(blogid=blogid).first()
    return render_template('update_blog.html', post = post, user=current_user)


@views.route('delete-blog/<int:blogid>', methods=['GET', 'POST'])
@login_required
def delete_blog(blogid):
    post = Post.query.filter_by(blogid=blogid).first()

    if not post:
        flash("post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        pathdir = os.path.abspath(os.path.dirname(__file__))
        pathpics = os.path.join(pathdir, "static/assets/Blog-post")
        if post.blogimage != 'blog-default.png':
            os.remove(os.path.join(pathpics, post.blogimage))
        db.session.delete(post)
        db.session.commit()
    
    return redirect(url_for('views.home'))

@views.route('delete-comment/<int:commentid>')
@login_required
def delete_comment(commentid):
    comment = Comment.query.filter_by(commentid=commentid).first()
    post = Post.query.filter_by(blogid = comment.post_id).first()
    if not comment:
        flash('comment does not exist', category='error')
    elif current_user.id != comment.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('views.show_blog', blogid = post.blogid))

@views.route('like-post/<int:blogid>')
@login_required
def like_post(blogid):
    post = Post.query.filter_by(blogid = blogid).first()
    like = Like.query.filter_by(author=current_user.id, post_id=blogid).first()
    if not post:
        flash('Post does not exist', category='success')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        dolike = Like(author = current_user.id, post_id=blogid)
        db.session.add(dolike)
        db.session.commit()
    return redirect(url_for('views.show_blog', blogid=blogid))