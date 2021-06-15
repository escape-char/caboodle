from typing import List, Final
from sqlalchemy import or_, exc
from backend.common import models
from backend.common.constants import ERROR_DATABASE
from backend.common import schema


def get_resources(db, offset=0, limit=100, search=""):
    s: Final[str] = f"%{search}%".lower()
    try:
        query = db.query(models.Resource)
        if search:
            query.filter(
                or_(
                    models.resource.name.like(s),
                    models.Resource.description.like(s),
                )
            )

        resources: List[models.Resource] = query.offset(
            offset
        ).limit(limit).all()

        return schema.DatabaseResult(
            success=True,
            data=resources
        )
    except exc.SQLAlchemyError as e:
        return schema.DatabaseResult(
            success=False,
            exception=e,
            message=ERROR_DATABASE
        )
