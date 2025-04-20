from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db, ShortURL
from utils import generate_short_code
from flask import render_template
from utils import generate_short_code
from models import ShortURL

app = Flask(__name__)

#---------Database Initialization
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

with app.app_context():
    db.create_all()

#------------HomePage------------------
@app.route('/')
def home():
    return render_template('index.html')

#--------------CREATE------------------------
@app.route('/shorten', methods=['POST'])
def create_short_url():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    short_code = generate_short_code()
    new_url = ShortURL(url=url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        'id': new_url.id,
        'url': new_url.url,
        'shortCode': new_url.short_code,
        'createdAt': new_url.created_at,
        'updatedAt': new_url.updated_at
    }), 201


#-------------RETRIEVE----------------------------------
@app.route('/shorten/<short_code>', methods=['GET'])
def get_original_url(short_code):
    url_entry = ShortURL.query.filter_by(short_code=short_code).first()
    if url_entry:
        url_entry.access_count += 1
        db.session.commit()
        return jsonify({
            'id': url_entry.id,
            'url': url_entry.url,
            'shortCode': url_entry.short_code,
            'createdAt': url_entry.created_at,
            'updatedAt': url_entry.updated_at
        }), 200
    return jsonify({'error': 'Short URL not found'}), 404

#--------------UPDATE------------------------
@app.route('/shorten/<short_code>', methods=['PUT'])
def update_url(short_code):
    data = request.get_json()
    new_url = data.get('url')
    if not new_url:
        return jsonify({'error': 'URL is required'}), 400

    url_entry = ShortURL.query.filter_by(short_code=short_code).first()
    if url_entry:
        url_entry.url = new_url
        db.session.commit()
        return jsonify({
            'id': url_entry.id,
            'url': url_entry.url,
            'shortCode': url_entry.short_code,
            'createdAt': url_entry.created_at,
            'updatedAt': url_entry.updated_at
        }), 200
    return jsonify({'error': 'Short URL not found'}), 404

#---------------DELETE------------------
@app.route('/shorten/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    url_entry = ShortURL.query.filter_by(short_code=short_code).first()
    if url_entry:
        db.session.delete(url_entry)
        db.session.commit()
        return '', 204
    return jsonify({'error': 'Short URL not found'}), 404

#---------------GET---------------------
@app.route('/shorten/<short_code>/stats', methods=['GET'])
def get_url_stats(short_code):
    url_entry = ShortURL.query.filter_by(short_code=short_code).first()
    if url_entry:
        return jsonify({
            'id': url_entry.id,
            'url': url_entry.url,
            'shortCode': url_entry.short_code,
            'createdAt': url_entry.created_at,
            'updatedAt': url_entry.updated_at,
            'accessCount': url_entry.access_count
        }), 200
    return jsonify({'error': 'Short URL not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)
