import xmlrpc.client

# Connexion aux services Odoo
url = 'http://localhost:8069'
db = 'MSI'
username = 'nthanhuyen1411@gmail.com'
password = 'uyen'

# Authentification
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

# Accès aux modèles
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
