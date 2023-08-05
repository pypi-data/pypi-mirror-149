""" This module contains the GridOperator simulator."""
from typing import Any, Dict, List
import mosaik_api
from midas.util.dict_util import update

from . import LOG
from .meta import META
from .model.coordinator import Coordinator as GOA


class GridOperatorSimulator(mosaik_api.Simulator):
    """The GridOperator simulator."""

    def __init__(self):
        super().__init__(META)
        self.sid: str = ""
        self.step_size: int = 0
        self.models: Dict[str, GOA] = {}
        self.cache: dict = {}

    def init(self, sid: str, **sim_params) -> Dict[str, Any]:
        """Called exactly ones after the simulator has been started.

        Parameters
        ----------
        sid : str
            Simulator ID for this simulator.
        step_size : int, optional
            Step size for this simulator. Defaults to 900.

        Returns
        -------
        dict
            The meta dict (set by *mosaik_api.Simulator*).
        """
        self.sid = sid
        if "step_size" not in sim_params:
            LOG.debug(
                "Param *step_size* not provided. "
                "Using default step size of 900."
            )
        self.step_size = sim_params.get("step_size", 900)
        return self.meta

    def create(self, num: int, model: str, **model_params):
        """Initialize the simulation model instance (entity).

        Parameters
        ----------
        num : int
            The number of models to create.
        model : str
            The name of the models to create. Must be present inside
            the simulator's meta.

        Returns
        -------
        list
            A list with information on the created entity.
        """

        assert num == 1, "Only one operator at a time"

        eid = f"GOA_{len(self.models)}"
        self.models[eid] = GOA(params=model_params["params"])

        return [{"eid": eid, "type": "GOA"}]

    def step(
        self,
        time: int,
        inputs: Dict[str, Dict[str, Dict[str, Any]]],
        max_advance: int = 0,
    ):
        """Perform a simulation step.

        Parameters
        ----------
        time : int
            The current simulation step (by convention in seconds since
            simulation start.
        inputs : dict
            A *dict* containing inputs for entities of this simulator.

        Returns
        -------
        int
            The next step this simulator wants to be stepped.

        """
        LOG.debug("At step %d received inputs %s", time, inputs)

        for eid, attrs in inputs.items():
            for attr, src_ids in attrs.items():
                for src_id, val in src_ids.items():
                    if val is None:
                        continue
                    if attr == "inbox":
                        for msg in val:
                            self.models[eid].receive(msg)
                            LOG.debug("GOA %s received message %s", eid, msg)
                    else:
                        msg = {
                            "from": src_id,
                            "to": f"{self.sid}.{eid}",
                            "topic": attr,
                            "msg": val,
                        }
                        self.models[eid].receive(msg)
                        LOG.debug("GOA %s received message %s", eid, msg)

        for eid, goa in self.models.items():
            goa.step()

        return time + self.step_size

    def get_data(
        self, outputs: Dict[str, List[Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """Return the requested output (if feasible).

        Parameters
        ----------
        outputs : dict
            A *dict* containing requested outputs of each entity.

        Returns
        -------
        dict
            A *dict* containing the values of the requested outputs.

        """

        data = {}
        grid_json = {}

        for eid, attrs in outputs.items():
            data[eid] = {}
            goa = self.models[eid]

            for attr in attrs:
                if attr == "outbox":
                    outs = dict()
                    while not goa.outbox.empty():
                        msg = goa.outbox.get()
                        if msg["to"] not in outs:
                            outs[msg["to"]] = dict()
                        outs[msg["to"]][msg["topic"]] = msg["msg"]
                    data[eid][attr] = outs
                elif attr == "grid":
                    grid_json.setdefault(eid, {})["grid"] = goa.grid
                else:
                    # Currently, only health and error can be requested
                    data[eid][attr] = getattr(goa, attr)

        LOG.debug("Gathered outputs %s", data)
        update(data, grid_json)

        return data


if __name__ == "__main__":
    mosaik_api.start_simulation(GridOperatorSimulator())
