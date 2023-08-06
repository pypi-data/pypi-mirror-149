"""This module contains the *mosaik_api* meta definition for pysimmods
models.
"""
from pysimmods.buffer.batterysim import Battery
from pysimmods.consumer.hvacsim import HVAC
from pysimmods.generator.biogassim import BiogasPlant
from pysimmods.generator.chplpgsystemsim import CHPLPGSystem
from pysimmods.generator.dieselsim import DieselGenerator
from pysimmods.generator.pvsystemsim import PVPlantSystem

META = {
    "type": "time-based",
    "models": {
        "Battery": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": [
                "set_percent",
                "p_mw",
                "q_mvar",
                "soc_percent",
                "local_time",
            ],
        },
        "Photovoltaic": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": [
                "set_percent",
                "p_mw",
                "q_mvar",
                "t_air_deg_celsius",
                "t_module_deg_celsius",
                "bh_w_per_m2",
                "dh_w_per_m2",
                "s_module_w_per_m2",
                "local_time",
                "inverter_inductive",
            ],
        },
        "CHP": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": [
                "set_percent",
                "p_mw",
                "q_mvar",
                "day_avg_t_air_deg_celsius",
                "p_th_mw",
                "local_time",
            ],
        },
        "HVAC": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": [
                "set_percent",
                "p_mw",
                "q_mvar",
                "t_air_deg_celsius",
                "local_time",
            ],
        },
        "Biogas": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": [
                "set_percent",
                "p_mw",
                "q_mvar",
                "p_th_mw",
                "local_time",
            ],
        },
        "DieselGenerator": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": ["set_percent", "p_mw", "q_mvar", "local_time"],
        },
    },
}

MODELS = {
    "Photovoltaic": PVPlantSystem,
    "HVAC": HVAC,
    "Battery": Battery,
    "CHP": CHPLPGSystem,
    "DieselGenerator": DieselGenerator,
    "Biogas": BiogasPlant,
}
