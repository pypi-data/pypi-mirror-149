import glob
import json
import logging
import os
import platform
import subprocess
import tempfile
import typing

import pandas

import pydelica.exception as pde
from pydelica.compiler import Compiler
from pydelica.logger import OMLogLevel
from pydelica.model import Model
from pydelica.options import SimulationOptions, Solver
from pydelica.solutions import SolutionHandler


class Session:
    def __init__(self, log_level: OMLogLevel = OMLogLevel.NORMAL) -> None:
        """Session object which handles model runs.

        This class is used to initiate model runs, building the models and
        allowing the user to set parameter values etc.

        Parameters
        ----------
        log_level : OMLogLevel, optional
            level of Modelica logging, by default OMLogLevel.NORMAL
        """
        self._solutions: typing.Dict[str, SolutionHandler] = {}
        self._model_parameters: typing.Dict[str, Model] = {}
        self._simulation_opts: typing.Dict[str, SimulationOptions] = {}
        self._current_profile: typing.Optional[typing.Dict] = None
        self._current_info: typing.Optional[typing.Dict] = None
        self._binaries: typing.Dict[str, str] = {}
        self._custom_libraries: typing.List[typing.Dict[str, str]] = []
        self._logger: logging.Logger = logging.getLogger("PyDelica")
        if log_level == OMLogLevel.DEBUG:
            self._logger.setLevel(logging.DEBUG)
        self._compiler = Compiler()
        self._log_level = log_level
        self._session_directory = os.getcwd()
        self._assert_fail_level = "error"

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self._compiler.clear_cache()

    def use_libraries(self, library_specs: typing.List[typing.Dict[str, str]]) -> None:
        """Use a Modelica library specification list

        Parameters
        ----------
        libary_specs : typing.List[typing.Dict[str, str]]
            list of dictionaries containing version and location info of libraries
        """
        self._custom_libraries = library_specs

    def use_library(
        self, library_name: str, library_version: str = "", library_directory: str = ""
    ) -> None:
        """Specify version of a library to use

        Parameters
        ----------
        library_name : str
            name of the Modelica library
        library_version : str, optional
            semantic version number, by default latest
        library_directory : str, optional
            location of library on system, by default OM default paths
        """
        self._custom_libraries.append(
            {
                "name": library_name,
                "version": library_version,
                "directory": library_directory,
            }
        )

    def fail_on_assert_level(self, assert_level: str) -> None:
        """Change assertion level on which model execution should fail

        By default Modelica model simulation will only fail if an assertion
        of level 'error' is given. The possible values and rankings are:

        info < warning < error < never

        where 'never' will mean no exception is raised

        Parameters
        ----------
        assert_level : str
            new level of assertion to trigger failure
        """
        if assert_level in {"info", "warning", "error", "debug", "never"}:
            self._assert_fail_level = assert_level
        else:
            raise pde.UnknownOptionError(
                f"Cannot set program fail assertion trigger to {assert_level}, "
                "not a valid option"
            )

    @property
    def code_profile(self) -> typing.Optional[typing.Dict]:
        return self._current_profile

    @property
    def code_info(self) -> typing.Optional[typing.Dict]:
        return self._current_info

    def _recover_profile(self, build_dir: str, run_dir: str) -> None:
        """Recovers a profile file if one exists"""
        _prof_files = glob.glob(os.path.join(run_dir, "*_prof.json"))
        _info_files = glob.glob(os.path.join(build_dir, "*_info.json"))
        if _prof_files:
            self._current_profile = json.load(open(_prof_files[0]))
        if _info_files:
            self._current_info = json.load(open(_info_files[0]))

    def build_model(
        self,
        modelica_source_file: str,
        model_addr: str = None,
        extra_models: typing.Optional[typing.List[str]] = None,
        c_source_dir: str = None,
        profiling: str = None,
        update_input_paths_to: str = None,
        omc_build_flags: typing.Optional[typing.Dict[str, typing.Optional[str]]] = None,
    ):
        """Build a Modelica model from a source file

        Parameters
        ----------
        modelica_source_file : str
            Modelica source file to compile
        model_addr : str, optional
            address of model within source file, else default
        extra_models : typing.Optional[typing.List[str]], optional
            additional models required for compile, by default None
        c_source_dir : str, optional
            directory containing any additional required C sources, by default None
        profiling : str, optional
            if set, activates the OMC profiling at the specified level
        update_input_paths_to : str, optional
            update input paths within model to another location, by default None
        omc_build_flags : typing.Optional[typing.Dict[str, typing.Optional[str]]]
            additional flags to pass to the OMC compiler

        Raises
        ------
        pde.ModelicaFileGenerationError
            if the XML parameter file was not generated
        RuntimeError
            If model compilation failed
        """
        if not omc_build_flags:
            omc_build_flags = {}

        self._logger.debug(
            "Building model %sfrom file '%s'",
            f"{model_addr} " if model_addr else "",
            modelica_source_file,
        )

        for flag, value in omc_build_flags.items():
            self._compiler.set_omc_flag(flag, value)

        self._compiler.set_profile_level(profiling)

        _binary_loc = self._compiler.compile(
            modelica_source_file=modelica_source_file,
            model_addr=model_addr,
            extra_models=extra_models,
            c_source_dir=c_source_dir,
            custom_library_spec=self._custom_libraries,
        )

        _xml_files = glob.glob(os.path.join(_binary_loc, "*.xml"))

        if not _xml_files:
            raise pde.ModelicaFileGenerationError(
                "Failed to retrieve XML files from model compilation"
            )

        self._logger.debug("Parsing generated XML files")
        for xml_file in _xml_files:
            _model_name = os.path.basename(xml_file).split("_init")[0]
            self._model_parameters[_model_name] = Model(modelica_source_file, xml_file)

            _binary = _model_name

            if platform.system() == "Windows":
                _binary += ".exe"

            self._binaries[_model_name] = os.path.join(
                os.path.abspath(_binary_loc), _binary
            )

            if not os.path.exists(self._binaries[_model_name]):
                raise RuntimeError(
                    f"Compilation of model '{_model_name}' failed, "
                    f"no binary '{self._binaries[_model_name]}' found."
                )

            self._logger.debug(
                "Located compiled binary '%s'", self._binaries[_model_name]
            )

            self._solutions[_model_name] = SolutionHandler(self._session_directory)

            self._logger.debug(
                "Extracting default simulation options for model '%s' from XML file",
                _model_name,
            )

            self._simulation_opts[_model_name] = SimulationOptions(xml_file)

            # Option to update any variable recognised as an input
            # i.e. .mat/.csv to point to the correct location as an
            # absolute path
            if update_input_paths_to:
                self._set_input_files_directory(_model_name, update_input_paths_to)

            # Allows easy creation of a Pandas dataframe for displaying solutions
            self._set_output_to_csv()

    def get_binary_location(self, model_name: str):
        if model_name not in self._binaries:
            raise pde.BinaryNotFoundError(
                f"Failed to retrieve binary for model '{model_name}'"
            )
        return self._binaries[model_name]

    def get_parameters(
        self, model_name: str = None
    ) -> typing.Union[Model, typing.Dict[str, typing.Any]]:
        """Retrieve a full parameter list

        Parameters
        ----------
        model_name : str, optional
            specify name of model to extract parameters, by default extract all

        Returns
        -------
        typing.Dict[str, typing.Any]
            dictionary containing parameters by name and their values
        """
        if model_name:
            if model_name not in self._model_parameters:
                raise pde.UnknownModelError(model_name)

            return self._model_parameters[model_name]
        else:
            _out_params: typing.Dict[str, typing.Any] = {}
            for model in self._model_parameters:
                for param in self._model_parameters[model]:
                    if param in _out_params:
                        continue
                    _out_params[param] = self._model_parameters[model][param]
        return _out_params

    def get_parameter(self, param_name: str) -> typing.Any:
        """Retrieve the value of a specific parameter

        Parameters
        ----------
        param_name : str
            name of parameter to retrieve

        Returns
        -------
        typing.Any
            the value of the parameter specified
        """
        for model in self._model_parameters:
            if param_name in self._model_parameters[model]:
                if isinstance(
                    self._model_parameters[model].get_parameter(param_name),
                    dict,
                ):
                    raise AssertionError(
                        "Expected non-mutable value for requested parameter"
                        f"'{param_name}' but got type 'dict'"
                    )
                return self._model_parameters[model].get_parameter(param_name)
        raise pde.UnknownParameterError(param_name)

    def get_simulation_options(self, model_name: str = None) -> SimulationOptions:
        """Retrieve typing.Dictionary of the Simulation Options

        Parameters
        ----------
        model_name : str
            name of model to get simulation options for

        Returns
        -------
        SimulationOptions
            dictionary containing all simulation options

        Raises
        ------
        KeyError
            if the given model name is not recognised
        """
        if not model_name:
            model_name = list(self._binaries.keys())[0]
        if model_name not in self._simulation_opts:
            raise pde.UnknownModelError(model_name)
        return self._simulation_opts[model_name]

    def get_simulation_option(self, option: str, model_name: str = None) -> typing.Any:
        """Retrieve a single option for a given model.

        Parameters
        ----------
        option : str
            option to search for
        model_name : str, optional
            name of modelica model

        Returns
        -------
        typing.Any
            value for the given option

        Raises
        ------
        KeyError
            if the given model is not recognised
        KeyError
            if the given option name is not recognised
        """
        if not model_name:
            return self._simulation_opts[list(self._binaries.keys())[0]][option]
        else:
            return self._simulation_opts[model_name][option]

    def set_parameter(self, param_name: str, value: typing.Any) -> None:
        """Set a parameter to a given value

        Parameters
        ----------
        param_name : str
            name of model parameter to update
        value : typing.Any
            new value to assign to the given parameters
        """
        if isinstance(value, dict):
            raise TypeError(
                "Cannot assign a value of type dictionary as a parameter value"
                f" for parameter '{param_name}'"
            )
        self._logger.debug(
            "Searching for parameter '%s' and assigning new value", param_name
        )
        for model in self._model_parameters:
            if param_name in self._model_parameters[model]:
                self._model_parameters[model].set_parameter(param_name, value)
                return
        raise pde.UnknownParameterError(param_name)

    def _set_input_files_directory(
        self, model_name: str, input_dir: str = None
    ) -> None:
        if not input_dir:
            input_dir = os.path.dirname(
                self._model_parameters[model_name].get_source_path()
            )

        for param, value in self._model_parameters[model_name].items():
            if not value["value"]:
                continue

            _has_addr_elem = any(
                i in value["value"]
                for i in [os.path.sep, ".mat", ".csv"]
                if value["type"] == str
            )

            if value["type"] == str and _has_addr_elem:
                _addr = os.path.join(input_dir, value["value"])
                self._model_parameters[model_name].set_parameter(param, _addr)

    def simulate(
        self, model_name: str = None, verbosity: typing.Optional[OMLogLevel] = None
    ) -> None:
        """Run simulation using the built models

        Parameters
        ----------
        model_name : str, optional
            Specify model to execute, by default use first in list
        verbosity : OMLogLevel, optional
            specify level of Modelica outputs, else use default
        """
        if not model_name:
            model_name = list(self._binaries.keys())[0]
            self._logger.warning(
                "No model name specified, using first result '%s'", model_name
            )
        if model_name not in self._binaries:
            raise pde.BinaryNotFoundError(
                f"Could not find binary for Model '{model_name}',"
                " did you run 'build_models' on the source file?"
            )

        self._logger.debug("Launching simulation for model '%s'", model_name)

        # Write parameters to the XML file read by the binary
        self._model_parameters[model_name].write_params()

        _binary_dir = os.path.dirname(self._binaries[model_name])

        _args = [self._binaries[model_name], f"-inputPath={_binary_dir}"]

        if not os.path.exists(self._binaries[model_name]):
            raise pde.BinaryNotFoundError(
                f"Failed to retrieve binary for model '{model_name}' "
                f"from location '{_binary_dir}'"
            )

        if verbosity and verbosity.value:
            _args += [verbosity.value]
        elif self._log_level.value:
            _args += [self._log_level.value]

        with tempfile.TemporaryDirectory() as run_dir:

            _run_sim = subprocess.run(
                _args,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
                shell=False,
                cwd=run_dir,
            )

            pde.parse_error_string_simulate(_run_sim.stdout, self._assert_fail_level)

            if _run_sim.returncode != 0:
                raise pde.OMExecutionError(
                    f"[{_run_sim.returncode}] Simulation failed with:\n{_run_sim.stderr}"
                )

            self._solutions[model_name].retrieve_session_solutions(run_dir)
            self._recover_profile(os.path.dirname(self._binaries[model_name]), run_dir)

    def _set_output_to_csv(self):
        for model in self._simulation_opts:
            self._simulation_opts[model].set_option("outputFormat", "csv")

    def set_solver(self, solver: Solver, model_name: str = None) -> None:
        if model_name:
            self._simulation_opts[model_name].set_option("solver", solver.value)
        else:
            for model in self._simulation_opts:
                self._simulation_opts[model].set_option("solver", solver.value)

    def set_time_range(
        self,
        start_time: int = None,
        stop_time: int = None,
        model_name: str = None,
    ) -> None:
        if model_name:
            if start_time:
                self._simulation_opts[model_name].set_option("startTime", start_time)
            if stop_time:
                self._simulation_opts[model_name].set_option("stopTime", stop_time)
        else:
            for model in self._simulation_opts:
                if start_time:
                    self._simulation_opts[model].set_option("startTime", start_time)
                if stop_time:
                    self._simulation_opts[model].set_option("stopTime", stop_time)

    def set_tolerance(self, tolerance: float, model_name: str = None) -> None:
        if model_name:
            self._simulation_opts[model_name].set_option("tolerance", tolerance)
        else:
            for model in self._simulation_opts:
                self._simulation_opts[model].set_option("tolerance", tolerance)

    def set_variable_filter(self, filter_str: str, model_name: str = None) -> None:
        if model_name:
            self._simulation_opts[model_name].set_option("variableFilter", filter_str)
        else:
            for model in self._simulation_opts:
                self._simulation_opts[model].set_option("variableFilter", filter_str)

    def set_simulation_option(
        self, option_name: str, value: typing.Any, model_name: str = None
    ) -> None:
        if model_name:
            self._simulation_opts[model_name].set_option(option_name, value)
        else:
            for model in self._simulation_opts:
                self._simulation_opts[model].set_option(option_name, value)

    def get_solutions(self) -> pandas.DataFrame:
        """Returns solutions to all simulated models as a dictionary of dataframes

        Outputs are written as Pandas dataframes the columns of which can be
        accessed by variable name.

        Returns
        -------
        typing.Dict
            dictionary containing outputs to all simulated models as Pandas
            dataframes

        Raises
        ------
        pde.BinaryNotFoundError
            if no models have been compiled
        """
        if not self._binaries:
            raise pde.BinaryNotFoundError(
                "Cannot retrieve solutions, you need to compile and"
                " run one or more models first"
            )

        # The SolutionHandler class takes into account the case of multiple
        # output files, however with OM there is only ever a single file per
        # model so we only need to retrieve the first one

        return {
            model: self._solutions[model].get_solutions()[
                list(self._solutions[model].get_solutions().keys())[0]
            ]
            for model in self._solutions
        }
