from typing import Callable

from tenacity import RetryCallState
from tenacity import _utils


def after_log() -> Callable[["RetryCallState"], None]:
    """After call strategy that logs to some logger the finished attempt."""

    def log_it(retry_state: "RetryCallState") -> None:
        args = retry_state.args
        if len(args) > 0 and hasattr(args[0], "_log"):
            args[0]._log.warning(f"Error: {repr(retry_state.outcome.exception())} ")

            args[0]._log.warning(
                f"Finished call to '{_utils.get_callback_name(retry_state.fn)}' "
                f"after {retry_state.seconds_since_start}(s), "
                f"this was the {_utils.to_ordinal(retry_state.attempt_number)} time calling it.",
            )

    return log_it
