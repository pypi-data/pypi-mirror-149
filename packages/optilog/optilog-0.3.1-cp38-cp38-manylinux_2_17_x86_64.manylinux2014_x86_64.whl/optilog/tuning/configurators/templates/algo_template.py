import importlib
import pathlib
import sys
import argparse
import pickle
import os

from optilog.tuning import config_str_to_dict
from optilog.tuning import basis

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname('../'))


MODULE_PATH = "__@MODULE#@PATH#__"  # Path to file of entry point function
INPUT_TYPE = "__@INPUT#@TYPE#__"  # Instance type


def load_pickle(module_path):
    path = pathlib.Path(module_path)
    sys.path.append(path.parent.as_posix())
    mod = importlib.import_module(path.stem)

    class CustomUnpickler(pickle.Unpickler):
        def find_class(self, module, name):
            if module == '__main__':
                return getattr(mod, name)
            return super().find_class(module, name)

    with open('arguments.pkl', 'rb') as f:
        return CustomUnpickler(f).load()


types_func = {
    "integer": int,
    "real": float,
    "ordinal": str,
    "categorical": str,
    "bool": lambda x: x == "True"
}


def cast_params(cfg, params):
    d = {}
    for k, v in cfg.items():
        if not isinstance(v, dict):
            param_type = params[k]['type']
            d[k] = types_func[param_type](v)
        else:
            d[k] = cast_params(v, params[k])
    return d


def main(args, params):

    types_input = {
        'int': int,
        'str': str,
        'float': float,
        'bool': lambda x: x == "True"
    }

    instance = types_input[INPUT_TYPE](args.instance)

    c = load_pickle(MODULE_PATH)
    entrypoint = c['entrypoint']
    global_cfgcalls = c['global_cfgcalls']
    data_kwarg = c['data_kwarg']
    seed_kwarg = c['seed_kwarg']
    reverse_index_lookup = c['reverse_index_lookup']

    cfg_input = {
        reverse_index_lookup[param[1:]]: val
        for param, val in zip(params[0::2], params[1::2])
    }

    nested_no_cast = config_str_to_dict(cfg_input)

    for index_global_cfgcalls, cfg in nested_no_cast.items():
        index_global_cfgcalls = index_global_cfgcalls.strip('_')
        fn = global_cfgcalls[int(index_global_cfgcalls)]
        if not hasattr(fn, '_global_cnfg_fn'):
            raise TypeError('Function {} missing configurable decorator'.format(fn.__name__))
        cnfg_fn = fn._global_cnfg_fn
        params = cnfg_fn.get_params()

        cfg = cast_params(cfg, params)
        cnfg_fn.configure(cfg)

    kwargs = {}
    if data_kwarg is not None:
        kwargs[data_kwarg] = instance
    if seed_kwarg is not None:
        kwargs[seed_kwarg] = args.seed
    entrypoint(**kwargs)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance')
    parser.add_argument('--seed', type=int)
    args, params = parser.parse_known_args()
    main(args, params)
