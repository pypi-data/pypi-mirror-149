import ast
from typing import Any, Dict, Sequence, Type

from prometheus_client.metrics import MetricWrapperBase


class MetricNameValidatioError(Exception):
    def __init__(self, name: str):
        self.name = name
        super().__init__(name)


def validate_statement(
    statement: ast.AST,
    valid_name_prefixes: Sequence[str],
    prometheus_mapping: Dict[str, Type[MetricWrapperBase]],
) -> None:
    if not isinstance(statement, ast.Call):
        return

    called = getattr(
        statement.func, 'id', getattr(statement.func, 'attr', None),
    )
    if called is None or called not in prometheus_mapping:
        return
    cls = prometheus_mapping[called]

    args = [
        _parse_call_arguments(arg)
        for arg in statement.args
        if not isinstance(arg, ast.Name)
    ]
    kwargs = {
        kw.arg: _parse_call_arguments(kw.value)
        for kw in statement.keywords
        if not isinstance(kw.value, ast.Name)
    }
    try:
        metric = cls(*args, **kwargs)
    except (ValueError, TypeError):
        return

    metric_name = metric._name  # pylint: disable=W0212
    for prefix in valid_name_prefixes:
        if metric_name.startswith(prefix):
            break
    else:
        raise MetricNameValidatioError(name=metric_name)


def _parse_call_arguments(ast_node: ast.expr) -> Any:
    if isinstance(ast_node, ast.Constant):
        return ast_node.value
    if isinstance(ast_node, ast.Tuple):
        return [
            _parse_call_arguments(inner_node) for inner_node in ast_node.elts
        ]

    return ast_node
