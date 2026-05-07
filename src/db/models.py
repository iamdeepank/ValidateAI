from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy import Text
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class PlayerMetric(Base):
    __tablename__ = "player_metrics"

    id: Mapped[int] = mapped_column(primary_key=True)

    environment: Mapped[str]

    dashboard: Mapped[str]
    screen_name: Mapped[str]

    country: Mapped[str]
    team: Mapped[str]
    role: Mapped[str]

    player_name: Mapped[str]

    hltv_wr: Mapped[float]
    age: Mapped[int]

    t_target_last12: Mapped[float]
    ct_target_last12: Mapped[float]

    ct_last12_delta: Mapped[float]
    t_last12_delta: Mapped[float]

    snapshot_date: Mapped[str]

    created_at: Mapped[str] = mapped_column(
        default=lambda: datetime.utcnow().isoformat()
    )
