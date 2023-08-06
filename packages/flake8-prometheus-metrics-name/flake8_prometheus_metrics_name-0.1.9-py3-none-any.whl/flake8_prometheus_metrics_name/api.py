import ast
from typing import Any, Sequence

from prometheus_client.metrics import MetricWrapperBase

from flake8_prometheus_metrics_name.cheker import (
    MetricNameValidatioError,
    validate_statement,
)

__version__ = '0.1.9'


class Api:
    name = 'flake8-prometheus-metrics-name'
    version = __version__

    _error_template = (
        'PRM902: Metric name should start with one of following prefixes: {}'
    )
    _valid_name_prefixes: Sequence[str] = ()
    _disabled = False

    def __init__(
        self,
        tree: ast.AST,
        # `filename` arg is required to implement flake8 checker interface
        filename: str,  # pylint: disable=W0613
    ) -> None:
        if self._disabled:
            return

        self._tree = tree

        if not self._valid_name_prefixes:
            raise ValueError(
                'No prefixes for metric name provided. '
                'Ensure option "prometheus-metrics-name-prefixes" is set.'
            )
        prefixes = ', '.join(f'"{s}"' for s in self._valid_name_prefixes)
        self._error_msg = self._error_template.format(prefixes)

        self._called_node_to_prometheus = {
            klass.__name__: klass
            for klass in _collect_subclasses(MetricWrapperBase)
        }

    @classmethod
    def add_options(cls, parser: Any) -> None:
        parser.add_option(
            '--prometheus-metrics-name-prefixes',
            default='',
            action='store',
            type='string',
            help='Possible prometheus metric name prefixes',
            parse_from_config=True,
            comma_separated_list=True,
        )
        parser.add_option(
            '--prometheus-metrics-disabled',
            default=False,
            action='store',
            type='int',
            help='Enabling linter',
            parse_from_config=True,
            comma_separated_list=False,
        )

    @classmethod
    def parse_options(cls, options: Any) -> None:
        cls._disabled = bool(options.prometheus_metrics_disabled)
        if cls._disabled:
            return

        prefixes = options.prometheus_metrics_name_prefixes
        if not isinstance(prefixes, (list, tuple)):
            prefixes = prefixes.split(',')
        cls._valid_name_prefixes = tuple(p.strip() for p in prefixes)

    def run(self):  # type: ignore  # pylint: disable=R1710
        if self._disabled:
            return []

        for statement in ast.walk(self._tree):  # noqa: R503
            try:
                validate_statement(
                    statement=statement,
                    valid_name_prefixes=self._valid_name_prefixes,
                    prometheus_mapping=self._called_node_to_prometheus,
                )
            except MetricNameValidatioError as error:
                yield (
                    statement.lineno,
                    statement.col_offset,
                    f'{self._error_msg}, got "{error.name}" instead',
                    type(self),
                )


def _collect_subclasses(klass: type) -> Sequence[type]:
    all_subclasses = []

    for subclass in klass.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(_collect_subclasses(subclass))

    return all_subclasses
