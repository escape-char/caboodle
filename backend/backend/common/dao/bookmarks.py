from sqlalchemy.orm import Session
from sqlalchemy import exc, func, case
from backend.common import schema
from backend.common import models


def get_bookmark_metadata(
    db: Session,
    user_id: int
) -> schema.DatabaseResult:

    try:
        bookmark_meta = db.query(
            func.count(models.Bookmark.id),
            func.sum(case([(models.Bookmark.favorite, 1)], else_=0)),
            func.sum(case([(models.Bookmark.to_read, 1)], else_=0))
        ).filter(
            models.Bookmark.user_id == user_id
        ).all()

        unsorted_meta = db.query(
            func.count(models.Bookmark.id)
        ).outerjoin(
            models.BookmarkTag,
            models.Bookmark.id == models.BookmarkTag.bookmark_id,
        ).filter(models.BookmarkTag.bookmark_id == None).all()

        meta: schema.MyBookmarkMeta = schema.MyBookmarkMeta(
            bookmarks=bookmark_meta[0][0],
            favorites=bookmark_meta[0][1],
            unread=bookmark_meta[0][2],
            unsorted=unsorted_meta[0][0]
        )

        return schema.DatabaseResult(
            success=True,
            data=meta
        )
    except exc.SQLAlchemyError as e:
        return schema.DatabaseResult(
            success=False,
            exception=e,
            message=str(e)
        )
