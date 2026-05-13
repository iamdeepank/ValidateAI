from .connection import engine, SessionLocal
from .models import Base, PlayerMetric


Base.metadata.create_all(bind=engine)

session = SessionLocal()

rows = [
PlayerMetric(
    environment="Preprod",
    dashboard="Tableau",
    screen_name="Overall",

    country="Canada",
    team="FaZe",
    role="IGL-Opener",

    player_name="Twistzz",

    hltv_wr=30,
    age=36,

    t_target_last12=1.01,
    ct_target_last12=1.13,

    ct_last12_delta=-0.07,
    t_last12_delta=0.08,


    snapshot_date="2024-01-01"
),
PlayerMetric(
    environment="Preprod",
    dashboard="Tableau",
    screen_name="Overall",

    country="Canada",
    team="Liquid",
    role="Support",

    player_name="NAF",

    hltv_wr=30,
    age=36,

    t_target_last12=1.08,
    ct_target_last12=1.09,

    ct_last12_delta=-0.07,
    t_last12_delta=0.08,


    snapshot_date="2024-01-01"
),
PlayerMetric(
    environment="Preprod",
    dashboard="Tableau",
    screen_name="Overall",

    country="Argentina",
    team="9z",
    role="AWPer",

    player_name="meyern",

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

    country="Argentina",
    team="9z",
    role="Opener",

    player_name="luchov",

    hltv_wr=30,
    age=36,

    t_target_last12=1.09,
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
    team="Spirit",
    role="Closer",

    player_name="tN1R",

    hltv_wr=30,
    age=36,

    t_target_last12=1.07,
    ct_target_last12=1.31,

    ct_last12_delta=-0.07,
    t_last12_delta=0.08,


    snapshot_date="2024-01-01"
),
]

session.add_all(rows)
session.commit()
session.close()

print("Seed complete")