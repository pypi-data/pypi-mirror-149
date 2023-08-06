import argparse
import csv
import io
import json
import math
import sys
import zipfile
from collections import defaultdict, namedtuple
from contextlib import suppress
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from arps.core.resource_category import ValueType
from arps.core.simulator.resource_event import ResourceEvent


def simulation_results_parser(simulation_result_file, output_dir, index_file):
    """
    Parse simulation result file accordingly with configuration file

    Args:
    - simulation_result_file: path to the location of the simulation result file
    - resource category class: class with resource category and its functions
    - output_dir: dir where the figures is saved
    - index_file: index containing all generated figures
    """

    with zipfile.ZipFile(simulation_result_file) as sim_file:
        namelist = sim_file.namelist()
        metadata_path = next(name for name in namelist if name.endswith('json'))
        with sim_file.open(metadata_path) as metadata_file:
            metadata = json.loads(metadata_file.read().decode())

        csv_file = next(name for name in namelist if 'sim_results.log' in name)
        with sim_file.open(csv_file) as fh:
            resources_event_per_env = group_resources_event_by_environment(fh)

    NAME_TEMPLATE = 'env_{}_resource_{}_{}.png'

    saved_figures = list()

    largest_epoch = search_for_largest_epoch(resources_event_per_env)

    figure_index = 0
    for env, resources_event in resources_event_per_env.items():
        for category, resources in resources_event.items():
            resources = resources_axis(category, resources)
            normalize(resources, largest_epoch)
            for resource_id, axis_values in resources.items():
                _ = plt.figure(figure_index)
                figure_index += 1
                x_axis = axis_values[0]
                axis_range = [x_axis[0], x_axis[-1]]
                y_axis = metadata[category]['range']
                value_type = metadata[category]['type']
                if value_type in (ValueType.range.name):
                    axis_range.extend(y_axis)
                    numerical_values = [float(value) for value in axis_values[1]]
                    plt.plot(axis_values[0], numerical_values, 'k')
                    try:
                        if any(math.isinf(x) or math.isnan(x) for x in axis_range):
                            largest = max(numerical_values)
                            if largest == 0:
                                largest = 10  # any number since largest is zero
                            axis_range = [x if not (math.isinf(x) or math.isnan(x)) else largest for x in axis_range]
                            y_axis = [x if not (math.isinf(x) or math.isnan(x)) else largest for x in y_axis]

                        plt.axis(axis_range)
                        plt.ylim(y_axis[0] * -1.01, y_axis[1] * 1.01)
                    except ValueError as err:
                        sys.exit(f'Error while generating graph for category {value_type}: {err}')
                elif value_type == ValueType.category.name:
                    mapped_values = [y_axis.index(v) for v in axis_values[1]]
                    plt.step(axis_values[0], mapped_values, 'k')
                    plt.yticks(range(len(y_axis)), y_axis)
                    plt.xticks(x_axis)
                elif value_type == ValueType.value.name:
                    print('Warning: not implemented for a single value')
                elif value_type == ValueType.complex.name:
                    print('Warning: implementation removed since there is no way to represent every complex object')
                    # Not implemented; I guess complex type will have
                    # to go. Make the user specify a type for each
                    # one of the complex types
                    # axis_range.extend(y_axis)
                    # complex_values = [resource_category.parse(value) for value in axis_values[1]]
                    # values_by_label = defaultdict(list)
                    # for values in complex_values:
                    #     for k, v in values.items():
                    #         values_by_label[k].append(v)

                    # markevery = len(axis_values[0]) // 20

                    # for (label, values), marker in zip(values_by_label.items(), itertools.cycle('+o*x^.d|')):
                    #     plt.plot(axis_values[0], values, label=label, marker=marker, markevery=markevery)
                    #     plt.axis(axis_range)
                    #     plt.ylim(y_axis[0] * -1.01, y_axis[1] * 1.01)
                    #     plt.legend()
                else:
                    raise NotImplementedError(f'Resource category value_type {value_type} not implemented')

                plt.title('Environment: {} | Resource: {} | ID: {}'.format(env, category, resource_id))
                plt.xlabel('time')
                plt.ylabel(category)
                plt.tight_layout()

                png_file = output_dir / NAME_TEMPLATE.format(env, resource_id, simulation_result_file.stem)
                saved_figures.append(str(png_file))
                plt.savefig(png_file)

    with open(index_file, 'w') as index_file:
        json.dump({'results': saved_figures}, index_file)


