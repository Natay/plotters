import numpy as np
import matplotlib.pyplot as plt
import csv


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

    fig, ax = plt.subplots(figsize=(190.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for res in results:
        # Get the list of segments to plot
        vals = results[res]
        # Compute the sum of all segments to use for percentages.
        total = sum([int(v.split(':')[0]) for v in vals if v.split(':')[-1] != 'white'])
        for i, p in enumerate(vals):
            # Get the label name, and color of each segment
            _, _, name, color = p.split(':')

            widths = data[:, i]
            # Ensure no overlap with previous segment
            starts = data_cum[:, i] - widths
            # Plot the segment
            ax.barh(labels, widths, left=starts,  height=0.5, color=color)

            # Center label text.
            xcenters = starts + widths / 2

            # Add labels to segments
            for y, (x, c) in enumerate(zip(xcenters, widths)):
                # 'white' segments are a gap.
                percent = (int(c) / total) * 100
                percent = "{0:.2f}".format(percent)
                label = '' if color == 'white' else f"{name}\n( {percent}% )"
                ax.text(x, y, label, ha='center', va='center',
                        color='black', rotation='vertical', fontsize=9)
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


def parse_data(fname):
    """
    Parse file and return a data dict.
    """

    data_dict = dict()
    file_stream = open(fname, 'r')
    csvreader = csv.reader(file_stream, delimiter='\t')

    colors = 'rgbymc'
    color_cycle = 0

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

        color = colors[color_cycle % len(colors)]
        # Add this segment to data dict.
        current_store.append(f"{diff}:{end}:{name}:{color}")

        # Add a black bar between segments
        data_dict[y_label] = current_store
        color_cycle += 1

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
