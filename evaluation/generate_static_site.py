from flask_frozen import Freezer
from server import app

freezer = Freezer(app)

if __name__ == '__main__':
    print("Freezing the site...")
    freezer.freeze()
    print("Site frozen.")
