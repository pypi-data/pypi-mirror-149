from __future__ import annotations

import abc
from datetime import timedelta
from typing import TYPE_CHECKING, Hashable, Mapping, Sequence

import numpy as np
import pandas as pd
from pyomo import environ as pyo
from pyomo.core import base as pyo_base

from eta_utility.eta_x.envs import BaseEnv
from eta_utility.eta_x.envs.base_env import log

if TYPE_CHECKING:
    from typing import Any, Callable, SupportsFloat

    from pyomo.opt import SolverResults

    from eta_utility.type_hints import Path


class BaseEnvMPC(BaseEnv, abc.ABC):
    """Base class for MPC models"""

    def __init__(
        self,
        env_id: int,
        run_name: str,
        general_settings: dict[str, Any],
        path_settings: dict[str, Path],
        env_settings: dict[str, Any],
        verbose: int,
        callback: Callable = None,
    ) -> None:
        self.req_env_settings = set(self.req_env_settings)
        self.req_env_settings.update(("model_parameters",))  # noqa
        self.req_env_config.update(
            {
                "discretize_state_space": False,
                "discretize_action_space": False,
                "normalize_state_space": False,
                "normalize_reward": False,
                "reward_shaping": False,
            }
        )
        super().__init__(
            env_id,
            run_name,
            general_settings,
            path_settings,
            env_settings,
            verbose,
            callback,
        )

        # Check configuration for MILP compatibility
        errors = False
        if self.settings["prediction_scope"] % self.settings["sampling_time"] != 0:
            log.error(
                "The sampling_time must fit evenly into the prediction_scope "
                "(prediction_scope % sampling_time must equal 0."
            )
            errors = True

        if errors:
            raise ValueError(
                "Some configuration parameters do not conform to the MPC environment " "requirements (see log)."
            )

        # Make some more settings easily accessible
        #: Total duration of one prediction/optimization run when used with the MPC agent.
        #:   This is automatically set to the value of episode_duration if it is not supplied
        #:   separately
        self.prediction_scope: int
        if "prediction_scope" not in self.settings:
            log.info("prediction_scope parameter is not present. Setting prediction_scope to episode_duration.")
        self.prediction_scope = int(self.settings.setdefault("prediction_scope", self.episode_duration))
        self.n_prediction_steps: int  #: Number of steps in the prediction (prediction_scope/sampling_time)
        self.n_prediction_steps = self.settings["prediction_scope"] // self.sampling_time
        #: Duration of the scenario for each episode (for total time imported from csv)
        self.scenario_duration: int = self.episode_duration + self.prediction_scope

        self.model_parameters: dict  #: Configuration for the MILP model parameters
        self.model_parameters = self.env_settings["model_parameters"]

        # Set additional attributes with model specific information.
        self._concrete_model: pyo.ConcreteModel | None = None  #: Concrete pyomo model as initialized by _model.

        #: Name of the "time" variable/set in the model (i.e. "T"). This is if the pyomo sets must be re-indexed when
        #:   updating the model between time steps. If this is None, it is assumed that no reindexing of the timeseries
        #:   data is required during updates - this is the default.
        self.time_var: str | None = None

        #: Updating indexed model parameters can be achieved either by updating only the first value of the actual
        #:   parameter itself or by having a separate handover parameter that is used for specifying only the first
        #:   value. The separate handover parameter can be denoted with an appended string. For example, if the actual
        #:   parameter is x.ON then the handover parameter could be x.ON_first. To use x.ON_first for updates, set the
        #:   nonindex_update_append_string to "_first". If the attribute is set to None, the first value of the
        #:   actual parameter (x.ON) would be updated instead.
        self.nonindex_update_append_string: str | None = None

        #: Some models may not use the actual time increment (sampling_time). Instead they would translate into model
        #:   time increments (each sampling time increment equals a single model time step). This means that indices
        #:   of the model components simply count 1,2,3,... instead of 0, sampling_time, 2*sampling_time, ...
        #:   Set this to true, if model time increments (1, 2, 3, ...) are used. Otherwise sampling_time will be used
        #:   as the time increment. Note: This is only relevant for the first model time increment, later increments
        #:   may differ.
        self._use_model_time_increments: bool = False

    @property
    def model(self) -> tuple[pyo.ConcreteModel, list]:
        """The model property is a tuple of the concrete model and the order of the action space. This is used
        such that the MPC algorithm can re-sort the action output. This sorting cannot be conveyed differently through
        pyomo.

        :return: tuple of the concrete model and the order of the action space
        """
        if self._concrete_model is None:
            self._concrete_model = self._model()

        if self.names["actions"] is None:
            self.names["actions"] = [
                com.name
                for com in self._concrete_model.component_objects(pyo.Var)
                if not isinstance(com, pyo.SimpleVar)
            ]

        return self._concrete_model, self.names["actions"]

    @model.setter
    def model(self, value: pyo.ConcreteModel) -> None:
        """The model attribute setter should be used for returning the solved model.

        :param value:
        :return:
        """
        if not isinstance(value, pyo.ConcreteModel):
            raise TypeError("The model attribute can only be set with a pyomo concrete model.")
        self._concrete_model = value

    @abc.abstractmethod
    def _model(self) -> pyo.AbstractModel:
        """Create the abstract pyomo model. This is where the pyomo model description should be placed.

        :return: Abstract pyomo model
        """
        raise NotImplementedError("The abstract MPC environment does not implement a model.")

    def step(self, action: np.ndarray) -> tuple[np.ndarray, np.floating | SupportsFloat, bool, str | dict]:
        """Perfom one time step and return its results. This is called for every event or for every time step during
        the simulation/optimization run. It should utilize the actions as supplied by the agent to determine
        the new state of the environment. The method must return a four-tuple of observations, rewards, dones, info.

        This also updates self.state and self.state_log to store current state information.

        TODO: Add something to handle actions, currently they are just ignored (MPC agent does not need to use actions)

        :param np.ndarray action: Actions to perform in the environment.
        :return: The return value represents the state of the environment after the step was performed.

            * observations: A numpy array with new observation values as defined by the observation space.
              Observations is a np.array() (numpy array) with floating point or integer values.
            * reward: The value of the reward function. This is just one floating point value.
            * done: Boolean value specifying whether an episode has been completed. If this is set to true,
              the reset function will automatically be called by the agent or by eta_i.
            * info: Provide some additional info about the state of the environment. The contents of this may
              be used for logging purposes in the future but typically do not currently serve a purpose.
        """
        if not self.action_space.contains(action):
            raise RuntimeError(f"Action {action} ({type(action)}) is invalid. Not in action space.")

        observations = self.update()

        # update and log current state
        self.state = {}
        for idx, act in enumerate(self.names["actions"]):
            self.state[act] = action[idx]
        for idx, obs in enumerate(self.names["observations"]):
            self.state[obs] = observations[idx]
        self.state_log.append(self.state)

        reward = pyo.value(list(self._concrete_model.component_objects(pyo.Objective))[0])
        done = True if self.n_steps >= self.n_episode_steps else False

        info = {}
        if done:
            info["terminal_observation"] = observations
        return observations, reward, done, info

    def update(self, observations: Sequence[Sequence[float | int]] | None = None) -> np.ndarray:
        """Update the optimization model with observations from another environment.

        :param observations: Observations from another environment
        :return: Full array of current observations
        """
        # update shift counter for rolling MPC approach
        self.n_steps += 1

        # The timeseries data must be updated for the next time step. The index depends on whether time itself is being
        # shifted. If time is being shifted, the respective variable should be set as "time_var".
        step = 1 if self._use_model_time_increments else self.sampling_time
        duration = (
            self.prediction_scope // self.sampling_time + 1
            if self._use_model_time_increments
            else self.prediction_scope
        )

        if self.time_var is not None:
            index = range(self.n_steps * step, duration + (self.n_steps * step), step)
            ts_current = self.pyo_convert_timeseries(
                self.timeseries.iloc[self.n_steps : self.n_prediction_steps + self.n_steps + 1],
                index=tuple(index),
                _add_wrapping_none=False,
            )
            ts_current[self.time_var] = list(index)
            log.debug(
                "Updated time_var ({}) with the set from {} to {} and steps (sampling time) {}.".format(
                    self.time_var, index[0], index[1], self.sampling_time
                )
            )
        else:
            index = range(0, duration, step)
            ts_current = self.pyo_convert_timeseries(
                self.timeseries.iloc[self.n_steps : self.n_prediction_steps + self.n_steps + 1],
                index=tuple(index),
                _add_wrapping_none=False,
            )

        # Log current time shift
        if self.n_steps + self.n_prediction_steps + 1 < len(self.timeseries.index):
            log.info(
                "Current optimization time shift: {} of {} | Current scope: {} to {}".format(
                    self.n_steps,
                    self.n_episode_steps,
                    self.timeseries.index[self.n_steps],
                    self.timeseries.index[self.n_steps + self.n_prediction_steps + 1],
                )
            )
        else:
            log.info(
                "Current optimization time shift: {} of {}. Last optimization step reached.".format(
                    self.n_steps, self.n_episode_steps
                )
            )

        updated_params = ts_current
        return_obs = []  # Array for all current observations
        for var_name in self.names["observations"]:
            settings = self.state_config.loc[var_name]
            value = None

            # Read values from external environment (for example simulation)
            if observations is not None and settings["is_ext_output"] is True:
                value = round(
                    (observations[0][settings["ext_id"]] + settings["ext_scale_add"]) * settings["ext_scale_mult"],
                    5,
                )
                return_obs.append(value)
            else:
                # Read additional values from the mathematical model
                for component in self._concrete_model.component_objects():
                    if component.name == var_name:
                        # Get value for the component from specified index
                        value = round(pyo.value(component[list(component.keys())[int(settings["index"])]]), 5)
                        return_obs.append(value)
                        break
                else:
                    log.error(f"Specified observation value {var_name} could not be found")
            updated_params[var_name] = value

            log.debug(f"Observed value {var_name}: {value}")

        self.pyo_update_params(updated_params, self.nonindex_update_append_string)
        return np.array(return_obs)

    def solve_failed(self, model: pyo.ConcreteModel, result: SolverResults) -> None:
        """This method will try to render the result in case the model could not be solved. It should automatically
        be called by the agent.

        :param model: Current model
        :param result: Result of the last solution attempt
        :return:
        """
        self.model = model
        try:
            self.render()
        except Exception as e:
            log.error(f"Rendering partial results failed: {str(e)}")
        self.reset()

    def reset(self) -> np.ndarray:
        """Reset the model and return initial observations. This also calls the callback, increments the episode
        counter, resets the episode steps and appends the state_log to the longtime log.

        If you want to extend this function, write your own code and call super().reset() afterwards to return
        fresh observations. This allows you to adjust timeseries for example. If you need to manipulate the state
        before initializing or if you want to adjust the initialization itself, overwrite the function entirely.

        :return: Initial observation
        """
        if self.n_steps > 0:
            if self.callback is not None:
                self.callback(self)

            # Store some logging data
            self.n_episodes += 1
            self.state_log_longtime.append(self.state_log)
            self.n_steps_longtime += self.n_steps

            # Reset episode variables
            self.n_steps = 0
            self.state_log = []
            self._concrete_model = self._model()

        # Initialize state with the initial observation
        self.state = {}
        observations = []
        for var_name in self.names["observations"]:
            for component in self._concrete_model.component_objects():
                if component.name == var_name:
                    if hasattr(component, "__getitem__") and (
                        (hasattr(component[0], "stale") and component[0].stale)
                        or (hasattr(component[0], "active") and not component[0].active)
                    ):
                        obs_val = 0
                    elif not hasattr(component, "__getitem__"):
                        obs_val = round(pyo.value(component), 5)
                    else:
                        obs_val = round(pyo.value(component[0]), 5)
                    observations.append(obs_val)
                    break
            self.state[var_name] = observations[-1]

        # Initialize state with zero actions
        for act in self.names["actions"]:
            self.state[act] = 0
        self.state_log.append(self.state)

        return np.array(observations)

    def close(self) -> None:
        """Close the environment. This should always be called when an entire run is finished. It should be used to
        close any resources (i.e. simulation models) used by the environment.

        Default behaviour for the MPC environment is to do nothing.

        :return:
        """
        pass

    def pyo_component_params(
        self,
        component_name: None | str,
        ts: Mapping[Any, Any] | None = None,
        index: Sequence | pyo.Set | None = None,
    ) -> dict[None, dict[str, Any]]:
        """Retrieve paramters for the named component and convert the parameters into the pyomo dict-format.
        If required, timeseries can be added to the parameters and timeseries may be reindexed. The
        pyo_convert_timeseries function is used for timeseries handling.

        .. see also:: pyo_convert_timeseries

        :param component_name: Name of the component
        :param ts: Timeseries for the component
        :param index: New index for timeseries data. If this is supplied, all timeseries will be copied and
                              reindexed.
        :return: Pyomo parameter dictionary
        """
        if component_name is None:
            params = self.model_parameters
        elif component_name in self.model_parameters:
            params = self.model_parameters[component_name]
        else:
            params = {}
            log.warning(f"No parameters specified for requested component {component_name}")

        out = {
            param: {None: float(value) if isinstance(value, Hashable) and value in {"inf", "-inf"} else value}
            for param, value in params.items()
        }

        # If component name was specified only look for relevant time series
        if ts is not None:
            out.update(self.pyo_convert_timeseries(ts, index, component_name, _add_wrapping_none=False))

        return {None: out}

    @staticmethod
    def pyo_convert_timeseries(
        ts: pd.DataFrame | pd.Series | dict[str, dict] | Sequence,
        index: pd.Index | Sequence | pyo.Set | None = None,
        component_name: str | None = None,
        *,
        _add_wrapping_none: bool = True,
    ) -> dict[None, dict[str, Any]] | dict[str, Any]:
        """Convert a time series data into a pyomo format. Data will be reindexed if a new index is provided.

        :param ts: Timeseries to convert
        :param index: New index for timeseries data. If this is supplied, all timeseries will be copied and
                              reindexed.
        :param component_name: Name of a specific component that the timeseries is used for. This limits which
                                   timeseries are returned.
        :param _add_wrapping_none: default is True
        :return: pyomo parameter dictionary
        """
        output = {}
        if index is not None:
            index = list(index) if type(index) is not list else index

        # If part of the timeseries was converted before, make sure that everything is on the same level again.
        if None in ts and isinstance(ts[None], Mapping):
            ts = ts.copy()
            ts.update(ts[None])
            del ts[None]

        def convert_index(_ts: pd.Series, _index: Sequence[int]) -> dict[int, Any]:
            """Take the timeseries and change the index to correspond to _index.

            :param _ts: Original timeseries object (with or without index does not matter)
            :param _index: New index
            :return: New timeseries dictionary with the converted index.
            """
            values = None
            if isinstance(_ts, pd.Series):
                values = _ts.values
            elif isinstance(_ts, Mapping):
                values = ts.values()  # noqa
            elif isinstance(_ts, Sequence):
                values = _ts

            if _index is not None and values is not None:
                _ts = dict(zip(_index, values))
            elif _index is not None and values is None:
                raise ValueError("Unsupported timeseries type for index conversion.")

            return _ts

        if isinstance(ts, pd.DataFrame) or isinstance(ts, Mapping):
            for key, t in ts.items():
                # Determine whether the timeseries should be returned, based on the timeseries name and the requested
                #  component name.
                if component_name is not None and "." in key and component_name in key.split("."):
                    key = key.split(".")[-1]
                elif component_name is not None and "." in key and component_name not in key.split("."):
                    continue

                # Simple values do not need their index converted...
                if not hasattr(t, "__len__") and np.isreal(t):
                    output[key] = {None: t}
                else:
                    output[key] = convert_index(t, index)

        elif isinstance(ts, pd.Series):
            # Determine whether the timeseries should be returned, based on the timeseries name and the requested
            #  component name.
            if (
                component_name is not None
                and type(ts.name) is str
                and "." in ts.name
                and component_name in ts.name.split(".")
            ):  # noqa
                output[ts.name.split(".")[-1]] = convert_index(ts, index)  # noqa
            elif component_name is None or "." not in ts.name:
                output[ts.name] = convert_index(ts, index)

        else:
            output[None] = convert_index(ts, index)

        return {None: output} if _add_wrapping_none else output

    def pyo_update_params(
        self,
        updated_params: Mapping[str, Any],
        nonindex_param_append_string: str | None = None,
    ) -> pyo.ConcreteModel:
        """Updates model parameters and indexed parameters of a pyomo instance with values given in a dictionary.
        It assumes that the dictionary supplied in updated_params has the correct pyomo format.

        :param updated_params: Dictionary with the updated values
        :param nonindex_param_append_string: String to be appended to values that are not indexed. This can
                                                  be used if indexed parameters need to be set with values that do
                                                  not have an index.
        :return: Updated model instance
        """
        # append string to non indexed values that are used to set indexed parameters.
        if nonindex_param_append_string is not None:
            original_indices = set(updated_params.keys()).copy()
            for param in original_indices:
                if not isinstance(updated_params[param], Mapping):
                    updated_params[str(param) + nonindex_param_append_string] = updated_params[param]
                    del updated_params[param]

        for parameter in self._concrete_model.component_objects():
            if str(parameter) in updated_params.keys():
                parameter_name = str(parameter)
            else:
                parameter_name = str(parameter).split(".")[
                    -1
                ]  # last entry is the parameter name for abstract models which are instanced
            if parameter_name in updated_params.keys():
                if isinstance(parameter, pyo_base.param.SimpleParam) or isinstance(parameter, pyo_base.var.SimpleVar):
                    # update all simple parameters (single values)
                    parameter.value = updated_params[parameter_name]
                elif isinstance(parameter, pyo_base.indexed_component.IndexedComponent):
                    # update all indexed parameters (time series)
                    if not isinstance(updated_params[parameter_name], Mapping):
                        parameter[list(parameter)[0]] = updated_params[parameter_name]
                    else:
                        for param_val in list(parameter):
                            parameter[param_val] = updated_params[parameter_name][param_val]

        log.info("Pyomo model parameters updated.")

    def pyo_get_solution(self, names: set[str] | None = None) -> dict[str, float | int | dict[int, float | int]]:
        """Convert the pyomo solution into a more useable format for plotting.

        :param names: Names of the model parameters that are returned
        :return: Dictionary of {parameter name: value} pairs. Value may be a dictionary of {time: value} pairs which
                 contains one value for each optimization time step
        """

        solution = {}

        for com in self._concrete_model.component_objects():
            if com.ctype not in {pyo.Var, pyo.Param, pyo.Objective}:
                continue
            if names is not None and com.name not in names:
                continue  # Only include names that were asked for

            # For simple variables we need just the values, for everything else we want time indexed dictionaries
            if (
                isinstance(com, pyo.SimpleVar)
                or isinstance(com, pyo_base.objective.SimpleObjective)
                or isinstance(com, pyo_base.param.SimpleParam)
            ):
                solution[com.name] = pyo.value(com)
            else:
                solution[com.name] = {}
                if self._use_model_time_increments:
                    for ind, val in com.items():
                        solution[com.name][
                            self.timeseries.index[self.n_steps].to_pydatetime()
                            + timedelta(seconds=ind * self.sampling_time)
                        ] = pyo.value(val)
                else:
                    for ind, val in com.items():
                        solution[com.name][
                            self.timeseries.index[self.n_steps].to_pydatetime() + timedelta(seconds=ind)
                        ] = pyo.value(val)

        return solution
