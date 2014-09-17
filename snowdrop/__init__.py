from flask import Flask

app = Flask(__name__)
app.config.from_object('snowdrop.config.default')
app.config.from_object('snowdrop.config.local')

import views
