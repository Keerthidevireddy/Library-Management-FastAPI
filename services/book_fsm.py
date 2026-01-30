from app.exceptions.book_exceptions import InvalidStatusChange

FSM_RULES = {
    "DRAFT": ["REQUESTED_FOR_APPROVAL", "ARCHIVED"],
    "REQUESTED_FOR_APPROVAL": ["APPROVED", "REJECTED"],
    "REJECTED": ["DRAFT"],
    "APPROVED": ["PUBLISHED"],
    "PUBLISHED": ["DEPRECATED"],
}


def validate_fsm_transition(current_status: str, target_status: str):
    allowed = FSM_RULES.get(current_status, [])
    if target_status not in allowed:
        raise InvalidStatusChange(
            f"Invalid transition from {current_status} to {target_status}"
        )
