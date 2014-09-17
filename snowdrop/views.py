from flask import render_template
from sqlalchemy.sql import func

from . import app
from .models import db, Archive


def stats():
    try:
        vault_size = db.session.query(func.sum(Archive.size)).first()[0]
        vault_size = vault_size / (1024 * 1024 * 1024)
        monthly_cost = app.config['AWS_GLACIER_DOLLAR_PER_GB'] * vault_size
        vault = Archive.query.all()
        for a in vault:
            a.size = a.size / (1024 * 1024 * 1024)
            a.cost = app.config['AWS_GLACIER_DOLLAR_PER_GB'] * a.size
        return {
            'vault': vault,
            'earliest': Archive.query.order_by(Archive.date).first().date,
            'latest': Archive.query.order_by(Archive.date.desc()).first().date,
            'vault_size': vault_size,
            'monthly_cost': monthly_cost}
    except:
        return {}


@app.route('/')
def home():
    return render_template('home.html', **stats())
