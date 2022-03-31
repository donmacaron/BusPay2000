import os
from ipaddress import ip_address
from BusPay2000 import app


port = int(os.environ.get("PORT", 5000))
if __name__ == '__main__':
    app.run(host=port, debug=True)
