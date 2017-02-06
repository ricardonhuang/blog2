#coding=utf-8
'''
Created on 2016年12月28日

@author: huangning
'''
from flask import render_template,request,redirect
from sqlalchemy import func
from . import main
from models import db, User, Post, Tag, Comment, posts_tags
import datetime
from uuid import uuid4
from .forms import CommentForm,PostForm
from flask.helpers import url_for



def sidebar_data():
    """Set the sidebar function."""

    # Get post of recent
    recent = db.session.query(Post).order_by(
            Post.publish_date.desc()
        ).limit(5).all()
        
    #Get the hottest posts
    top_posts = Post.query.order_by(Post.read_count.desc()).limit(5).all()

    # Get the tags and sort by count of posts.
    top_tags = db.session.query(
            Tag, func.count(posts_tags.c.post_id).label('total')
        ).join(
            posts_tags
        ).group_by(Tag).order_by('total DESC').limit(10).all()
    return recent, top_posts,top_tags


@main.route('/')
@main.route('/<int:page>')
def home(page=1):
    """View function for home page"""

    posts = Post.query.order_by(
        Post.publish_date.desc()
    ).paginate(page, 10)

    recent,top_posts,top_tags = sidebar_data()

    return render_template('home.html',
                           posts=posts,
                           recent=recent,
                           top_posts=top_posts,
                           top_tags=top_tags)
    
@main.route('/new',methods=['GET','POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(id=str(uuid4()),
                              title=form.title.data)
        new_post.text = form.text.data
        new_post.publish_date = datetime.datetime.now()
       
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('new_post.html',
                           form=form)
    

@main.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_post(id):
    """View function for edit_post."""

    post = Post.query.get_or_404(id)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.publish_date = datetime.datetime.now()

        # Update the post
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.post', post_id=post.id))

    form.title.data = post.title
    form.text.data = post.text
    return render_template('edit_post.html', form=form, post=post)

@main.route('/post/<string:post_id>',methods=['GET','POST'])
def post(post_id):
    """View function for post page"""

    # Form object: `Comment`
    form = CommentForm()
    # form.validate_on_submit() will be true and return the
    # data object to form instance from user enter,
    # when the HTTP request is POST
    if form.validate_on_submit():
        new_comment = Comment(id=str(uuid4()),
                              name=form.name.data)
        new_comment.text = form.text.data
        new_comment.date = datetime.datetime.now()
        new_comment.post_id = post_id
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('main.post',post_id=post_id))
    post = Post.query.get_or_404(post_id)
    if post:
        post.read_count += 1
        db.session.add(post)
        db.session.commit()
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent,top_posts,top_tags = sidebar_data()

    return render_template('post.html',
                           post=post,
                           tags=tags,
                           comments=comments,
                           form=form,
                           recent=recent,
                           top_posts=top_posts,
                           top_tags=top_tags)

@main.route('/tag/<string:tag_name>')
def tag(tag_name):
    """View function for tag page"""
    page = request.args.get('page', 1, type=int)
    # Tag.qurey() 对象才有 first_or_404()，而 db.session.query(Model) 是没有的
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    pagination = tag.posts.order_by(Post.publish_date.desc()).paginate(page, 10)
    posts = pagination.items
    recent, top_posts,top_tags = sidebar_data()
    #print posts
    return render_template('tag.html',
                           tag=tag,
                           posts=posts,
                           recent=recent,
                           top_posts=top_posts,
                           top_tags=top_tags,
                           pagination=pagination)


@main.route('/user/<string:username>')
def user(username):
    """View function for user page"""
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('user.html',
                           user=user,
                           posts=posts,
                           recent=recent,
                           top_tags=top_tags)