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
