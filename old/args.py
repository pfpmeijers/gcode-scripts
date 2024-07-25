import sys
import os
import inspect
from dataclasses import dataclass
from typing import Any, Optional, Tuple, List, Callable


@dataclass
class ArgSpec:
    name: str
    optional: bool
    default: Any
    description: Optional[str]


def get_args_count(f: Callable) -> int:
    return len(inspect.getfullargspec(f).args)


def get_mandatory_args_count(f: Callable) -> int:
    return get_args_count(f) - get_default_args_count(f)


def get_default_args_count(f: Callable) -> int:
    defaults = inspect.getfullargspec(f).defaults
    return len(defaults) if defaults else 0


def get_arg_defaults(f: Callable) -> Optional[Tuple[str]]:
    return inspect.getfullargspec(f).defaults


def get_arg_names(f: Callable) -> List[str]:
    return inspect.getfullargspec(f).args


def get_arg_specs(f: Callable) -> List[ArgSpec]:
    arg_specs = inspect.getfullargspec(f)
    args = arg_specs.args
    defaults = arg_specs.defaults
    n = get_mandatory_args_count(f)
    arg_specs = []
    for i, arg_name in enumerate(args):
        arg_specs.append(ArgSpec(arg_name, i >= n, defaults[i - n] if i >= n else None, None))
    return arg_specs


def print_usage(f: Callable):
    name = os.path.basename(inspect.getfile(f))
    print("Usage: {} ".format(name), end="")
    for arg_spec in get_arg_specs(f):
        print((" [{}]" if arg_spec.optional else " <{}>").format(arg_spec.name), end="")
    print()


def get_args(f: Callable) -> List[Any]:
    arg_specs = inspect.getfullargspec(f)
    if len(sys.argv) - 1 <= len(arg_specs.args):
        return [arg_specs.annotations[arg_specs.args[i]](arg) for i, arg in enumerate(sys.argv[1:])]
    else:
        return []
