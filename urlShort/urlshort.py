import os
import json
from flask import Blueprint ,abort, jsonify
from flask.globals import request, session
from flask.helpers import flash, url_for
from flask.templating import render_template
from werkzeug.utils import redirect, secure_filename

bp = Blueprint('urlshort', __name__)

@bp.route('/')
def home():
    return render_template('home.html', codes=session.keys())

@bp.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = dict()

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('That short name already taken. Please select another name.')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('urlShort/static/user_files/' + full_name)
            urls[request.form['code']] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True
        return render_template('your-url.html', code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home'))

@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
