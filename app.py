from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db, ShortURL
from utils import generate_short_code

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

with app.app_context():
    db.create_all()

#--------------CREATE------------------------
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

if __name__ == "__main__":
    app.run(debug=True)
