# Copyright 2022 Cognite AS
import numpy as np
import pandas as pd

from indsl.resample.auto_align import auto_align
from indsl.type_check import check_types


@check_types
def total_head(
    discharge_pressure: pd.Series, suction_pressure: pd.Series, den: pd.Series, align_timesteps: bool = False
) -> pd.Series:
    r"""Total head

    Head is a measure of the potential of a liquid to reach a certain
    height. The head is essentially a unit of pressure. The total head
    is the difference in pressure of the discharge to the suction of
    the pump.he formula for total head :math:`h` [m] given inputs discharge pressure
    :math:`P_{discharge}` [Pa], suction pressure :math:`P_{suction}` [Pa] and liquid density
    :math:`\rho_L\:[\frac{kg}{m^3}]`.

    .. math::
        h = \frac{P_{discharge} - P_{suction}}{9.81\rho_L}

    Args:
        discharge_pressure (pandas.Series): Discharge pressure
            [Pa].
            Discharge pressure of a centrifugal pump.
        suction_pressure (pandas.Series): Suction pressure [Pa].
            Suction pressure of a centrifugal pump.
        den (pandas.Series): Density of fluid
            [:math:`\frac{kg}{m^3}`].
            Density of the fluid.
        align_timesteps (bool): Auto-align.
            Automatically align time stamp  of input time series. Default is False.

    Returns:
        pandas.Series: Total head [m]
            Difference in total discharge head and the total suction head.

    """
    # auto-align
    discharge_pressure, suction_pressure, den = auto_align([discharge_pressure, suction_pressure, den], align_timesteps)

    return (discharge_pressure - suction_pressure) / (den * 9.81)


@check_types
def percent_BEP_flowrate(
    pump_liquid_flowrate: pd.Series, BEP_flowrate: pd.Series, align_timesteps: bool = False
) -> pd.Series:
    r"""BEP from flowrate [%]

    Centrifugal pumps operate optimally at a specific liquid flowrate which is typically called the Best Efficiency Point (BEP).
    This function calculates the flowrate relative to BEP as a percentage.
    i.e. 100% means the current flowrate is at the BEP, 110% means the
    current flowrate is 10% above BEP. The formula for this equation is:

    .. math::
        BEP\:from\:flowrate\:[\%]=\frac{Pump\:liquid\:flowrate}
        {BEP}*100

    Args:
        pump_liquid_flowrate (pandas.Series): Pump liquid flowrate
            :math:`[\frac{m^3}{s}]`.
            The current flowrate of the pump.
        BEP_flowrate (pandas.Series): Best efficiency point [-].
            The best efficiency flowrate point of the pump.
        align_timesteps (bool): Auto-align.
            Automatically align time stamp  of input time series. Default is False.

    Returns:
        pandas.Series:BEP to current flowrate [%].
            Percentage of current flowrate to BEP

    """

    pump_liquid_flowrate, BEP_flowrate = auto_align([pump_liquid_flowrate, BEP_flowrate], align_timesteps)

    return pump_liquid_flowrate / BEP_flowrate * 100


@check_types
def pump_hydraulic_power(
    pump_liquid_flowrate: pd.Series, total_head: pd.Series, den: pd.Series, align_timesteps: bool = False
) -> pd.Series:
    r"""Pump hydraulic power

    Pump hydraulic power [W] is the amount of energy per unit time
    delivered to the liquid. Pump hydraulic power can be calculated
    if the pump liquid flowrate :math:`Q_L\:[\frac{m^3}{s}]`, total head across the pump
    :math:`h` [m], and density of the fluid :math:`\rho_L\:[\frac{kg}{m^3}]`.

    .. math::
        Pump\:hydraulic\:power=9.81Q_L\rho_Lh

    Args:

        pump_liquid_flowrate (pandas.Series): Pump liquid flowrate
            :math:`[\frac{m^3}{s}]`.
            The current flowrate of the pump.
        total_head (pandas.Series): Total head across pump
            [m].
            Difference in pressure between discharge and suction of pump.
        den (pandas.Series): Density of fluid
            :math:`[\frac{kg}{m^3}]`.
            Density of the fluid.
        align_timesteps (bool): Auto-align.
            Automatically align time stamp  of input time series. Default is False.

    Returns:
        pandas.Series: Pump hydraulic power [W].
            Pump hydraulic power of pump.

    """
    # auto-align
    pump_liquid_flowrate, total_head, den = auto_align([pump_liquid_flowrate, total_head, den], align_timesteps)

    return pump_liquid_flowrate * den * 9.81 * total_head


