"""This module contains three time series for generation

"""

INFO = {
    "PV": {
        "p_mwh_per_a": 11_193_780.25,
        "peak_mw": 8038,
        "average_generation": 1277.829,
    },
    "Wind": {
        "p_mwh_per_a": 35_081_507.918,
        "peak_mw": 15_053.42,
        "average_generation": 4004.738,
    },
    "WindOffshore": {
        "p_mwh_per_a": 4_136_477.0,
        "peak_mw": 472.201,
        "average_generation": 1051.33,
    },
}


META = {
    "type": "time-based",
    "models": {
        "PV": {
            "public": True,
            "params": [
                "p_peak_mw",
                "scaling",
                "interpolate",
                "randomize_data",
                "randomize_cos_phi",
            ],
            "attrs": ["p_mw", "q_mvar", "cos_phi"],
        },
        "Wind": {
            "public": True,
            "params": [
                "p_peak_mw",
                "scaling",
                "interpolate",
                "randomize_data",
                "randomize_cos_phi",
            ],
            "attrs": ["p_mw", "q_mvar", "cos_phi"],
        },
        "WindOffshore": {
            "public": True,
            "params": [
                "p_peak_mw",
                "scaling",
                "interpolate",
                "randomize_data",
                "randomize_cos_phi",
            ],
            "attrs": ["p_mw", "q_mvar", "cos_phi"],
        },
    },
    "extra_methods": ["get_data_info"],
}
