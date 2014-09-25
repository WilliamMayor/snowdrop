from flask import render_template, request, jsonify
from sqlalchemy.sql import func

from . import app, glacier
from .models import db, Archive


def format_size(bytes):
    if bytes < 1024:
        return '%dB' % bytes
    bytes = bytes / 1024.0
    if bytes < 1024:
        return '%.0fKB' % bytes
    bytes = bytes / 1024.0
    if bytes < 1024:
        return '%.0fMB' % bytes
    bytes = bytes / 1024.0
    if bytes < 1024:
        return '%.0fGB' % bytes
    bytes = bytes / 1024.0
    if bytes < 1024:
        return '%.0fTB' % bytes
    bytes = bytes / 1024.0
    return '%.0fPB' % bytes


def format_cost(bytes):
    gb = bytes / (1024.0 * 1024 * 1024)
    cost = app.config['AWS_GLACIER_DOLLAR_PER_GB'] * gb
    return '$%.2f' % cost


def stats():
    try:
        vault_size = db.session.query(func.sum(Archive.size)).first()[0]
        monthly_cost = format_cost(vault_size)
        vault = Archive.query.all()
        for a in vault:
            a.cost = format_cost(a.size)
            a.size = format_size(a.size)
        return {
            'vault': vault,
            'earliest': Archive.query.order_by(Archive.date).first().date,
            'latest': Archive.query.order_by(Archive.date.desc()).first().date,
            'vault_size': format_size(vault_size),
            'monthly_cost': monthly_cost}
    except:
        return {}


@app.route('/')
def home():
    return render_template('home.html', **stats())


@app.route('/delete/', methods=['POST'])
def delete():
    for aid in request.get_json().get('aids', []):
        glacier.delete(aid)
    return jsonify(message='OK')