@check_types
def pump_shaft_power(
    pump_hydraulic_power: pd.Series,
    pump_liquid_flowrate: pd.Series,
    eff_parameter_1: pd.Series,
    eff_parameter_2: pd.Series,
    eff_intercept: pd.Series,
    align_timesteps: bool = False,
) -> pd.Series:
    r"""Pump shaft power

    Pump shaft power is the input power delivered by the shaft.
    Pump shaft power can be calculated by dividing the pump hydraulic hp
    by the pump efficiency. Pump efficiency is a function of liquid flowrate :math:`\eta(Q_L)`.
    The pump efficiency curve as a function of liquid flowrate is assumed to be a 2nd order polynomial.
    Therefore the input parameters of the curve are coefficients
    to :math:`x^2` and :math:`x` and the :math:`y` intercept of the curve.

    .. math::
        Pump\:shaft\:power=\frac{Pump\:hydraulic\:power}{\eta(Q_L)}

    Args:

        pump_hydraulic_power (pandas.Series): Pump hydraulic power
            [W].
            Hydraulic power of pump.
        pump_liquid_flowrate (pandas.Series): Pump liquid flowrate
            :math:`[\frac{m^3}{h}]`.
            The current flowrate of the pump.
        eff_parameter_1 (pandas.Series): :math:`x^2` coefficient [-].
            Coefficient of :math:`x^2`.
        eff_parameter_2 (pandas.Series): :math:`x` coefficient [-].
            Coefficient of :math:`x`.
        eff_intercept (pandas.Series): :math:`y`-intercept [-].
            Coefficient of :math:`y`-intercept of curve
        align_timesteps (bool): Auto-align.
            Automatically align time stamp  of input time series. Default is False.

    Returns:
        pandas.Series: Pump shaft power [W]
            Pump shaft power of pump.
    """
    # auto-align
    pump_liquid_flowrate, pump_hydraulic_power, eff_parameter_1, eff_parameter_2, eff_intercept = auto_align(
        [pump_liquid_flowrate, pump_hydraulic_power, eff_parameter_1, eff_parameter_2, eff_intercept], align_timesteps
    )

    p = (eff_parameter_1, eff_parameter_2, eff_intercept)
    eff = np.polyval(p, pump_liquid_flowrate) / 100

    return pump_hydraulic_power / eff


@check_types
def recycle_valve_power_loss(
    Q_valve: pd.Series, total_head: pd.Series, den: pd.Series, align_timestamps: bool = False
) -> pd.Series:
    r"""Pump recycle valve power loss

    This calculation can be used where there is a recirculation line with a recycle valve whose purpose is to maintain a minimum flow through the pump.
    The calculation does not take into account the difference in pump efficiency at different flow rates. This is acceptable because pumps are usally sized to take into account extra flow due to recirculation.

    .. math::
            Power\:loss=9.81Q_{valve}\rho_Lh

    Args:
        Q_valve (pd.Series): Valve flow rate
            :math:`[\frac{m^3}{h}]`.
            Flow rate through recycle valve.
        total_head (pd.Series): Pump total head
            [m].
        den (pd.Series): Density of the fluid
            :math:`[\frac{kg}{m^3}]`.
        align_timestamps (bool, optional): Auto-align.
            Automatically align time stamp  of input time series. Defaults to False.

    Returns:
        pd.Series: Power loss [W].
            Power loss by recirculation though the pump.
    """
    return pump_hydraulic_power(Q_valve, total_head, den, align_timestamps)
