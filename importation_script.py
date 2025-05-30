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

