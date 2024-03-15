import os
from flask_frozen import Freezer
from server import app

if 'FREEZER_BASE_URL' in os.environ:
    app.config['FREEZER_BASE_URL'] = os.environ['FREEZER_BASE_URL']

freezer = Freezer(app)

if __name__ == '__main__':
    print("Freezing the site...")
    freezer.freeze()
    print("Site frozen.")
