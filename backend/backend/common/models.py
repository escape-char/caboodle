from sqlalchemy import (
    Table,
    Boolean,
    Column,
    Integer,
    DateTime,
    ForeignKey,
    SmallInteger,
    String
)
from sqlalchemy.orm import relationship
from .database import Base
from backend.common.utils import (
    utcnow,
    has_expired,
    min_from_now
)
from backend.common.security.utils import gen_password_hash, verify_password
from backend.settings import settings

user_role_assc_table = Table(
    'user_role',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column(
        'created_at',
        DateTime,
        nullable=False,
        default=utcnow
    ),
    Column(
        'modified_at',
        DateTime,
        nullable=False,
        default=utcnow
    )
)

role_assc_table = Table(
    'role_permission',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id')),
    Column(
        'created_at',
        DateTime,
        nullable=False,
        default=utcnow
    ),
    Column(
        'modified_at',
        DateTime,
        nullable=False,
        default=utcnow
    )
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(45), unique=True, index=True)
    password = Column(String(70))
    name = Column(String(70))
    email = Column(String(255))
    dark_theme = Column(Boolean, default=False)
    retries = Column(SmallInteger, default=0)
    locked_until = Column(DateTime, default=None)
    roles = relationship("Role", secondary=user_role_assc_table)
    last_login = Column(DateTime, default=None)
    created_at = Column(DateTime, default=utcnow)
    modified_at = Column(DateTime, default=utcnow)

    def __str__(self) -> str:
        return (
            "<User id='{id}' username='{username}' name='{name}'>"
        ).format(
            id=self.id,
            username=self.username,
            name=self.name
        )

    def asdict(self) -> dict:
        return dict(
            id=self.id,
            username=self.username,
            name=self.name,
            email=self.email,
            dark_theme=self.dark_theme,
            retries=self.retries,
            locked_until=self.locked_until,
            roles=[r.asdict() for r in self.roles],
            last_login=self.last_login,
            created_at=self.created_at,
            modified_at=self.modified_at
        )

    def set_password(self, password):
        self.password = gen_password_hash(password)

    def verify_password(self, password) -> bool:
        return verify_password(password, self.password)

    def has_max_retries(self):
        return self.retries >= settings.auth_retries

    def lock_account(self):
        self.locked_until = min_from_now(settings.auth_lockout_exp)

    def unlock_account(self):
        self.locked_until = None
        self.retries = 0

    def is_locked(self) -> bool:
        return bool(self.locked_until)

    def set_last_login(self):
        self.last_login = utcnow()

    def has_locked_expired(self) -> bool:
        return has_expired(self.locked)


class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), unique=True, index=True, nullable=False)
    description = Column(String(150), nullable=False)
    permissions = relationship("Permission")
    roles = relationship("Role")
    created_at = Column(DateTime, default=utcnow)
    modified_at = Column(DateTime, default=utcnow)

    def __str__(self) -> str:
        return (
            "<Resource id='{id}' name='{name}' description='{description}'"
        ).format(
            id=self.id,
            name=self.name,
            description=self.description
        )

    def asdict(self) -> dict:
        return dict(
            id=self.id,
            name=self.name,
            description=self.description,
            permissions=[p.asdict() for p in self.permissions],
            created_at=self.created_at,
            modified_at=self.modified_at
        )


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), unique=True, index=True, nullable=False)
    description = Column(String(150), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'))
    created_at = Column(DateTime, default=utcnow)
    modified_at = Column(DateTime, default=utcnow)

    def __str__(self) -> str:
        return (
            "<Permission id='{id}' name='{name}'"
            "description='{descr}' resource_id='{r_id}'>"
        ).format(
            id=self.id,
            name=self.name,
            descr=self.description,
            r_id=self.resource_id
        )

    def asdict(self) -> dict:
        return dict(
            id=self.id,
            name=self.name,
            description=self.description,
            resource_id=self.resource_id,
            created_at=self.created_at,
            modified_at=self.modified_at
        )


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), unique=True, index=True, nullable=False)
    description = Column(String(150), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'))
    permissions = relationship("Permission", secondary=role_assc_table)
    created_at = Column(DateTime, default=utcnow)
    modified_at = Column(DateTime, default=utcnow)

    def __str__(self) -> str:
        return (
            "<Role id='{id}' name='{name}'"
            "description='{descr}' resource_id='{r_id}'>"
        ).format(
            id=self.id,
            name=self.name,
            descr=self.description,
            r_id=self.resource_id
        )

    def asdict(self) -> dict:
        return dict(
            id=self.id,
            name=self.name,
            description=self.name,
            resource_id=self.resource_id,
            permissions=[p.asdict() for p in self.permissions],
            created_at=self.created_at,
            modified_at=self.modified_at
        )
