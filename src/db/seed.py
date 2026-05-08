from .connection import engine, SessionLocal
from .models import Base, PlayerMetric


Base.metadata.create_all(bind=engine)

session = SessionLocal()

rows = [
PlayerMetric(
    environment="Preprod",
    dashboard="Tableau",
    screen_name="Overall",

    country="Belarus",
    team="Spirit",
    role="Closer",

    player_name="tN1r",

    hltv_wr=30,
    age=36,

    t_target_last12=1.06,
    ct_target_last12=1.11,

    ct_last12_delta=-0.07,
    t_last12_delta=0.08,


    snapshot_date="2024-01-01"
),

PlayerMetric(
    environment="Preprod",
    dashboard="Tableau",
    screen_name="Overall",

    country="Belarus",
    team="BIG",
    role="AWPer",

    player_name="gr1ks",

    hltv_wr=30,
    age=36,

    t_target_last12=1.07,
    ct_target_last12=1.31,

    ct_last12_delta=-0.07,
    t_last12_delta=0.08,


    snapshot_date="2024-01-01"
)
# PlayerMetric(
#     environment="staging",
#     dashboard="Tableau",
#     screen_name="Overall",
#
#     country="Argentina",
#     team="NRG",
#     role="AWPer",
#
#     player_name="oSee",
#
#     hltv_wr=30,
#     age=16,
#
#     t_target_last12=1.04,
#     ct_target_last12=1.11,
#
#     ct_last12_delta=-0.07,
#     t_last12_delta=0.08,
#
#     snapshot_date="2024-01-01"
# )
]

session.add_all(rows)
session.commit()
session.close()

print("Seed complete")