from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os
import math
from itertools import combinations

def make_boxplots(data, groups, output_dirs):

    # data is a list where each element is a combined replicate_output

    # find all columns that we want to plot
    plotted_columns = [col for col in data[0].columns if 'partition' in col] + ["area", "circularity"]
    for plotted_column_name in plotted_columns:
        plot_data = [d[plotted_column_name] for d in data]
        # groups = [np.unique(g['sample']) for g in data]
	    # groups = [item for items in groups for item in items]

        fig, ax = plt.subplots()

        for i in range(len(groups)):
            y = plot_data[i]
            if len(y) < 1 or y.empty:
                y = [0.0]
                x = 1 + i
                plot_data[i] = [0.0]
            else:
                x = np.random.normal(1 + i, 0.04, size=len(y))

            ax.plot(x, y, 'b.', markersize=8, markeredgewidth=0, alpha=0.3)


        ax.boxplot(plot_data, labels=groups, showfliers=False)

        plt.xticks(rotation=45, ha='right')

        plt.ylim(bottom=0)
        plt.ylabel(plotted_column_name)

        plt.tight_layout()

        plt.savefig(os.path.join(output_dirs['output_individual'], plotted_column_name + '_boxplot.png'), dpi=300, format='png')
        plt.savefig(os.path.join(output_dirs['output_individual'], plotted_column_name + '_boxplot.pdf'), format='pdf')
        plt.close()


def make_droplet_size_histogram(sample_name, data, output_dirs, input_args):
    size_data = data['area'].tolist()

    fig, ax = plt.subplots()
    if len(size_data) > 0:
        ax.hist(size_data, bins=50, density=True)

    plt.title(sample_name)

    plt.ylabel('Fraction of total')
    plt.xlabel('Droplet area')
    plt.axis('tight')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dirs['output_individual'], sample_name + '_droplet_size_histogram.png'), dpi=300, format='png')
    plt.savefig(os.path.join(output_dirs['output_individual'], sample_name + '_droplet_size_histogram.pdf'), format='pdf')
    plt.close()


def make_droplet_intensity_scatter(sample_name, data, output_dirs, input_params):
    # for now, we only support this feature for 2 channels because it will be hard-coded
    mean_intensity_cols = [col for col in data.replicate_output.columns if 'mean' in col]
    rep_data = data.replicate_output
    for pair in combinations(mean_intensity_cols, 2):
        channel_a_name = pair[0][pair[0].find('ch') : pair[0].find('ch') + 5]
        channel_b_name = pair[1][pair[1].find('ch') : pair[1].find('ch') + 5]

        channel_a = rep_data[pair[0]]
        channel_b = rep_data[pair[1]]

        fig, ax = plt.subplots()
        ax.plot(channel_a, channel_b, 'b.', markersize=5, markeredgewidth=0, alpha=0.3)

        plt.ylabel(pair[1])
        plt.xlabel(pair[0])
        plt.title(sample_name)
        plt.axis('tight')

        plt.tight_layout()

        plt.savefig(os.path.join(output_dirs['output_individual'], sample_name + '_' + channel_a_name + '_' + channel_b_name + '_droplet_intensity_scatter.png'), dpi=300,
                    format='png')
        plt.savefig(os.path.join(output_dirs['output_individual'], sample_name + '_' + channel_a_name + '_' + channel_b_name + '_droplet_intensity_scatter.pdf'),
                    format='pdf')
        plt.close()

def make_average_sample_graph(data, output_dirs, input_args):

    # partition ratio graph
    pr_cols = [col for col in data.columns if 'partition_ratio_mean' in col]

    for p in pr_cols:
        fig, ax = plt.subplots()
        for i, s in enumerate(data['sample']):
            ax.errorbar(x=i+1, y=data[p][data['sample'] == s], yerr=data[p.replace('_mean_', '_std_')][data['sample'] == s],
                        fmt='bo', capsize=20, markersize=10)

        plt.ylabel(p)
        plt.xlim(0, len(data.index) + 1)
        # plt.ylim(bottom=1, top=math.floor(np.max(data[p]) + 1))
        plt.ylim(bottom=1)
        x_labels = data['sample'].tolist()
        plt.xticks(list(range(1, len(data.index)+1)), x_labels, rotation=45, ha='left')

        plt.tight_layout()
        plt.savefig(os.path.join(output_dirs['output_summary'], p + '_average.png'),
                    dpi=300,
                    format='png')
        plt.savefig(os.path.join(output_dirs['output_summary'], p + '_average.pdf'),
                    format='pdf')
        plt.close()

    # condensed fraction graph
    cf_cols = [col for col in data.columns if 'condensed_fraction_mean' in col]

    for c in cf_cols:
        fig, ax = plt.subplots()
        for i, s in enumerate(data['sample']):
            ax.errorbar(x=i + 1, y=data[c][data['sample'] == s],
                        yerr=data[c.replace('_mean_', '_std_')][data['sample'] == s],
                        fmt='bo', capsize=20, markersize=10)

        plt.ylabel(c)
        plt.xlim(0, len(data.index) + 1)
        plt.ylim(bottom=0)
        x_labels = data['sample'].tolist()
        plt.xticks(list(range(1, len(data.index) + 1)), x_labels)

        plt.savefig(os.path.join(output_dirs['output_summary'], c + '_average.png'),
                    dpi=300,
                    format='png')
        plt.savefig(os.path.join(output_dirs['output_summary'], c + '_average.pdf'),
                    format='eps')
        plt.close()


def make_droplet_count_histogram(graph_input, sample_list, output_dirs):
    droplet_counts = list()
    for sample_group in graph_input:
        droplet_counts.append(len(sample_group))
    x_values = list(range(len(sample_list)))

    fig, ax = plt.subplots()
    ax.bar(x_values, droplet_counts, width=1)
    ax.set_xlim(-0.5, max(6, len(x_values)) + 0.5)
    ax.set_ylim(bottom=0)
    ax.set_xticks(x_values, sample_list, rotation=45, ha='left')
    ax.set_ylabel("Droplet count")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dirs['output_summary'], 'droplet_count_histogram.png'),
                dpi=300, format='png')
    plt.savefig(os.path.join(output_dirs['output_summary'], 'droplet_count_histogram.pdf'))
    plt.close()