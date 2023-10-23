import databases
import sqlalchemy

from app.config import app_config

metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(
    app_config.DATABASE_URI,
    connect_args={"check_same_thread": False},  # only needed for sqlite
)

# tables
TrainLine = sqlalchemy.Table(
    "trainlines",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, unique=True),
    sqlalchemy.Column("occupied_at", sqlalchemy.DateTime),
)

Train = sqlalchemy.Table(
    "trains",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, unique=True),
    sqlalchemy.Column("cost", sqlalchemy.Float(precision=2)),
    sqlalchemy.Column("weight", sqlalchemy.Integer),
    sqlalchemy.Column("volume", sqlalchemy.Integer),
    sqlalchemy.Column("line_id", sqlalchemy.ForeignKey("trainlines.id")),
    sqlalchemy.Column("ready_to_book", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("booked_at", sqlalchemy.DateTime),
)

Parcel = sqlalchemy.Table(
    "parcels",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("weight", sqlalchemy.Integer),
    sqlalchemy.Column("volume", sqlalchemy.Integer),
    sqlalchemy.Column("train_id", sqlalchemy.ForeignKey("trains.id")),
)

metadata.create_all(engine)
database = databases.Database(
    app_config.DATABASE_URI, force_rollback=app_config.TESTING
)
