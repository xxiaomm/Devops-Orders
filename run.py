import os
from service import app

DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '8080')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)