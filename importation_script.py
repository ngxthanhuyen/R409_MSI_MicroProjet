import csv
import requests
import json
import random
import string
from datetime import datetime
import logging

# Configuration Odoo
ODOO_URL = "http://localhost:8069"  
ODOO_DB = "MSI"               
ODOO_USER = "nthanhuyen1411@gmail.com"                
ODOO_PASSWORD = "uyen"            

# Configuration du fichier de log
LOG_FILE = "odoo_user_import.log"

# Initialisation du logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_action(action, status, details=None):
    """Fonction pour logger les actions"""
    log_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'action': action,
        'status': status,
        'details': details
    }
    logging.info(json.dumps(log_entry))

def authenticate():
    """Authentification à l'API Odoo"""
    try:
        url = f"{ODOO_URL}/jsonrpc"
        headers = {'Content-Type': 'application/json'}
        auth_data = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "authenticate",
                "args": [ODOO_DB, ODOO_USER, ODOO_PASSWORD, {}]
            },
            "id": 1
        }
        response = requests.post(url, json=auth_data, headers=headers).json()
        uid = response.get("result")
        
        if uid:
            log_action("authenticate", "success", {"user": ODOO_USER})
            return uid
        else:
            log_action("authenticate", "failed", {"error": "Authentication failed", "response": response})
            return None
    except Exception as e:
        log_action("authenticate", "error", {"error": str(e)})
        return None


def generate_password(length=12):
    """Génère un mot de passe aléatoire"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))


def create_user(uid, user_data):
    """Crée un utilisateur dans Odoo"""
    try:
        # Génération du mot de passe
        password = generate_password()
        
        url = f"{ODOO_URL}/jsonrpc"
        headers = {'Content-Type': 'application/json'}
        create_user_data = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [ODOO_DB, uid, ODOO_PASSWORD, "res.users", "create", [{
                    "name": f"{user_data['prenom']} {user_data['nom']}",
                    "login": user_data['login'],
                    "email": user_data['email'],
                    "password": password,
                    "active": True
                }]]
            },
            "id": 3
        }
        response = requests.post(url, json=create_user_data, headers=headers).json()
        result = response.get("result")
        
        if result:
            log_action("create_user", "success", {
                "user_data": user_data,
                "user_id": result,
                "password": password  # Dans un environnement réel, ne pas logger le mot de passe
            })
            
            # Envoyer un email avec les identifiants (simulé ici)
            send_credentials_email(user_data['email'], user_data['login'], password)
            
            return result
        else:
            log_action("create_user", "failed", {
                "user_data": user_data,
                "error": response.get("error", "Unknown error")
            })
            return None
    except Exception as e:
        log_action("create_user", "error", {
            "user_data": user_data,
            "error": str(e)
        })
        return None
    
def send_credentials_email(email, login, password):
    """Fonction simulée pour envoyer les identifiants par email"""
    # Dans une implémentation réelle, utiliser le module smtplib ou l'API Odoo pour envoyer des emails
    print(f"Envoi d'email à {email} avec login: {login} et mot de passe: {password}")
    log_action("send_credentials_email", "success", {
        "email": email,
        "login": login
        # Ne pas logger le mot de passe dans les logs réels
    })

def get_group_id(uid, group_name):
    """Récupère l'ID d'un groupe par son nom"""
    try:
        url = f"{ODOO_URL}/jsonrpc"
        headers = {'Content-Type': 'application/json'}
        search_data = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [ODOO_DB, uid, ODOO_PASSWORD, "res.groups", "search", [[("name", "=", group_name)]]]
            },
            "id": 2
        }
        response = requests.post(url, json=search_data, headers=headers).json()
        result = response.get("result")
        
        if result:
            group_id = result[0]
            log_action("get_group_id", "success", {"group_name": group_name, "group_id": group_id})
            return group_id
        else:
            log_action("get_group_id", "failed", {"group_name": group_name, "error": "Group not found"})
            return None
    except Exception as e:
        log_action("get_group_id", "error", {"group_name": group_name, "error": str(e)})
        return None
    
def assign_permissions(uid, user_id, group_id):
    """Attribue des permissions à un utilisateur"""
    try:
        url = f"{ODOO_URL}/jsonrpc"
        headers = {'Content-Type': 'application/json'}
        assign_data = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [ODOO_DB, uid, ODOO_PASSWORD, "res.users", "write", [[user_id], {"groups_id": [(4, group_id)]}]]
            },
            "id": 4
        }
        response = requests.post(url, json=assign_data, headers=headers).json()
        result = response.get("result")
        
        if result:
            log_action("assign_permissions", "success", {
                "user_id": user_id,
                "group_id": group_id
            })
            return True
        else:
            log_action("assign_permissions", "failed", {
                "user_id": user_id,
                "group_id": group_id,
                "error": response.get("error", "Unknown error")
            })
            return False
    except Exception as e:
        log_action("assign_permissions", "error", {
            "user_id": user_id,
            "group_id": group_id,
            "error": str(e)
        })
        return False

def import_accounts_from_csv(file_path):
    """Fonction principale pour importer les utilisateurs depuis un fichier CSV"""
    log_action("import_accounts_from_csv", "start", {"file": file_path})
    
    # Authentification
    uid = authenticate()
    if not uid:
        print("Échec de l'authentification à Odoo")
        return
    
    # Lecture du fichier CSV
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                print(f"Traitement de l'utilisateur: {row['prenom']} {row['nom']}")
                
                # Création de l'utilisateur
                user_id = create_user(uid, row)
                
                if user_id:
                    # Attribution des permissions
                    group_id = get_group_id(uid, row['droits'])
                    
                    if group_id:
                        success = assign_permissions(uid, user_id, group_id)
                        if success:
                            print(f"Utilisateur {row['prenom']} {row['nom']} créé avec le rôle {row['droits']}")
                        else:
                            print(f"Échec de l'attribution des permissions pour {row['prenom']} {row['nom']}")
                    else:
                        print(f"Groupe {row['droits']} introuvable pour l'utilisateur {row['prenom']} {row['nom']}")
                else:
                    print(f"Échec de la création de l'utilisateur {row['prenom']} {row['nom']}")
    
    except FileNotFoundError:
        error_msg = f"Fichier {file_path} introuvable"
        print(error_msg)
        log_action("import_accounts_from_csv", "error", {"error": error_msg})
    except Exception as e:
        error_msg = f"Erreur lors de la lecture du fichier CSV: {str(e)}"
        print(error_msg)
        log_action("import_accounts_from_csv", "error", {"error": error_msg})
    
    log_action("import_accounts_from_csv", "end", {"file": file_path})

if __name__ == "__main__":
    import_accounts_from_csv("utilisateurs.csv")
