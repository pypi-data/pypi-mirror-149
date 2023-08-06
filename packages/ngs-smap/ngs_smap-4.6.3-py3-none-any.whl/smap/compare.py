#!usr/bin/python3
import logging
from pathlib import Path
from typing import Iterable, Tuple
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.colors import LinearSegmentedColormap
from pybedtools import Interval
import numpy as np
import pandas as pd
from pybedtools import BedTool
from argparse import ArgumentParser
from matplotlib.backends.backend_pdf import PdfPages
from .plotting import heatmap

LOGGER = logging.getLogger("Compare")
BED_COLUMNS = ['chr', 'start', 'end', 'name', 'read_depth', 'strand', 'SMAP_pos',
               'sample_count', 'SMAP_pos_count', 'label']


def get_set_information(smap_set: Path) -> Tuple[str, int]:
    """Retreive the label and number of samples from a
       SMAP delineate bed file.

    :param smap_set: location of a .bed file containing SMAP delineate merged clusters.
    :type smap_set: Path
    :raises ValueError: The bed files containes more than one sample set.
    :return: The label and number of samples (max of the sample count column) in the set.
    :rtype: Tuple[str, str]
    """
    final_stacks = pd.read_csv(smap_set, names=BED_COLUMNS, header=None, index_col=0, sep="\t")
    label_set_list = set(final_stacks['label'])
    if len(label_set_list) > 1:
        raise ValueError(f'{smap_set} contains more then one sample set '
                         '(duplicate entries in the label column)')
    set_label = label_set_list.pop()
    max_number_of_samples = final_stacks['sample_count'].max()
    return set_label, max_number_of_samples


def intersect(set1: Path, set2: Path) -> Iterable[Interval]:
    joined_stacks = BedTool(set1).cat(BedTool(set2),
                                      s=True,  # strandedness
                                      d=-1,  # Maximum distance for features to merge
                                      c="5,8,10",  # read depth, sample_count, setlabel
                                      o="collapse,collapse,collapse")
    return joined_stacks


def swap(x, y):
    _ = x
    x = y
    y = _
    return x, y


def sets_in_correct_orientation(set1: Path, set2: Path):
    # extract name of set from both files, extract maximal number of samples from both files.
    label_set1, max_number_of_samples_set1 = get_set_information(set1)
    label_set2, max_number_of_samples_set2 = get_set_information(set2)

    if max_number_of_samples_set1 < max_number_of_samples_set2:
        # switch the two sets around so that the plots fit better on a horizontal page
        set1, set2 = swap(set1, set2)
        label_set1, label_set2 = swap(label_set1, label_set2)
        max_number_of_samples_set1, max_number_of_samples_set2 = swap(max_number_of_samples_set1,
                                                                      max_number_of_samples_set2)
    return ((set1, label_set1, max_number_of_samples_set1),
            (set2, label_set2, max_number_of_samples_set2))


def calculate_mean_read_depth(depth, number_of_loci):
    return np.divide(depth, number_of_loci,
                     out=np.zeros_like(depth, dtype=float),
                     where=number_of_loci != 0)


def parse_stack(stack):
    chr, start, stop, stack_depths, stack_counts, stack_names = stack
    stack_names_list = stack_names.partition(',')
    stack_counts_list, stack_depth_list = list(stack_counts.partition(',')), \
        list(stack_depths.partition(','))
    return chr, start, stop, stack_depth_list, stack_counts_list, stack_names_list


def calculate_loci_intersect_statistics(set1: Path, set2: Path):
    set1_info, set2_info = sets_in_correct_orientation(set1, set2)
    set1, label_set1, max_number_of_samples_set1 = set1_info
    set2, label_set2, max_number_of_samples_set2 = set2_info

    joined_merged_clusters = intersect(set1, set2)

    # Contruct matrices to fill, they contain the heatmap data
    # one entry in the heatmap is an element in these arrays
    matrix_shape = (max_number_of_samples_set2+1, max_number_of_samples_set1+1)
    number_of_loci = np.zeros(shape=matrix_shape,
                              dtype=int)
    merged_cluster_depth_set1 = np.zeros(shape=matrix_shape,
                                         dtype=float)
    merged_cluster_depth_set2 = np.zeros(shape=matrix_shape,
                                         dtype=float)

    for stack in joined_merged_clusters:
        chr, start, stop, stack_depth_list, stack_counts_list, stack_names_list\
            = parse_stack(stack)

        label1, _, label2 = stack_names_list
        first_is_set1 = label1 == label_set1

        # ignore lines containing three or more overlapping merged clusters
        if ',' in label2:  # residual clusters that were not split of using partition
            continue

        if not label2:
            # Locus was not observed in one of the two samples
            stack_counts_list[-1] = 0
            stack_depth_list[-1] = 0

        if not first_is_set1:
            # check if set2 comes first, in that case we need to reverse all variables
            stack_counts_list = reversed(stack_counts_list)
            stack_depth_list = reversed(stack_depth_list)

        count_set1, _, count_set2 = stack_counts_list
        count_set1, count_set2 = int(count_set1), int(count_set2)
        depth_set1, _, depth_set2 = stack_depth_list
        depth_set1, depth_set2 = float(depth_set1), float(depth_set2)
        location_in_array = (count_set2, count_set1)

        assert count_set1 <= max_number_of_samples_set1 and \
               count_set2 <= max_number_of_samples_set2
        number_of_loci[location_in_array] += 1
        merged_cluster_depth_set1[location_in_array] += depth_set1
        merged_cluster_depth_set2[location_in_array] += depth_set2

    mean_stack_depth_set1 = calculate_mean_read_depth(merged_cluster_depth_set1, number_of_loci)
    mean_stack_depth_set2 = calculate_mean_read_depth(merged_cluster_depth_set2, number_of_loci)
    return (number_of_loci, mean_stack_depth_set1, mean_stack_depth_set2, label_set1, label_set2)


