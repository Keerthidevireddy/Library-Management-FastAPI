from fastapi import APIRouter, Depends
from app.models.role_models import RoleCreateRequest
from app.repositories.role_repo import create_role, list_roles, delete_role
from app.utils.role_guard import require_roles

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("")
def create(req: RoleCreateRequest, _=Depends(require_roles("ADMIN"))):
    create_role(req.dict())
    return {"message": "Role created"}

@router.get("")
def read(_=Depends(require_roles("ADMIN"))):
    return list_roles()

@router.delete("/{name}")
def delete(name: str, _=Depends(require_roles("ADMIN"))):
    delete_role(name)
    return {"message": "Role deleted"}
