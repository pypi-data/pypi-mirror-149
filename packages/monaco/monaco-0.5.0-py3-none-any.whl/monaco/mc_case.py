# mc_case.py
from __future__ import annotations

from monaco.mc_var import OutVar, InVar
from monaco.mc_val import OutVal, InVal
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
import numpy as np

class Case():
    """
    Object to hold all the data for a single Monte Carlo case.

    Parameters
    ----------
    ncase : int
        The number of this case.
    ismedian : bool
        Whether this represents the median case.
    invars : dict[str, monaco.mc_var.InVar]
        A dict pointing to all of the input variables.
    constvals : dict[str, Any], default: None
        A dict of any constant values common to all cases.
    seed : int, default: np.random.get_state(legacy=False)['state']['key'][0]
        The random seed to pass to the run function for this case. Not used in
        as part of any Monte Carlo sampling.

    Attributes
    ----------
    starttime : datetime.datetime
        Timestamp for when this case started running.
    endtime : datetime.datetime
        Timestamp for when this case stopped running.
    runtime : datetime.timedelta
        Total run duration for this case.
    filepath : pathlib.Path
        The filepath for the case data, if saved to disk.
    runsimid : int
        The id for the particular sim run this case was run for.
    haspreprocessed : bool
        Whether this case has been preprocessed.
    hasrun : bool
        Whether this case has run the run function.
    haspostprocessed : bool
        Whether this case has been postprocessed.
    invals : dict[str, monaco.mc_val.InVal]
        The input values for this partitcular case.
    outvals : dict[str, monaco.mc_val.OutVal]
        The output values for this partitcular case.
    siminput : tuple[Any]
        The preprocessed inputs provided to the run function for this case.
    simrawoutput : tuple[Any]
        The non-postprocessed outputs from the run function for this case.
    """
    def __init__(self,
                 ncase     : int,
                 ismedian  : bool,
                 invars    : dict[str, InVar],
                 constvals : dict[str, Any] = None,
                 seed      : int = np.random.get_state(legacy=False)['state']['key'][0],
                 ):

        self.ncase = ncase
        self.ismedian = ismedian
        self.invars = invars
        if constvals is None:
            constvals = dict()
        self.constvals = constvals
        self.outvars : dict[str, OutVar] = dict()
        self.seed = seed

        self.starttime : datetime = None
        self.endtime   : datetime = None
        self.runtime   : timedelta = None

        self.filepath : Path = None
        self.runsimid : int = None
        self.haspreprocessed  : bool = False
        self.hasrun           : bool = False
        self.haspostprocessed : bool = False

        self.invals  : dict[str, InVal]  = self.getInVals()
        self.outvals : dict[str, OutVal] = dict()

        self.siminput     : tuple[Any] = None
        self.simrawoutput : tuple[Any] = None


    def getInVals(self) -> dict[str, InVal]:
        """
        From all the InVar's, extract the vals for this case.

        Returns
        -------
        vals: dict[str, monaco.mc_val.InVal]
            The InVal's for this case.
        """
        vals = dict()
        for var in self.invars.values():
            val = var.getVal(self.ncase)
            vals[val.name] = val
        return vals


    def getOutVals(self) -> dict[str, OutVal]:
        """
        From all the OutVar's, extract the vals for this case.

        Returns
        -------
        vals: dict[str, monaco.mc_val.OutVal]
            The OutVal's for this case.
        """
        vals = dict()
        for var in self.outvars.values():
            val = var.getVal(self.ncase)
            vals[val.name] = val
        return vals


    def addOutVal(self,
                  name   : str,
                  val    : Any,
                  split  : bool = True,
                  valmap : dict[Any, float] = None
                  ) -> None:
        """
        Generate an OutVal and add it to the dict of outvals.

        Parameters
        ----------
        name : str
            The name of the output value.
        val : Any
            The output value.
        split : bool
            Whether to split the value into its components.
        valmap : dict[Any, float], default: None
            A valmap dict mapping nonnumeric values to numbers.
        """

        self.outvals[name] = OutVal(name=name, ncase=self.ncase, val=val,
                                    valmap=valmap, ismedian=self.ismedian)
        if split:
            self.outvals.update(self.outvals[name].split())
