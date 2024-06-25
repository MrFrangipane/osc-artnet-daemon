# FIXME: please redo all the configuration loading
from copy import deepcopy


def _updated(original: dict, new_data: dict) -> dict:
    copied = deepcopy(original)
    for k, v in new_data.items():
        if k not in copied:
            copied[k] = v
    return copied


def _named(layer_name: str, control: dict) -> dict:
    copied = deepcopy(control)
    copied['name'] = f"{layer_name}.{copied['control']}"
    return copied


def hack_layer_groups(layer_groups: dict):
    for group in layer_groups:
        all_controls = dict()
        for layer in group['layers']:
            for control in layer['controls']:
                if not control['control'] in all_controls:
                    all_controls[control['control']] = {'control': control['control']}

        for layer in group['layers']:
            controls = {c['control']: c for c in layer['controls']}
            controls = _updated(original=controls, new_data=all_controls)
            controls = [_named(layer['name'], control) for control in controls.values()]
            layer['controls'] = controls

    return layer_groups
