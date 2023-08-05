import logging
import sys

LOG_LEVELS = ['CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG']


def configure_structlog_dev(log_level='WARNING'):
    import structlog

    if isinstance(log_level, str):
        log_level = getattr(logging, log_level)
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            # structlog.processors.CallsiteParameterAdder([
            #     structlog.processors.CallsiteParameter.MODULE,
            #     structlog.processors.CallsiteParameter.FUNC_NAME,
            #     structlog.processors.CallsiteParameter.LINENO,
            # ]),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=False,
    )
