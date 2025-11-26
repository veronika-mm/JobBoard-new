import os
import secrets
from flask import Flask, jsonify, redirect, url_for, render_template, flash, request
from sqlalchemy.sql.functions import current_user
from forms import RegistrationForm, LoginForm, JobForm, UpdateAccountForm
from flask_login import login_manager, current_user, login_user, logout_user, login_required, LoginManager
from db import init_db, db
from models import User, Job, Jobs
import requests
import logging


app = Flask(__name__)

app.config['SECRET_KEY'] = 'e327222739cdb48d67dc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

init_db(app)

login_meneger = LoginManager()
login_manager.login_view = 'login'
login_meneger.init_app(app)

@login_meneger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data).first()
        if existing:
            flash(f"ასეთი მომხმარებელი უკვე არსებობს", category='danger')
            return redirect(url_for('login'))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"თქვენ წარმატებით დარეგისტრირდით საიტზე", category='success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f"შენ წარმატებით გაიარე ავტორიზაცია", category='success')
            logging.info(f"წარმატებული {user.email}")
            return redirect(url_for('index'))
        else:
            flash(f"არასწორი იმეილი ან პაროლი", category='danger')
            logging.warning(f"Failed {form.email.data}")
    return render_template('login.html', title='Login', form=form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            random_hex = secrets.token_hex(8)
            _,format_ext = os.path.splitext(form.image.data.filename)
            picture_x = random_hex + format_ext
            picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_x)
            form.image.data.save(picture_path)
            current_user.image = picture_x
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"ექაუნთი წარმატებით განახლდა", category='success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html', form=form)


API_KEY = "bb4beb2e24b54775a08fbca951c53d19"

#ვაკანსიების გვერდს API-KEY არ ქონდა და ორი ვარიანტი გავაკეთე, API-KEY-ით და API-KEY-ის გარეშე
@app.route('/news', methods=['GET'] )
def news():
    url =f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
    response = requests.get(url)

    news_data = None
    if response.status_code == 200:
        news_data = response.json()
    else:
        flash(f"ERROR", category='danger')

    return render_template('news.html', news=news_data)

@app.route('/careers')
def careers():
    url =f"https://remotive.com/api/remote-jobs"
    response = requests.get(url)

    careers_data = None
    if response.status_code == 200:
        careers_data = response.json()
    else:
        flash(f"ERROR", category='danger')
    return render_template('careers.html', careers=careers_data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f"შენ გახვედი პროგრამიდან", category='success')
    return redirect(url_for('index'))



@app.route('/job/add', methods=['GET', 'POST'])

def add_job():
    form = JobForm()

    if form.validate_on_submit():
        #title = form.title.data

        new_job = Jobs(
            title=form.title.data,
            short_description=form.short_description.data,
            long_description=form.long_description.data,
            company=form.company.data,
            salary=form.salary.data,
            location=form.location.data,
            author_id=current_user.id

        )

        db.session.add(new_job)
        db.session.commit()

        form.title.data = ''
        form.short_description.data = ''
        form.long_description.data = ''
        form.company.data = ''
        form.salary.data = None
        form.location.data = None

        flash(f"Job { form.title.data } დაემატა წარმატებით", 'success')
        return redirect(url_for('add_job'))

    our_jobs = Jobs.query.order_by(Jobs.date_posted.desc()).all()
    return render_template('add_job.html', form=form, our_jobs=our_jobs)




@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = JobForm()
    title_to_update = Jobs.query.get_or_404(id)
    if request.method == 'POST':
        title_to_update.title = request.form['title']
        title_to_update.short_description =request.form['short_description']
        title_to_update.short_description = request.form['short_description']
        title_to_update.company = request.form['company']
        title_to_update.salary = request.form['salary']
        title_to_update.location = request.form['location']
        title_to_update.author_id = current_user.id
        try:
            db.session.commit()
            flash(f"ვაკანსია წარმატებით განახლდა", 'success')
        except:
            flash(f"სამწუხაროდ მონაცემები არ შეიცვალა", 'danger')
            return render_template("update.html", form=form, title_to_update=title_to_update)
    else:
        return render_template('update.html', form=form, title_to_update=title_to_update)



@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    job_to_delete = Jobs.query.get_or_404(id)
    form = JobForm()

    try:
        db.session.delete(job_to_delete)
        db.session.commit()
        flash(f"Job '{job_to_delete.title}' წარმატებით წაიშალა", 'success')
        our_job = User.query.order_by(Jobs.date_posted.desc()).first()
        return render_template('add_job.html', form=form, our_job=our_job)

    except:
        flash(f"სამწუხაროდ, ვაკანსიის წაშლა შეუძლებელია")
        return render_template('add_job.html', form=form, our_job=our_job)




@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    our_jobs = Job.query.order_by(Job.date_posted.desc()).all()
    return render_template('jobs.html', our_jobs=our_jobs)




@app.errorhandler(404)
def page_not_found(e):
    return '<h1>რას ეძებ ჩემი ძმა?</h1>'

@app.errorhandler(500)
def internal_server_error(e):
    return '<h1>500 - სერვერის შეცდომა</h1>'

if __name__ == '__main__':
    app.run(debug=True)
