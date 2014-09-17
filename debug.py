import os

import snowdrop

if __name__ == '__main__':
    if not os.path.isfile('snowdrop/glacier.db'):
        snowdrop.models.db.create_all()
    snowdrop.app.run(debug=True)
