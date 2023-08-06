from collections import defaultdict
from typing import Dict

import yaml
from pyrasgo.schemas.transform import Transform, TransformArgument
from pyrasgo.schemas.dataset import Dataset
from pyrasgo.schemas.dw_operation_set import OperationSet


def parse_operation(
    operation_args: Dict[str, any],
    used_transform: Transform,
    all_arguments: Dict[str, any],
    dependency_names: Dict[str, any],
):
    transform_args = {}
    for arg, value in operation_args.items():
        # this arg is a previous operation
        if str(value) in dependency_names:
            transform_args[arg] = f"{{{{{dependency_names[value]}}}}}"
        # it's a regular arg
        else:
            if arg == 'source_table':
                used_argument = TransformArgument(
                    name='dummy',
                    description='A source table argument that must be passed to this Accelerator',
                    type='dataset',
                )

                argument_create = {
                    "name": f'{arg}{"_"+str(len(all_arguments[arg])) if  arg in all_arguments else ""}',
                    "description": used_argument.description,
                    "argument_type": used_argument.type,
                }

                dependency_names[value] = arg
                transform_args[arg] = f"{{{{{argument_create['name']}}}}}"
                all_arguments[arg].append(argument_create)
            else:
                transform_args[arg] = value

    return (
        {
            'description': used_transform.description.replace('\n', ''),
            'transform_name': used_transform.name,
            'transform_arguments': transform_args,
        },
        all_arguments,
        dependency_names,
    )


def escape_name(name: str) -> str:
    return name.replace(' ', '_').lower()


def dataset_to_accelerator_yaml(api_dataset: Dataset, api_operation_set: OperationSet) -> str:
    from pyrasgo.api.get import Get

    get = Get()

    all_arguments = defaultdict(list)
    accelerator_operations = {}
    used_transforms = {}
    dependency_names = {}

    for operation in api_operation_set.operations:
        # get the transform def, fetch it if we haven't already. It could be deleted and that's okay, we really just need the name.
        used_transforms[operation.transform_id] = used_transforms.get(
            operation.transform_id, get.transform(operation.transform_id)
        )
        used_transform = used_transforms.get(operation.transform_id)
        if not used_transform:
            raise AttributeError(
                f"Transform {operation.transform_id} referenced in {operation.operation_name} is not available"
            )

        (
            accelerator_operations[escape_name(operation.operation_name)],
            all_arguments,
            dependency_names,
        ) = parse_operation(operation.operation_args, used_transform, all_arguments, dependency_names)
        dependency_names[operation.dw_table.fqtn] = operation.operation_name

    for insight in api_dataset.insights:
        used_transforms[insight.source_transform_id] = used_transforms.get(
            insight.source_transform_id, get.transform(insight.source_transform_id)
        )
        used_transform = used_transforms.get(insight.source_transform_id)
        if not used_transform:
            raise AttributeError(
                f"Transform {insight.source_transform_id} referenced in {insight.name} is not available"
            )

        parsed, all_arguments, dependency_names = parse_operation(
            insight.transform_arguments, used_transform, all_arguments, dependency_names
        )
        accelerator_operations[escape_name(insight.name)] = {'operation_type': 'INSIGHT', **parsed}

    final_args = {}
    for arg_list in all_arguments.values():
        final_args.update({x.pop('name'): x for x in arg_list})

    ac = {
        'name': f"{api_dataset.name} Accelerator",
        'description': f"Accelerator template created from Dataset {api_dataset.id}",
        'arguments': final_args,
        'operations': accelerator_operations,
    }
    return yaml.safe_dump(ac, sort_keys=False)
