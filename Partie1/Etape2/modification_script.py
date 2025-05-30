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

# Vérifie si un utilisateur existe
def user_exists(login):
    user_ids = models.execute_kw(db, uid, password, 'res.users', 'search', [[('login', '=', login)]])
    if user_ids:
        return user_ids[0]
    else:
        print(f"Utilisateur avec login '{login}' non trouvé.")
        return None
