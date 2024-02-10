from flask import Flask, render_template, request, abort, redirect, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bjoern
from models import db, Url
from config import generate_hash, is_url, normalize_url

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change_me_please'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'

db.init_app(app)

limiter = Limiter(
    app,
    key_func=get_remote_address
)


@app.before_first_request
def before_first_request():
    db.create_all()


@app.route('/')
@limiter.limit('2/second')
def index():
    return render_template('index.html')


@app.route('/shorten/', methods=['POST'])
@limiter.limit('1/second')
def shorten():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    if not is_url(url):
        return jsonify({'error': 'The URL is invalid'}), 400

    url = normalize_url(url)

    db_value = Url.query.filter_by(forward_to=url).first()
    if not db_value:
        _hash = generate_hash()
        while Url.query.filter_by(hash=_hash).first():
            _hash = generate_hash()

        db_value = Url(hash=_hash, forward_to=url)
        db.session.add(db_value)
        db.session.commit()

    return jsonify({'hash': db_value.hash, 'visited_times': db_value.visited_times}), 200


@app.route('/<shortened>', methods=['GET'])
@limiter.limit('1/second')
def get(shortened: str):
    db_value = Url.query.filter_by(hash=shortened).first()
    if not db_value:
        abort(404)

    db_value.visited_times += 1
    db.session.add(db_value)
    db.session.commit()

    return redirect(db_value.forward_to)


@app.errorhandler(429)
def ratelimit_handler(event):
    return 'Too many requests', 429


@app.errorhandler(404)
def page_not_found(event):
    return render_template('404.html'), 404


if __name__ == "__main__":
    bjoern.run(app, '127.0.0.1', 8000)
