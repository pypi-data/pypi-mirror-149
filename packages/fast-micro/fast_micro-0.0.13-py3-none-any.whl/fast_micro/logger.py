import logging
import logging.config
from multiprocessing import Event
import structlog
from typing import Any, MutableMapping, Optional, Tuple
from starlette_context import context
from structlog.types import WrappedLogger, EventDict


def format_exc_message(logger: WrappedLogger, name: str, event_dict: EventDict) -> EventDict:
    exc_info = event_dict.get("exc_info", None)
    if exc_info and isinstance(exc_info, Tuple):
        event_dict["exception_message"] = exc_info[1]

    return event_dict


shared_processors: Tuple[structlog.types.Processor, ...] = (
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
    format_exc_message,
    structlog.processors.format_exc_info,
)

default_logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": shared_processors,
        }
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "json",
        }
    },
    "loggers": {
        "": {
            "handlers": ["default"], 
            "level": "INFO"
        },
        "fast_micro": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

def setup_logging(log_level: str, logging_config: Optional[dict] = None) -> None:
    def add_app_context(logger: logging.Logger, method_name: str, event_dict: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
        if context.exists():
            event_dict.update(context.data)

        return event_dict

    structlog.configure(
        processors=[
            add_app_context,
            structlog.stdlib.filter_by_level,
            *shared_processors,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    if not logging_config:
        logging_config = default_logging_config

    logging_config["loggers"][""]["level"] = log_level
    logging_config["loggers"]["fast_micro"]["level"] = log_level
    logging.config.dictConfig(logging_config)


def get_logger(mod_name: str) -> structlog.stdlib.BoundLogger:
    """To use this, do logger = get_logger(__name__)

    Parameters
    ----------
    mod_name : str
        Module name

    Returns
    -------
    Logger:
        Logger instance
    """
    logger: structlog.stdlib.BoundLogger = structlog.getLogger(mod_name)
    return logger