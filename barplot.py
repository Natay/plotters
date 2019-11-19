import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def get_segs_count(data_dict):

    max_nsegs = 0
    for d in data_dict:
        nsegs = len(data_dict[d]['segs'])
        if max_nsegs < nsegs:
            max_nsegs = nsegs

    return max_nsegs


def plot():
    people = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
    segments = 9

    # generate some multi-dimensional data & arbitrary labels
    data = 3 + 10 * np.random.rand(segments, len(people))
    percentages = (np.random.randint(5, 20, (len(people), segments)))
    y_pos = np.arange(len(people))

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    colors = 'rgbwmc'
    patch_handles = []
    left = np.zeros(len(people))  # left alignment of data starts at zero
    for i, d in enumerate(data):
        patch_handles.append(ax.barh(y_pos, d,
                                     color=colors[i % len(colors)], align='center',
                                     left=left))
        # accumulate the left-hand offsets
        left += d

    # go through all of the bar segments and annotate
    for j in range(len(patch_handles)):
        for i, patch in enumerate(patch_handles[j].get_children()):
            bl = patch.get_xy()
            x = 0.5 * patch.get_width() + bl[0]
            y = 0.5 * patch.get_height() + bl[1]
            ax.text(x, y, "%d%%" % (percentages[i, j]), ha='center')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.set_xlabel('Distance')

    plt.show()


def horizontal_plot(data_dict):

    # Example data
    fig, ax = plt.subplots()
    y_pos = range(len(data_dict))
    y_labels = data_dict.keys()

    for idx, data in enumerate(data_dict):
        #left = np.zeros(len(y_pos))
        segments = data_dict[data]['segs']

        for seg in segments:
            min_val, max_val, color = seg[0], seg[1], seg[2]
            xvals = list(range(min_val, max_val))
            yvals = [idx] * len(xvals)
            ax.barh(yvals, xvals, align='center', color=color)

    # Plot each segment as a stacked bar.
        #ax.barh(y_pos, x_vals, align='center')
    #ax.set_yticks(yvals)
    #ax.set_yticklabels(y_labels)

    plt.show()

    return


def pandas_hplot():
    df2 = pd.DataFrame([[1, 2, 3, 1],
                        [1, 21, 4, 3],
                        [1, 3, 22, 10],
                        [1, 2, 3, 4]
                        ], columns=['a', 'b', 'c', 'd'])
    df2.plot.barh(stacked=True)
    plt.show()
    return


def parse_data(fname):
    """Parse file and return a data dict."""

    stream = open(fname, 'r')

    data_dict = dict()
    for line in stream:
        line = line.strip().replace(' ', '')
        # Parse the y_value, the particular segment, and actual color used
        y_val, segments, color = line.split(',')

        segs = data_dict.get(y_val, {}).get('segs', [])

        min_val, max_val = segments.strip().split('-')

        segs.append((int(min_val), int(max_val), color))

        # Sort segments by the minimum values
        segs.sort(key=lambda x: x[0])
        # Store in dictionary keyed by y_value
        data_dict.setdefault(y_val, dict()).update({'segs': segs})

    n_segs = get_segs_count(data_dict)

    for d in data_dict:
        segs = data_dict[d]['segs']
        if len(segs) < n_segs:
            filler = [(0, 0, 'black')] * (n_segs - len(segs))
            segs += filler

        data_dict[d]['segs'] = segs

    return data_dict


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--file', type=str, dest='file', help='Files to be plotted')
    args = parser.parse_args()

    fname = args.file

    data_dict = parse_data(fname=fname)

    #horizontal_plot(data_dict=data_dict)
    #plot()
    pandas_hplot()

    print(fname, "FNAME")


if __name__ == "__main__":
    main()