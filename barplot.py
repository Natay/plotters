import numpy as np
import matplotlib.pyplot as plt
import csv
import random


def stacked_horizontal_barplot(results):
    """
    """
    labels = list(results.keys())

    data = []
    # Parse the numerical values to plot.
    for x in results:
        d = [int(v.split(':')[0]) for v in results[x]]
        data.append(d)

    data = np.array(data)

    data_cum = data.cumsum(axis=1)

    fig, ax = plt.subplots(figsize=(19.2, 5))
    ax.invert_yaxis()
    plt.subplots_adjust(right=.83)

    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())
    category_names = set()

    for res in results:
        # Get the list of segments to plot
        vals = results[res]
        # Compute the sum of all segments to use for percentages.
        for i, p in enumerate(vals):
            # Get the label name, and color of each segment
            _, _, name, color = p.split(':')
            widths = data[:, i]
            # Ensure no overlap with previous segment
            starts = data_cum[:, i] - widths
            # Plot the segment
            if name not in category_names:
                ax.barh(labels, widths, left=starts,  label=name, height=0.5, color=color)
            else:
                ax.barh(labels, widths, left=starts, height=0.5, color=color)

            category_names.update([name])

    ax.legend(bbox_to_anchor=(1.04,1), loc="upper left")

    return fig, ax


def determine_gap(current_store, start):
    """
    Determine the gap between previous end and current start
    """
    gap = ''
    if not current_store:
        return gap

    # Get the previous data values.
    previous = current_store[-1].split(':')
    previous_diff, previous_end, previous_name, color = previous
    previous_diff, previous_end = int(previous_diff), int(previous_end)

    if previous_end != start:
        # The size of the gap will be proportional to the difference between the current
        # start and previous end.
        gap_diff = start - previous_end
        gap = f"{gap_diff}:::white"

    return gap


def get_color(name):

    color_map = dict(chr6_BT_minus='#4fff38', chr6_BT_plus='#03a7ff',
                     chr8_BT_minus='#0010a3', chr8_BT_plus='#db00d8',
                     chr4_BT_plus='#9900ff', chr4_BT_minus='#ffff05',
                     chr11_BT_minus='#8ca61b', chr11_BT_plus='#878787',
                     chr17_BT_plus='#00f2ff', chr17_BT_minus='#27686b',
                     chr5_BT_plus='#ffe838', chr5_BT_minus='#8a2c00',
                     chr27_BT_plus='#9c6d38', chr27_BT_minus='#ff8700',
                     chr21_BT_plus='#82005d', chr21_BT_minus='#0d0009',
                     )

    color = color_map.get(name, 'black')

    return color


def parse_data(fname):
    """
    Parse file and return a data dict.
    """

    data_dict = dict()
    file_stream = open(fname, 'r')
    csvreader = csv.reader(file_stream, delimiter='\t')

    # Assumes the data is already sorted.
    for line in csvreader:
        y_label, start, end, name, _, plus_minus = line
        start, end = int(start), int(end)
        # Get the value to plot
        diff = end - start
        current_store = data_dict.get(y_label, [])
        # Fill in gaps between previous end and current start
        gap = determine_gap(current_store=current_store, start=start)
        if gap:
            current_store.append(gap)

        color = get_color(name)
        # Add this segment to data dict.
        current_store.append(f"{diff}:{end}:{name}:{color}")

        # Add a black bar between segments
        data_dict[y_label] = current_store

    return data_dict


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--file', type=str, dest='file', help='Files to be plotted')
    args = parser.parse_args()

    fname = args.file

    results = parse_data(fname=fname)

    stacked_horizontal_barplot(results)

    plt.show()


if __name__ == "__main__":
    main()
