import os
from ipaddress import ip_address
from BusPay2000 import app
from BusPay2000 import db

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 33507)), debug=True)
