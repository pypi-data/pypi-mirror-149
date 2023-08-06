"""This module contains the meta for the default load profile
simulator.

All profiles are normalized to an annual consumption of 1000 kWh/a.

"""


MODELS = [
    "H0",  # Households
    "G0",  # Commercial (general)
    "G1",  # Commercial (weekday 8-18)
    "G2",  # Commercial (evening)
    "G3",  # Commercial (continuous)
    "G4",  # Commercial (Shop/Barber)
    "G5",  # Commercial (Bakery)
    "G6",  # Commercial (weekend)
    "L0",  # Agriculture (general)
    "L1",  # Acriculture (milk/animal breeding)
    "L2",  # Agriculture (other)
]

CONFIG = {
    "public": True,
    "params": [
        "p_mwh_per_a",
        "interpolate",
        "randomize_data",
        "randomize_cos_phi",
    ],
    "attrs": ["p_mw", "q_mvar", "cos_phi"],
}

META = {
    "type": "time-based",
    "models": {model: CONFIG for model in MODELS},
    "extra_methods": ["get_data_info"],
}