def resources_axis(resource, events):
    """
    For each resource event, create x and y axis, where x represent
    the time series and y the state of the resource

    Args:
    - resources_event: resources event grouped by their category
    """
    resources = {}
    for event in events:
        events_x, events_y = create_axis(events)
        # if len(events_x) == 1:
        #    continue
        resources[resource] = (events_x, events_y)
    return resources


def create_axis(events):
    """
    Return two sequences for x and y axis, where x is the
    timeseries and y is the resource state

    Args:
    - events: list containing tuples with the state of the
    resource given a specific epoch
    """
    x = list()
    y = list()
    for event in events:
        epoch = event.epoch
        value = event.state
        if epoch in x:
            index = x.index(epoch)
            y[index] = value
        else:
            x.append(epoch)
            y.append(value)

    start = x[0]
    end = x[-1]
    complete_x = list(range(start, end + 1))
    complete_y = list()
    y_it = iter(y)
    current_y = next(y_it)
    for i in complete_x:
        if i not in x:
            complete_y.append(complete_y[-1])
        else:
            complete_y.append(current_y)
            with suppress(StopIteration):
                current_y = next(y_it)

    return complete_x, complete_y


def normalize(resources_by_categories, largest_epoch):
    """
    Organize all timeseries by the serie with the longest duration
    """

    for resource_axis in resources_by_categories.values():
        number_of_missing_values = largest_epoch - len(resource_axis[0])
        if not number_of_missing_values:
            continue
        resource_axis[0].extend(list(range(largest_epoch - number_of_missing_values, largest_epoch)))
        resource_axis[1].extend([resource_axis[1][-1]] * number_of_missing_values)


def search_for_largest_epoch(resources_event_per_env):
    """
    Search for the largest epoch to show all resources using the same scale

    Args:
    - resources_event_per_env:
    """
    largest_epoch = 9
    for resources_event in resources_event_per_env.values():
        for resources in resources_event.values():
            for resource in resources:
                largest_epoch = max(resource.epoch, largest_epoch)
    return largest_epoch


def group_resources_event_by_environment(simulator_result_file):
    """
    Create a structure, for each category, containing a resource and
    its time series related to when it was modified

    Args:
    - simulator_result_file: path to the location of the log file
    """

    EpochState = namedtuple('EpochState', 'epoch state')

    with io.TextIOWrapper(simulator_result_file) as result:
        resources_event = defaultdict(lambda: defaultdict(list))
        events = csv.reader(result, delimiter=';')
        next(events)  # skip header
        for event in events:
            resource_event = ResourceEvent(*event)
            resources_event[resource_event.env][resource_event.identifier].append(
                EpochState(int(resource_event.epoch), resource_event.value)
            )
        return resources_event


def main():
    parser = argparse.ArgumentParser(description='Generate graph of the simulation')
    parser.add_argument('--result_file', help='simulation result zip file path')
    parser.add_argument('--index_file', help='output index file containing the path to all figures created')
    parser.add_argument('--out_dir', help='output directory where the charts will be created', default=None)

    parsed_args = parser.parse_args(sys.argv[1:])
    simulation_result_file = Path(parsed_args.result_file)

    output_dir = (
        Path(parsed_args.out_dir)
        if parsed_args.out_dir and Path(parsed_args.out_dir).is_dir()
        else simulation_result_file.parent
    )

    simulation_results_parser(simulation_result_file, output_dir, parsed_args.index_file)


if __name__ == '__main__':
    main()
