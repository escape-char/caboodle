from typing import List, Final
from sqlalchemy import or_, exc
from backend.common import models
from backend.common.constants import ERROR_DATABASE
from backend.common import schema


def get_resources(db, offset=0, limit=100, search=""):
    s: Final[str] = f"%{search}%".lower()
    try:
        if search:
            resources: List[models.Resource] = db.query(
                models.Resource
            ).filter(
                or_(
                    models.resource.name.like(s),
                    models.Resource.description.like(s),
                )
            ).offset(offset).limit(limit).all()

            return schema.DatabaseResult(
                success=True,
                data=resources
            )
        else:
            resources = db.query(
                models.Resource
            ).offset(offset).limit(limit).all()

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
