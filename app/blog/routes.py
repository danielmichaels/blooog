from flask import render_template, redirect, request, flash, url_for, \
    current_app

from app import db
from run import app
from . import blog
from .forms import Login, EntryForm, SearchBar
from flask_login import login_required, logout_user, login_user
from app.models import User, Entries

MAX_SEARCH_RESULTS = 20


# ------ GENERAL ROUTES ----------#


@blog.route('/')
@blog.route('/index')
def index():
    page = request.args.get('page', 1,
                            type=int)  # sets the pagination start point
    pagination = Entries.query.order_by(Entries.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    entries_list = pagination.items
    return render_template('blog/index.html', pagination=pagination,
                           entries=entries_list)


@blog.route('/search', methods=('GET',
                                'POST'))  # FTS only returning the entire post in which obj search for is found
def search():
    form = SearchBar()
    entries = Entries.query.whoosh_search(
        request.args.get('query', MAX_SEARCH_RESULTS)).all()
    return render_template('blog/index_search.html', entries=entries,
                           form=form)  # needed new template due to poor planning (pagination)


@blog.route('/index/<int:id>/<slug>')
def post(id, slug):
    post = Entries.query.get_or_404(id)
    slug = post.slug
    return render_template('blog/post_.html', post=post, slug=slug)


@blog.route('/entry', methods=('GET', 'POST'))
@login_required
def entry():
    form = EntryForm()
    if form.validate_on_submit():
        entry = Entries(
            title=form.title.data,
            content=form.content.data,
            # category=form.category.data,
        )
        db.session.add(entry)
        db.session.commit()
        flash('Success!')
        return redirect(url_for('blog.index'))
    return render_template('blog/entry.html', form=form)


# ----------- Edit / Delete ------ #
@blog.route('/index/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    entry = Entries.query.get_or_404(id)  # query for object on db
    form = EntryForm(obj=entry)  # return 'entries' as an object
    if form.validate_on_submit():
        entry.title = form.title.data  # call everything entered in as from.title.data to be saved as entry.title for DB
        entry.content = form.content.data
        # entry.category = form.category.data
        db.session.commit()
        flash('Post Successfully Updated')
        return redirect(url_for('.index', id=entry.id))
    form.title.data = entry.title
    form.content.data = entry.content
    return render_template('blog/entry.html', form=form)


@blog.route('/index/delete/<int:id>')
@login_required
def delete(id):
    entry = Entries.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    flash('Post Deleted')
    return redirect(url_for('blog.index'))


# ------ About / Contact ---------#

@blog.route('/about')
def about():
    return render_template('blog/about.html')


@blog.route('/contact')
def contact():
    return render_template('blog/contact.html')


# ------ LOGIN / LOGOUT ----------#

@blog.route('/login', methods=('GET', 'POST'))
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash("Invalid Password or Username")
            return redirect(url_for('blog.login'))
        login_user(user, form.stay_logged_in.data)
        flash("Successfully Logged In!")
        return redirect(request.args.get('next') or (url_for('blog.index')))
    return render_template('blog/login.html', form=form)


@blog.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out!')
    return redirect(url_for('blog.index'))


# --------- ERRORS ------------#

@app.errorhandler(404)
def error(error):
    return render_template('blog/error.html'), 404
