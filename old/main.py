from typing import Union, Callable, Tuple

from GCode import GCode
from old.args import get_mandatory_args_count, get_arg_specs, print_usage, get_args, get_args_count


def main_call(f: Callable, description: str = None, arg_descriptions: Tuple[Union[Tuple[str, str], str], ...] = None):

    def print_info():
        if description is not None:
            print(description)
        print_usage(f)
        if arg_descriptions is not None:
            arg_specs = get_arg_specs(f)
            i = 0
            for arg_description in arg_descriptions:
                if isinstance(arg_description, tuple):
                    arg_name, arg_specs[i].description = arg_description
                    ii = i
                    while arg_name.find(arg_specs[i].name) != -1:
                        arg_specs[i].name = ""
                        i += 1
                    arg_specs[ii].name = arg_name
                else:
                    arg_specs[i].description = arg_description
                    i += 1
            max_arg_name_len = max(len(arg_spec.name) for arg_spec in arg_specs)
            for arg_spec in arg_specs:
                if arg_spec.name != "":
                    print("- {}{} : {} {}".format(
                        arg_spec.name,
                        " " * (max_arg_name_len - len(arg_spec.name)), arg_spec.description,
                        " (optional; default: {})".format(arg_spec.default) if arg_spec.optional else ""))

    args = get_args(f)
    if len(args) < get_mandatory_args_count(f) or len(args) > get_args_count(f):
        print_info()
        exit()

    gcode = GCode()
    gcode.start()
    f(gcode, *args)
    gcode.finish()
