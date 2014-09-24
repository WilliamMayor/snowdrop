import sys
import datetime
import os

from boto.glacier.layer2 import Layer2

from . import app
from .models import db, Archive


LAYER2 = Layer2(
    aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],
    region_name=app.config['AWS_REGION_NAME'])


def upload(path=None):
    with app.app_context():
        a = Archive()
        a.name = '%s - %s' % (datetime.date.today(), os.path.basename(path))
        a.size = os.stat(path).st_size
        a.upload_progress = 0
        db.session.add(a)
        db.session.commit()
        v = LAYER2.get_vault(app.config['AWS_TARGET_VAULT_NAME'])
        v.name = str(v.name)
        writer = v.create_archive_writer(
            part_size=app.config['UPLOAD_CHUNK_SIZE'], description=a.name)
        uploaded_size = 0
        if path is not None:
            fd = open(path, 'rb')
        else:
            fd = sys.stdin
        while True:
            d = fd.read(app.config['UPLOAD_CHUNK_SIZE'])
            if d == '':
                writer.close()
                a.id = writer.get_archive_id()
                a.upload_progress = 100
                break
            else:
                writer.write(d)
                uploaded_size += len(d)
                a.upload_progress = int(100 * uploaded_size / a.size)
            db.session.add(a)
            db.session.commit()
        db.session.add(a)
        db.session.commit()
        if path is not None:
            fd.close()
