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

