import datetime as dt

import pandas as pd

from lumipy.common.string_utils import indent_str
from lumipy.lab.test.base import BaseExperiment, BaseResult
from typing import Union, List, Any


class ExperimentResult(BaseResult):
    """Class that represents the result for a single luminesce query experiment.

    """

    def __init__(self):
        """Constructor for the luminesce experiment result class.

        """
        self.submitted = pd.NaT
        self.get = pd.NaT
        self.download_finish = pd.NaT
        self.obs_rows = None
        self.obs_cols = None
        self.query_time = None
        self.download_time = None
        super().__init__()


class LusidResult(BaseResult):
    # todo: move to another module under lusid.lab?
    def __init__(self):
        self.call_start = pd.NaT
        self.call_end = pd.NaT
        self.call_time = None
        super().__init__()


class LusidExperiment(BaseExperiment):

    # todo: move to another module under lusid.lab?
    def __init__(
            self,
            build_fn,
            *ranges: Union[List[Union[int, float]], Union[int, float]],
            **kwargs: Any
    ):
        self.build_fn = build_fn
        self.throw_on_failure = kwargs.get('throw_on_failure', True)
        super().__init__(*ranges, **kwargs)

    def copy(self, seed: int, quiet: bool):
        return LusidExperiment(self.build_fn, *self._ranges, seed=seed, quiet=quiet)

    def _init_result(self) -> LusidResult:
        return LusidResult()

    def _job(self, args: List[Union[int, float]]) -> None:

        def extract_request_id(x):
            rl_link = [link for link in x.links if link.relation == 'RequestLogs']
            if len(rl_link) != 1:
                raise ValueError("")

            return rl_link[0].href.split('/')[-1]

        def extract_failures(x):
            if hasattr(x, 'failed'):
                return list(x.failed.values())
            return []

        fn = self.build_fn(*args)
        
        self._return.call_start = dt.datetime.utcnow()
        res = fn()
        self._return.call_end = dt.datetime.utcnow()

        self._return.execution_id = extract_request_id(res)

        failures = extract_failures(res)

        if len(failures) > 0 and self.throw_on_failure:
            fail_str = '\n,'.join(map(str, failures))
            raise ValueError(f"There were {len(failures)} failures in the response (throw_on_failure = True):"
                             f"\n{fail_str}")

        self._return.call_time = (self._return.call_end - self._return.call_start).total_seconds()


class Experiment(BaseExperiment):
    """Class that encapsulates a luminesce experiment.

    """

    def __init__(
            self,
            build_fn,
            *ranges: Union[List[Union[int, float]], Union[int, float]],
            **kwargs: Any
    ):
        """Constructor for the experiment class.

        Args:
            build_fn (Callable): a function that returns a lumipy query object when given a set of values.
            *ranges (Union[List[Union[int, float]], Union[int, float]]): single constant values or ranges to randomly
            sample for the experiment.

        Keyword Args:
            seed (int): random seed to set in numpy when selecting experiment arg values.
            quiet (bool): whether to suppress log printouts during the experiment.

        """
        self.build_fn = build_fn
        super().__init__(*ranges, **kwargs)

    def copy(self, seed: int, quiet: bool):
        """Make an independent copy of this experiment object.

        Args:
            seed (int): random seed to set in numpy when selecting experiment arg values.
            quiet (bool): whether to suppress log printouts during the experiment.

        Returns:
            Experiment: an independent copy of this experiment.
        """
        return Experiment(self.build_fn, *self._ranges, seed=seed, quiet=quiet)

    def _init_result(self) -> ExperimentResult:
        return ExperimentResult()

    def _job(self, args) -> None:
        qry = self.build_fn(*args)

        if not self._quiet:
            print(indent_str(qry.get_sql(), 4), end='\n\n')

        if self.should_stop():
            return

        job = qry.go_async()
        self._return.execution_id = job.ex_id
        self._return.submitted = dt.datetime.utcnow()

        if self.should_stop():
            return

        job.interactive_monitor(self._quiet, 0.1, self.should_stop)

        if self.should_stop():
            return

        self._return.get = dt.datetime.utcnow()
        df = job.get_result(quiet=self._quiet)
        self._return.download_finish = dt.datetime.utcnow()

        self._return.obs_rows = df.shape[0]
        self._return.obs_cols = df.shape[1]

        self._return.query_time = (self._return.get - self._return.start).total_seconds()
        self._return.download_time = (self._return.download_finish - self._return.get).total_seconds()
