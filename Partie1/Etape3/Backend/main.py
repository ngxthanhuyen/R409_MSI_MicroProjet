# main.py
import xmlrpc.client
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Authentification Odoo
URL = "http://localhost:8069"
DB = "odoo_db"
USERNAME = "harrylam317@gmail.com"
PASSWORD = "LamHarry2005@_"

common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
ud = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")
uid = common.authenticate(DB, USERNAME, PASSWORD, {})
if not uid:
	raise Exception("Erreur d'authentification")

# Initialisation FastAPI
app = FastAPI()

# Ajoute ce bloc AVANT les routes
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:3000"],
	allow_credentials=True,
	allow_methods=["*"],  
	allow_headers=["*"],
)

# Modèles Pydantic

class AccountAdditionalIds(BaseModel):
	id: str
	guid: str
	up_id: Optional[str] = None
	display_name: str

class UserCreate(BaseModel):
	login_name: str
	other_ids: AccountAdditionalIds
	password: str
	groups: Optional[List[int]] = []

class UpdateUser(BaseModel):
	name: Optional[str] = None
	login: Optional[str] = None
	password: Optional[str] = None
	groups: Optional[List[int]] = None
class GroupOtherIds(BaseModel):
	guid: str
	display_name: str
	extra_info1: Optional[str] = None
	extra_info2: Optional[str] = None
	extra_info3: Optional[str] = None

class GroupInfo(BaseModel):
	external_name: str
	other_ids: GroupOtherIds

class FullUserCreate(BaseModel):
	login_name: str
	other_ids: AccountAdditionalIds
	password: str
	groups: Optional[List[GroupInfo]] = []

class GroupAssign(BaseModel):
	groups: List[int]

# Endpoints

@app.post("/users")
def create_user(user: UserCreate):
	try:
    	user_id = ud.execute_kw(DB, uid, PASSWORD, 'res.users', 'create', [{
        	'name': user.other_ids.display_name,
        	'login': user.login_name,
        	'password': user.password,
        	'groups_id': [(6, 0, user.groups or [])]
    	}])
    	return {"message": "Utilisateur créé", "user_id": user_id}
	except Exception as e:
    	raise HTTPException(status_code=500, detail=f"Erreur lors de la création de l'utilisateur : {str(e)}")

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UpdateUser):
	try:
    	user_exists = ud.execute_kw(DB, uid, PASSWORD, 'res.users', 'search', [[['id', '=', user_id]]])
    	if not user_exists:
        	raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    	values = {}
    	if user.name:
        	values["name"] = user.name
    	if user.login:
        	values["login"] = user.login
    	if user.password:
        	values["password"] = user.password
    	if user.groups is not None:
        	values["groups_id"] = [(6, 0, user.groups)]

    	if not values:
        	raise HTTPException(status_code=400, detail="Aucune donnée fournie pour la mise à jour")

    	ud.execute_kw(DB, uid, PASSWORD, 'res.users', 'write', [[user_id], values])
    	return {"message": "Utilisateur mis à jour"}
	except HTTPException:
    	raise
	except Exception as e:
    	raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour de l'utilisateur : {str(e)}")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
	try:
    	user_exists = ud.execute_kw(DB, uid, PASSWORD, 'res.users', 'search', [[['id', '=', user_id]]])
    	if not user_exists:
        	raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    	ud.execute_kw(DB, uid, PASSWORD, 'res.users', 'unlink', [[user_id]])
    	return {"message": "Utilisateur supprimé"}
	except HTTPException:
    	raise
	except Exception as e:
    	raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression de l'utilisateur : {str(e)}")

@app.get("/users/{user_id}/groups")
def list_user_groups(user_id: int):
	try:
    	user = ud.execute_kw(DB, uid, PASSWORD, 'res.users', 'read', [[user_id]], {'fields': ['groups_id']})
    	if not user:
        	raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    	return {"user_id": user_id, "groups": user[0].get('groups_id', [])}
	except HTTPException:
    	raise
	except Exception as e:
    	raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des groupes : {str(e)}")

@app.post("/users/{user_id}/roles")
def assign_roles(user_id: int, data: GroupAssign):
	try:
    	user = ud.execute_kw(DB, uid, PASSWORD, 'res.users', 'read', [[user_id]], {'fields': ['groups_id']})
    	if not user:
        	raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    	existing = set(user[0]['groups_id'])
    	new_groups = list(existing.union(set(data.groups)))

    	ud.execute_kw(DB, uid, PASSWORD, 'res.users', 'write', [[user_id], {'groups_id': [(6, 0, new_groups)]}])
    	return {"message": "Groupes attribués", "user_id": user_id, "groups": new_groups}
	except HTTPException:
    	raise
	except Exception as e:
    	raise HTTPException(status_code=500, detail=f"Erreur lors de l'attribution des groupes : {str(e)}")

@app.delete("/users/{user_id}/roles")
def remove_roles(user_id: int, data: GroupAssign):
	try:
    	user = ud.execute_kw(DB, uid, PASSWORD, 'res.users', 'read', [[user_id]], {'fields': ['groups_id']})
    	if not user:
        	raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    	current_groups = set(user[0]['groups_id'])
    	requested_groups = set(data.groups)

    	missing_groups = requested_groups - current_groups
    	if missing_groups:
        	raise HTTPException(
            	status_code=400,
            	detail=f"Les rôles suivants ne sont pas attribués à l'utilisateur : {list(missing_groups)}"
        	)

    	updated_groups = list(current_groups - requested_groups)
    	ud.execute_kw(DB, uid, PASSWORD, 'res.users', 'write', [[user_id], {'groups_id': [(6, 0, updated_groups)]}])
    	return {"message": "Groupes retirés", "user_id": user_id, "groups": updated_groups}
	except HTTPException:
    	raise
	except Exception as e:
    	raise HTTPException(status_code=500, detail=f"Erreur lors du retrait des groupes : {str(e)}")

@app.post("/users/full")
def create_user_with_full_info(user: FullUserCreate):
	try:
    	group_ids = []
    	for group in user.groups or []:
        	existing = ud.execute_kw(DB, uid, PASSWORD, 'res.groups', 'search', [[['name', '=', group.external_name]]])
        	if existing:
            	group_id = existing[0]
        	else:
            	group_id = ud.execute_kw(DB, uid, PASSWORD, 'res.groups', 'create', [{
        	'name': group.external_name,
        	'comment': group.other_ids.extra_info2 if group.other_ids.extra_info2 else ""
    	}])
        	group_ids.append(group_id)

    	user_id = ud.execute_kw(DB, uid, PASSWORD, 'res.users', 'create', [{
        	'name': user.other_ids.display_name,
        	'login': user.login_name,
        	'password': user.password,
        	'groups_id': [(6, 0, group_ids)]
    	}])
    	return {
        	"message": "Utilisateur et groupes créés",
        	"user_id": user_id,
        	"group_ids": group_ids
    	}
	except Exception as e:
    	raise HTTPException(status_code=500, detail=f"Erreur lors de la création complète de l'utilisateur : {str(e)}")