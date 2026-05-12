# tests/test_prompts.py

TEST_PROMPTS = [

    {
        "name": "basic_country_role_validation",

        "user_prompt": (
            "Validate AWPer players from Canada for "
            "T Target Last12 and CT Target Last12 "
            "on Tableau Overall dashboard in Preprod."
        ),

        "expected_parsed_output": {
            "dashboard": "Tableau",

            "screen_name": "Overall",

            "environment": "Preprod",

            "entity_filters": {
                "country": "Canada",
                "team": None,
                "role": "AWPer",
                "player_name": None
            },

            "metric_filters": [
                "t_target_last12",
                "ct_target_last12"
            ],

            "validation_config": {
                "comparison_type": "row_level",
                "tolerance": 0.05
            }
        }
    },

    {
        "name": "team_based_validation",

        "user_prompt": (
            "Validate Support players from team NRG "
            "for CT Last12 Delta "
            "on Tableau Overall dashboard in Prod."
        ),

        "expected_parsed_output": {
            "dashboard": "Tableau",

            "screen_name": "Overall",

            "environment": "Prod",

            "entity_filters": {
                "country": None,
                "team": "NRG",
                "role": "Support",
                "player_name": None
            },

            "metric_filters": [
                "ct_last12_delta"
            ],

            "validation_config": {
                "comparison_type": "row_level",
                "tolerance": 0.05
            }
        }
    },

    {
        "name": "player_specific_validation",

        "user_prompt": (
            "Validate player oSee "
            "for T Last12 Delta and CT Last12 Delta "
            "on Tableau Overall dashboard in Preprod."
        ),

        "expected_parsed_output": {
            "dashboard": "Tableau",

            "screen_name": "Overall",

            "environment": "Preprod",

            "entity_filters": {
                "country": None,
                "team": None,
                "role": None,
                "player_name": "oSee"
            },

            "metric_filters": [
                "t_last12_delta",
                "ct_last12_delta"
            ],

            "validation_config": {
                "comparison_type": "row_level",
                "tolerance": 0.05
            }
        }
    },

    {
        "name": "multi_metric_validation",

        "user_prompt": (
            "Validate AWPer metrics including "
            "T Target Last12, CT Target Last12, "
            "T Last12 Delta, and CT Last12 Delta "
            "for United States players "
            "in Tableau Overall dashboard."
        ),

        "expected_parsed_output": {
            "dashboard": "Tableau",

            "screen_name": "Overall",

            "environment": "Preprod",

            "entity_filters": {
                "country": "United States",
                "team": None,
                "role": "AWPer",
                "player_name": None
            },

            "metric_filters": [
                "t_target_last12",
                "ct_target_last12",
                "t_last12_delta",
                "ct_last12_delta"
            ],

            "validation_config": {
                "comparison_type": "row_level",
                "tolerance": 0.05
            }
        }
    },

    {
        "name": "age_hltv_validation",

        "user_prompt": (
            "Validate age and HLTV WR metrics "
            "for players from team Liquid "
            "on Tableau Overall dashboard in QA environment."
        ),

        "expected_parsed_output": {
            "dashboard": "Tableau",

            "screen_name": "Overall",

            "environment": "QA",

            "entity_filters": {
                "country": None,
                "team": "Liquid",
                "role": None,
                "player_name": None
            },

            "metric_filters": [
                "age",
                "hltv_wr"
            ],

            "validation_config": {
                "comparison_type": "row_level",
                "tolerance": 0.05
            }
        }
    },

    {
        "name": "default_values_validation",

        "user_prompt": (
            "Validate Canada AWPer players "
            "for CT Target Last12."
        ),

        "expected_parsed_output": {
            "dashboard": "Tableau",

            "screen_name": "Overall",

            "environment": "Preprod",

            "entity_filters": {
                "country": "Canada",
                "team": None,
                "role": "AWPer",
                "player_name": None
            },

            "metric_filters": [
                "ct_target_last12"
            ],

            "validation_config": {
                "comparison_type": "row_level",
                "tolerance": 0.05
            }
        }
    },

    {
        "name": "country_team_player_validation",

        "user_prompt": (
            "Validate player Twistzz from team FaZe in Canada "
            "for T Target Last12 and CT Target Last12 "
            "on Tableau dashboard in Prod."
        ),

        "expected_parsed_output": {
            "dashboard": "Tableau",

            "screen_name": "Overall",

            "environment": "Prod",

            "entity_filters": {
                "country": "Canada",
                "team": "FaZe",
                "role": None,
                "player_name": "Twistzz"
            },

            "metric_filters": [
                "t_target_last12",
                "ct_target_last12"
            ],

            "validation_config": {
                "comparison_type": "row_level",
                "tolerance": 0.05
            }
        }
    },

    {
        "name": "support_team_validation",

        "user_prompt": (
            "Validate CT Last12 Delta "
            "for Support players from M80 team "
            "on Tableau Overall dashboard in Staging."
        ),

        "expected_parsed_output": {
            "dashboard": "Tableau",

            "screen_name": "Overall",

            "environment": "Staging",

            "entity_filters": {
                "country": None,
                "team": "M80",
                "role": "Support",
                "player_name": None
            },

            "metric_filters": [
                "ct_last12_delta"
            ],

            "validation_config": {
                "comparison_type": "row_level",
                "tolerance": 0.05
            }
        }
    },

    {
        "name": "role_based_hltv_validation",

        "user_prompt": (
            "Validate all Opener players "
            "for HLTV WR and age metrics "
            "on Tableau Overall dashboard in Preprod."
        ),

        "expected_parsed_output": {
            "dashboard": "Tableau",

            "screen_name": "Overall",

            "environment": "Preprod",

            "entity_filters": {
                "country": None,
                "team": None,
                "role": "Opener",
                "player_name": None
            },

            "metric_filters": [
                "hltv_wr",
                "age"
            ],

            "validation_config": {
                "comparison_type": "row_level",
                "tolerance": 0.05
            }
        }
    },

    {
        "name": "enterprise_validation_request",

        "user_prompt": (
            "Validate AWPer players from Canada and team NRG "
            "for T Target Last12, CT Target Last12, "
            "CT Last12 Delta, and T Last12 Delta "
            "on Tableau Overall dashboard in Prod "
            "using row-level comparison."
        ),

        "expected_parsed_output": {
            "dashboard": "Tableau",

            "screen_name": "Overall",

            "environment": "Prod",

            "entity_filters": {
                "country": "Canada",
                "team": "NRG",
                "role": "AWPer",
                "player_name": None
            },

            "metric_filters": [
                "t_target_last12",
                "ct_target_last12",
                "ct_last12_delta",
                "t_last12_delta"
            ],

            "validation_config": {
                "comparison_type": "row_level",
                "tolerance": 0.05
            }
        }
    }
]