from typing import List, Final
from sqlalchemy.orm import Session
from sqlalchemy import exc, func, case, or_
from backend.common import schema
from backend.common import models


def get_bookmark_metadata(
    db: Session,
    user_id: int,
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
        ).filter(models.BookmarkTag.bookmark_id.isn(None)).all()

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


def get_my_bookmarks(
    db: Session,
    user_id: int,
    params: schema.MyBookmarksParams
):
    search: Final[str] = f"%{params.q}%"
    try:
        query = db.query(models.Bookmark)

        if params.unsorted:
            query = query.outerjoin(
                models.BookmarkTag,
                models.Bookmark.id == models.BookmarkTag.bookmark_id,
            ).filter(
                models.BookmarkTag.bookmark_id.is_(None)
            )

        query = query.filter(models.Bookmark.user_id == user_id)

        if params.favorite is not None:
            query = query.filter(models.Bookmark.favorite.is_(params.favorite))
        if params.unread is not None:
            query = query.filter(models.Bookmark.favorite.is_(params.favorite))

        if params.q is not None:
            query = query.filter(
                or_(
                    models.Bookmark.title.like(search),
                    models.Bookmark.description.like(search)
                )
            )

        # order by asc if name or desc if datetime
        if params.sort_by == schema.MyBookmarkSortByEnum.title:
            query = query.order_by(
                getattr(models.Bookmark, params.sort_by.value).asc()
            )
        else:
            query = query.order_by(
                getattr(models.Bookmark, params.sort_by.value).desc()
            )
        bookmarks: List[models.Bookmark] = query.all()

        return schema.DatabaseResult(success=True, data=bookmarks)

    except exc.SQLAlchemyError as e:
        return schema.DatabaseResult(
            success=False,
            exception=e,
            message=str(e)
        )
