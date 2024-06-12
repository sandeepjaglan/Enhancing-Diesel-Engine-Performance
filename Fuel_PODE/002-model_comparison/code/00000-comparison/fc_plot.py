#######################################################################################################################
# Plot the results of the comparison
######################################################################################################################

#  import packages
import numpy as np
import cantera as ct
from pathlib import Path
import matplotlib.pyplot as plt
plt.style.use('stfs_2')


def plot_IDT(IDT_MLP_PV, IDT_GRM_PV, IDT_HR_PV, args):
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111)

    ax.semilogy(1000 / IDT_MLP_PV[:, 0], IDT_MLP_PV[:, 1], 'r-', label='MLP')
    ax.semilogy(1000 / IDT_GRM_PV[:, 0], IDT_GRM_PV[:, 1], 'g-', label='GRM')
    ax.semilogy(1000 / IDT_HR_PV[:, 0], IDT_HR_PV[:, 1], 'b-', label='HR')

    ax.set_ylabel('$Y_c$ at ignition')
    ax.set_xlabel('1000/T [1/K]')

    # Add a second axis on top to plot the temperature for better readability
    ax2 = ax.twiny()
    ticks = ax.get_xticks()
    ax2.set_xticks(ticks)
    ax2.set_xticklabels((1000 / ticks).round(1))
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xlabel('T [K]')

    textstr = '$\\Phi$={:.1f}\np={:.0f}bar\nPODE{}'.format(args.equivalence_ratio, args.pressure, args.pode)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top')

    # ax.set_yscale('log')
    ax.set_yticks([0.03, 0.04, 0.05, 0.06, 0.07])
    ax.set_yticklabels([0.03, 0.04, 0.05, 0.06, 0.07])

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=False, ncol=4,
              prop={'size': 14})

    plt.tight_layout()

    path = Path(__file__).resolve()
    path = path.parents[2] / 'data/00000-comparison/ID_pode{}_phi{}_p{}.pdf' \
        .format(args.pode, args.equivalence_ratio, args.pressure)
    plt.savefig(path)

    plt.show()


def plot_outputs(y_samples, y_samples_nn, samples_grm, x_samples, features, labels):
    """
    Function to plot MLP and GRM outputs next to reactor output

    :param y_samples:           - pd dataframe -    y_samples generated by HR
    :param y_samples_nn:        - np array -        corresponding output of the MLP
    :param samples_grm:         - pd dataframe -    corresponding results of the GRM
    :param x_samples:           - pd dataframe -    x_samples generated by HR
    :param features:            - list of str -     list of features
    :param labels:              - list of str -     list of labels
    """

    for i, label_run in enumerate(labels):
        if label_run == 'P':
            y_samples_run = np.squeeze(y_samples[[label_run]]) / 1.e+6
            y_samples_nn_run = np.squeeze(y_samples_nn[:, i]) / 1.e+6
            samples_grm[['P']] = samples_grm[['P']] / 10
        else:
            y_samples_run = np.squeeze(y_samples[[label_run]])
            y_samples_nn_run = np.squeeze(y_samples_nn[:, i])

        plt.figure(figsize=(9, 6))

        # plot the MLP and reactor output
        plt.plot(x_samples[['PV']], y_samples_run, 'b-', label='HR')
        plt.plot(x_samples[['PV']], y_samples_nn_run, 'r-', label='NN')
        plt.plot(samples_grm[['PV']], samples_grm[[label_run]], 'g-', label='GRM')

        samples_feature = x_samples.to_numpy()

        if len(features) == 5:
            plt.title('PODE{:.0f} {}={:.2f} {}={:.0f} {}={}bar '.format(samples_feature[0, 0],
                                                                        features[1],
                                                                        samples_feature[0, 1],
                                                                        features[2],
                                                                        samples_feature[0, 2] / ct.one_atm,
                                                                        features[3],
                                                                        samples_feature[0, 3]))

            path = Path(__file__).resolve()
            path_plt = path.parents[2] / 'data/00000-comparison/plt_{}_comp_PODE{}_{}{:.2f}_{}{:.0f}_{}{:.0f}.pdf'.\
                format(labels[i], samples_feature[0, 0], features[1], samples_feature[0, 1], features[2],
                       samples_feature[0, 2] / ct.one_atm, features[3], samples_feature[0, 3])

        else:
            plt.title('PODE{:.0f} {}={:.2f} {}={:.2f} [MJ/kg]'.format(samples_feature[0, 0],
                                                                      features[1],
                                                                      samples_feature[0, 1],
                                                                      features[2],
                                                                      samples_feature[0, 2] / 1.e+3))

            path = Path(__file__).resolve()
            path_plt = path.parents[2] / 'data/00000-comparison/plt_{}_comp_PODE{}_{}{:.2f}_{}{:.0f}.pdf'.format\
                (labels[i], samples_feature[0, 0], features[1], samples_feature[0, 1], features[2],
                 samples_feature[0, 2])

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=False, ncol=4,
                   prop={'size': 14})
        plt.xlabel('PV')
        label_unit = unit(labels[i])
        plt.ylabel('{}'.format(label_unit))

        plt.tight_layout()

        plt.savefig(path_plt)

        plt.show()


def unit(label):
    """ Corresponding unit for the selected label

    :parameter
    :param label:       - str -             label

    :returns:
    :return label_unit: - str -             label with corresponding unit
    """

    if label == 'P':
        label_unit = 'P [MPa]'
    elif label == 'T':
        label_unit = 'T [K]'
    elif label == 'HRR':
        label_unit = "HRR [W/$m^3$]"
    else:
        label_unit = 'Y_{}'.format(label)

    return label_unit
