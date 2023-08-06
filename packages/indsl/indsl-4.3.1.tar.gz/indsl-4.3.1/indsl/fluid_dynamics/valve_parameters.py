# Copyright 2022 Cognite AS
import numpy as np
import pandas as pd

from indsl.resample.auto_align import auto_align
from indsl.type_check import check_types
from indsl.validations import UserValueError


@check_types
def flow_through_valve(
    inlet_P: pd.Series,
    outlet_P: pd.Series,
    valve_opening: pd.Series,
    SG: float,
    type: str,
    min_opening: float,
    max_opening: float,
    min_Cv: float,
    max_Cv: float,
    align_timestamps: bool = False,
) -> pd.Series:
    r"""Valve volumetric flow rate

    This calculation can be used when there is no flow meter, but the pressure difference over the valve is known.
    The calculated flow rate is only exactly applicable for ideal fluids (incompressible and with zero viscosity).
    The availible valve characteristics are

    * Linear: :math:`Cv = ax + b`.
    * Equal percentage: :math:`Cv = ae^x + b`.

    The formula for the flow rate is

    .. math:: Q = Cv \sqrt{\frac{p_{in} - p_{out}}{SG}}.

    Args:
        inlet_P (pd.Series): Pressure at
            inlet [bar].
        outlet_P (pd.Series): Pressure at outlet
            [bar].
        valve_opening (pd.Series): Valve opening [-].
            Note that this is the proportional and not percentage valve opening.
        SG (float): Specific gravity of
            fluid [-].
        type (str): Valve characteristic
            Valve characteristic, either "linear" or "EQ" (equal percentage)
        min_opening (float): Min opening [-].
            Valve opening at minimum flow.
            Note that the flow coefficient should be expressed in imperial units.
        max_opening (float): Max opening [-].
            Valve opening at maximum flow.
            Note that the flow coefficient should be expressed in imperial units.
        min_Cv (float): Min Cv
            :math:`[(-, \frac{gpm}{psi^{0.5}})]`.
            Valve Cv at minimum flow.
            Note that the flow coefficient should be expressed in imperial units.
        max_Cv (float): Max Cv
            :math:`[(-, \frac{gpm}{psi^{0.5}})]`.
            Valve Cv at maximum flow.
            Note that the flow coefficient should be expressed in imperial units.
        align_timestamps (bool): Auto-align.
            Automatically align time stamp  of input time series. Default is False.

    Raises:
        ValueError: If the valve characteristic is not recognized.

    Returns:
        pd.Series: Valve flow rate [m3/h].
    """
    if SG < 0:
        raise UserValueError("Specific gravity cannot be negative.")

    inlet_P, outlet_P, valve_opening = auto_align([inlet_P, outlet_P, valve_opening], align_timestamps)

    if type == "linear":
        Cv = (max_Cv - min_Cv) / (max_opening - min_opening) * valve_opening + (
            min_Cv * max_opening - min_opening * max_Cv
        ) / (max_opening - min_opening)
    elif type == "EQ":
        exp_coef = (max_Cv - min_Cv) / (np.exp(max_opening) - np.exp(min_opening))
        intercept = (min_Cv * np.exp(max_opening) - np.exp(min_opening) * max_Cv) / (
            np.exp(max_opening) - np.exp(min_opening)
        )
        Cv = exp_coef * np.exp(valve_opening) + intercept
    else:
        raise UserValueError("Only 'linear' or 'EQ' valve characteristics are supported.")

    return 0.865 * Cv * np.sqrt((inlet_P - outlet_P) / SG)
