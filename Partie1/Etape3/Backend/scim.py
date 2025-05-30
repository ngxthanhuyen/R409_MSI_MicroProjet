from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import xmlrpc.client

# Configuration Odoo 
ODOO_URL = "http://localhost:8069"
DB = "odoo_db"
USERNAME = "harrylam317@gmail.com"
PASSWORD = "LamHarry2005@_"

# Connexion XML-RPC
common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
uid = common.authenticate(DB, USERNAME, PASSWORD, {})
ud = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

# App FastAPI
app = FastAPI()
router = APIRouter()

# Modèle SCIM simplifié
class SCIMUser(BaseModel):
    schemas: List[str] = Field(default=["urn:ietf:params:scim:schemas:core:2.0:User"])
    userName: str
    name: Optional[dict] = None
    displayName: Optional[str] = None
    password: str
    active: Optional[bool] = True
    groups: Optional[List[dict]] = []

@router.post("/scim/v2/Users", status_code=201)
def create_scim_user(user: SCIMUser):
    try:
        group_ids = []
        for group in user.groups:
            name = group.get("display")
            existing = ud.execute_kw(DB, uid, PASSWORD, 'res.groups', 'search', [[['name', '=', name]]])
            if existing:
                group_ids.append(existing[0])
            else:
                group_id = ud.execute_kw(DB, uid, PASSWORD, 'res.groups', 'create', [{'name': name}])
                group_ids.append(group_id)

        user_id = ud.execute_kw(DB, uid, PASSWORD, 'res.users', 'create', [{
            'name': user.displayName or user.userName,
            'login': user.userName,
            'password': user.password,
            'groups_id': [(6, 0, group_ids)],
            'active': user.active,
        }])

        return {
            "id": user_id,
            "userName": user.userName,
            "displayName": user.displayName,
            "active": user.active,
            "groups": user.groups,
            "schemas": user.schemas
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur SCIM : {str(e)}")

app.include_router(router)
