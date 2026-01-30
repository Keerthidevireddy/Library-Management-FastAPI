from fastapi import APIRouter, Depends
from app.models.bulk_models import BulkInventoryUpdate
from app.services.bulk_service import bulk_inventory_update_service
from app.utils.role_guard import require_roles

router = APIRouter(prefix="/bulk", tags=["Bulk"])

@router.patch("/inventory")
def bulk_update(req: BulkInventoryUpdate, _=Depends(require_roles("ADMIN"))):
    bulk_inventory_update_service(req.dict())
    return {"message": "Inventory updated"}
