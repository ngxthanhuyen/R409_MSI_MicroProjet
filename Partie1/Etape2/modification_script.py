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
    
# Met à jour les informations de l'utilisateur
def update_user_info(user_id, new_email=None, new_password=None):
    values = {}
    if new_email:
        values['email'] = new_email
    if new_password:
        values['password'] = new_password

    if values:
        success = models.execute_kw(db, uid, password, 'res.users', 'write', [[user_id], values])
        if success:
            print(f"Informations de l'utilisateur {user_id} mises à jour.")
        else:
            print("Échec de la mise à jour.")

# Récupère les groupes d'un utilisateur
def get_user_groups(user_id):
    user_data = models.execute_kw(db, uid, password, 'res.users', 'read', [user_id], {'fields': ['groups_id']})
    return user_data[0]['groups_id']

# Modifie les groupes d’un utilisateur
def modify_user_groups(user_id, group_ids_to_add=None, group_ids_to_remove=None):
    group_ids_to_add = group_ids_to_add or []
    group_ids_to_remove = group_ids_to_remove or []

    current_groups = get_user_groups(user_id)

    for group_id in group_ids_to_add:
        if group_id not in current_groups:
            current_groups.append(group_id)

    for group_id in group_ids_to_remove:
        if group_id in current_groups:
            current_groups.remove(group_id)

    # Obtenir dynamiquement les groupes de type utilisateur
    user_type_category_ids = models.execute_kw(
        db, uid, password,
        'ir.module.category', 'search',
        [[['name', 'ilike', 'Utilisateur']]]
    )

    user_type_group_ids = models.execute_kw(
        db, uid, password,
        'res.groups', 'search',
        [[['category_id', 'in', user_type_category_ids]]]
    )

    # Supprimer tous les groupes de type utilisateur
    current_groups = [gid for gid in current_groups if gid not in user_type_group_ids]

    # Ajouter le groupe utilisateur souhaité (par ex. Internal User = 1)
    current_groups.append(1)

    # Mise à jour des groupes
    models.execute_kw(
        db, uid, password,
        'res.users', 'write',
        [[user_id], {'groups_id': [(6, 0, current_groups)]}]
    )
    print(f"Groupes mis à jour pour l'utilisateur {user_id}.")
