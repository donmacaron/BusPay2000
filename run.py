from ipaddress import ip_address
from BusPay2000 import app


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
