import argparse
from collections import Iterable
import inspect
import re

SAVED_WORDS = ['func']


def eval_if_possible(expression):
    try:
        return eval(expression, {})
    except NameError:
        return expression

def get_func_description(f):
    if f.__doc__:
        m = re.match(r"\n\s(.*?)\s*:", f.__doc__, re.DOTALL)
        if m:
            return m.groups(1)[0]


def edit_parser_by_func(parser, f):
    """
    Edit the given parser to support the function signature

    If there is no docstring - set arguments without defaults as positional.
    set arguments with default as optional
    :param parser: edit this parser instead of creating one
    :param f: any function
    """
    function_spec = inspect.getargspec(f)
    assert function_spec.keywords is None, 'can not parse function with keywords'
    params_description = {}
    if f.__doc__:
        m = re.findall(r":param\s?(.*?):\s*?(.*?)\n", f.__doc__, re.DOTALL)
        params_description = dict(m)
    parser.set_defaults(func=f)
    defaults = function_spec.defaults
    if defaults:
        positional = function_spec.args[:-len(defaults)]
        optional = zip(function_spec.args[len(defaults):], defaults)
    else:
        positional = function_spec.args
        optional = []
    for arg in positional:
        parser.add_argument(arg, help=params_description.get(arg))
    for arg, default in optional:
        parser.add_argument('--' + arg, default=default, help=params_description.get(arg, "")
                                                              + " default: {}".format(default))
    varargs = function_spec.varargs
    if varargs:
        parser.add_argument('--' + varargs, nargs='+', help=params_description.get(varargs))


def fun_to_cml(f, args_list=None):
    """
    Takes the arguments from the command line and execute the function
    :param f: callable
    :param args_list: list of argument to parse, default sys.argv
    :return: the function results
    """
    if isinstance(f, Iterable):
        parser = f2multi_parser(f)
    else:
        assert callable(f)
        parser = argparse.ArgumentParser(description=get_func_description(f))
        edit_parser_by_func(parser, f)
    args = vars(parser.parse_args(args_list))
    func = args.pop('func')
    kwargs = {key: eval_if_possible(val) for key, val in args.items() if not isinstance(val, list)}
    varargs = []
    if any(isinstance(val, list) for val in args.values()):
        varargs = [v for v in args.values() if isinstance(v, list)][0]
        varargs = [eval_if_possible(a) for a in varargs]
    return func(*varargs, **kwargs)


def f2multi_parser(f_collection, description=None, title='subcommands'):
    """
    Generate multi parser from function collection
    The parser syntax would by mashehu.py function_name arguments
    :param f_collection: iterable of functions
    :param description: description for the multi parser
    :param title: subcommands title
    :return: parser with subparser for each of the functions
    """
    multi_parser = argparse.ArgumentParser(description=description)
    subparsers = multi_parser.add_subparsers(title=title)
    for f in f_collection:
        f_parser = subparsers.add_parser(f.func_name, description=get_func_description(f))
        edit_parser_by_func(f_parser, f)
    return multi_parser


if __name__ == '__main__':
    import sys
    sys.path.append(r'C:\Users\chaimb\PycharmProjects\function2commandline')
    from tests.test_module import sum_with_documantation, multi_with_documantation
    print fun_to_cml([sum_with_documantation, multi_with_documantation] )