def get_colormap(number_of_colors: int):
    base_cmap = get_cmap("RdPu", number_of_colors+1)  # Get 7 colors from palette
    newcolors = np.delete(base_cmap(np.linspace(0, 1, number_of_colors+1)),
                          0, axis=0)  # Remove the first one as it is not very visible
    cmap = LinearSegmentedColormap.from_list('compare',
                                             colors=newcolors,
                                             N=number_of_colors)  # Create new map
    cmap.set_bad('lightgray')
    return cmap


def plot_combo(number_of_loci,
               relative_stack_depth_set1,
               relative_stack_depth_set2,
               label_set1, label_set2):
    with PdfPages('SMAP_compare.pdf') as pdf:
        row_labels = f"Completeness {label_set1}\n(occurrence in number of samples)"
        column_labels = f"Completeness {label_set2}\n(occurrence in number of samples)"
        title_completeness_plots = ("Frequency of loci per the number of samples\n"
                                    "from each set in which the loci were observed.")
        plot_options = [
            {
                "title": title_completeness_plots,
                "cbarlabel": "Number of loci",
                "row_label": row_labels,
                "col_label": column_labels,
                "vmin": 1
            },
            {
                "title": (title_completeness_plots +
                          "\nLoci that occurred at least once in both sets."),
                "cbarlabel": "Number of loci",
                "row_label": row_labels,
                "col_label": column_labels,
                "vmin": 1,
                "xmin": 1,
                "ymin": 1,
            },
            {
                "title": f"Mean read depth of {label_set1} loci\n"
                         "stratified per number of set1 (x) and set2 (y)\n"
                         "samples in which the loci were observed.",
                "cbarlabel": "Mean read depth",
                "row_label": row_labels,
                "col_label": column_labels,
                "vmin": 1,

            },
            {
                "title": f"Mean read depth of {label_set2} loci\n"
                         "stratified per number of set1 (x) and set2 (y)\n"
                         "samples in which the loci were observed.",
                "cbarlabel": "Mean read depth",
                "row_label": row_labels,
                "col_label": f"Completeness\n(occurrence in\nnumber of samples\n{label_set2})",
                "vmin": 1,
            }
        ]
        # number_of_overlapping_loci = np.delete(np.delete(number_of_loci, 0, axis=1), 0, axis=0)
        relative_stack_depth_set1[:, 0] = np.nan  # Gray-out first column
        relative_stack_depth_set2[0, :] = np.nan  # Gray-out first row
        data_list = (number_of_loci, number_of_loci,
                     relative_stack_depth_set1, relative_stack_depth_set2)
        for (data, plot_kwargs) in zip(data_list, plot_options):
            plt.figure(figsize=(11.7, 8.3))  # A4 in inch, horizontal
            heatmap(data, cmap=get_colormap(25), **plot_kwargs)
            pdf.savefig()  # saves the current figure into a pdf page
            plt.close()


def parse_args(args):
    compare_parser = ArgumentParser("compare",
                                    description="Compare merged clusters of two SMAP outputs.")

    compare_parser.add_argument('smap_set1',
                                type=Path,
                                help='SMAP delineate output BED file for set 1')

    compare_parser.add_argument('smap_set2',
                                type=Path,
                                help='SMAP delineate output BED file for set 2.')
    return compare_parser.parse_args(args)


def main(args):
    LOGGER.info('SMAP compare started.')
    parsed_args = parse_args(args)
    if not parsed_args.smap_set1.is_file():
        raise ValueError(f"Smap set {parsed_args.smap_set1!s} was not found.")
    if not parsed_args.smap_set2.is_file():
        raise ValueError(f"Smap set {parsed_args.smap_set2!s} was not found.")
    number_of_loci, relative_stack_depth_set1, relative_stack_depth_set2, label_set1, label_set2 = \
        calculate_loci_intersect_statistics(parsed_args.smap_set1, parsed_args.smap_set2)
    LOGGER.info('Overlapping stacks from %s and %s', label_set1, label_set2)
    LOGGER.info('Plotting')
    plot_combo(number_of_loci, relative_stack_depth_set1,
               relative_stack_depth_set2, label_set1, label_set2)
    LOGGER.info('Finished')
