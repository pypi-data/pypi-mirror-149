import numpy as np
import pandas as pd
import os
from tkinter.filedialog import askdirectory, askopenfilenames
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit

matplotlib.use('TkAgg')


def fit_ramberg_osgood(YoungsModulus, threshold=None, figurewidth='nature-doublecolumn',
                       figureheight=None, plotstyle='seaborn-deep', figurestyle='whitegrid', axisunitstyle='arrow',
                       title=None, dpi=500, hue=True, filetype='pdf', savedata=False):
    """Reads multiple evaluated excel files, calculates mean amplitudes, then fits Ramberg Osgood equation to the
    amplitudes and returns a fitting plot.

    Keyword arguments:
        YoungsModulus       -- YoungsModulus of the material. Float value in MPa.
        threshold           -- float between 0.0 and 1.0 depicting at what percentage of all Elapsed Cylcles
                               to start the stable zone. Beware of logic errors, when the end of the stable zone
                               falls before the start of the stable zone by using a too high threshold variable.
                               Will default to the previously determined stable zone if this error is encountered.
        figurewidth         -- Width of figure. Float value in cm or one of the following:
                                    - 'nature-singlecolumn'
                                    - 'nature-oneandhalfcolumn'
                                    - 'nature-doublecolumn' --> Default
                                    - 'elsevier-minimal'
                                    - 'elsevier-singlecolumn'
                                    - 'elsevier-oneandhalfcolumn'
                                    - 'elsevier-doublecolumn'
                                    - 'science-singlecolumn'
                                    - 'science-doublecolumn'
                               Defaults to 'nature-singlecolumn'
        figureheight        -- Height of figure. Float value in cm. Defaults to value of figurewidth.
        plotstyle           -- Style of plot. One of the following:
                                    - 'seaborn-default' --> Default
                                    - 'seaborn-colorblind'
                                    - 'seaborn-rocket'
                                    - 'seaborn-crest'
                                    - 'seaborn-spectral'
                                    - 'red-blue'
        figurestyle         -- Seaborn figure Style. One of the following:
                                    - 'whitegrid' --> Default
                                    - 'white'
                                    - 'darkgrid'
                                    - 'dark'
                                    - 'ticks'
        axisunitstyle       -- Style to plot the axis label with. One of the following:
                                    - 'arrow' equates to 'Measurement in Unit →' --> Dafault
                                    - 'square-brackets' equates to 'Measurement [Unit]
                                    - 'round-brackets' equates to 'Measurement (Unit)'
        title               -- Title for the resulting plot.
        dpi                 -- Dpi to save figure with. Int Value.
        hue                 -- True/False whether to uniquely identify the samples in the legend
        filetype            -- specify filetype as one of the following:
                                    - 'pdf' --> Default
                                    - 'png'
                                    - 'ps'
                                    - 'eps'
                                    - 'svg'
        savedata            -- True/False wheter to save the Dataframe as Excel file

        """
    figurewidths = {'nature-singlecolumn': 8.9,
                    'nature-oneandhalfcolumn': 12,
                    'nature-doublecolumn': 18.3,
                    'elsevier-minimal': 3,
                    'elsevier-singlecolumn': 9,
                    'elsevier-oneandhalfcolumn': 14,
                    'elsevier-doublecolumn': 19,
                    'science-singlecolumn': 5.5,
                    'science-doublecolumn': 12}
    plotstyles = {'seaborn-deep': 'deep',
                  'seaborn-colorblind': 'colorblind',
                  'seaborn-rocket': 'rocket',
                  'seaborn-crest': 'crest',
                  'seaborn-spectral': 'Spectral',
                  'red-blue': ['r']}

    if figurestyle not in ['whitegrid', 'white', 'darkgrid', 'dark', 'ticks']:
        print('Figure style not in list\n run "help(rambergosgood)" for details')
        return
    sns.set_style(figurestyle)
    if filetype not in ['png', 'pdf', 'ps', 'eps', 'svg']:
        print('Filetype not in list\n run "help(rambergosgood)" for details')
        return

    if figurewidth not in ['nature-singlecolumn', 'nature-oneandhalfcolumn', 'nature-doublecolumn', 'elsevier-minimal',
                           'elsevier-singlecolumn', 'elsevier-oneandhalfcolumn', 'elsevier-doublecolumn',
                           'science-singlecolumn',
                           'science-doublecolumn'] and not np.issubdtype(type(figurewidth), np.number):
        print('Figurewidth not in list\n run "help(rambergosgood)" for details')
        return
    elif figurewidth not in ['nature-singlecolumn', 'nature-oneandhalfcolumn', 'nature-doublecolumn',
                             'elsevier-minimal',
                             'elsevier-singlecolumn', 'elsevier-oneandhalfcolumn', 'elsevier-doublecolumn',
                             'science-singlecolumn',
                             'science-doublecolumn'] and np.issubdtype(type(figurewidth), np.number):
        width = figurewidth
    else:
        width = figurewidths[figurewidth]

    if figureheight is None:
        figsize = (width / 2.54, width / 2.54)
    else:
        figsize = (width / 2.54, figureheight / 2.54)

    sns.set_context('notebook')

    filepaths = askopenfilenames(filetypes=[("Excel Files", '*.xlsx')], title='Which files shall be evaluated?')
    savedirectory = askdirectory(title='Where to save the results?')

    stressamplitudes, strainamplitudes = np.zeros(len(filepaths)), np.zeros(len(filepaths))

    for index, file in enumerate(filepaths):
        Sample = pd.read_excel(file, engine='openpyxl')

        if threshold is not None:
            lower = int(np.ceil(np.multiply(threshold, Sample['Elapsed Cycles'].max())))
            higher = int(Sample.index[Sample['Stable'] == 'Stable'].tolist()[-1])
            strainamplitudes[index] = np.mean(Sample.iloc[lower:higher, :]['Strain Amplitude (%)'])
            stressamplitudes[index] = np.mean(Sample.iloc[lower:higher, :]['Stress Amplitude (MPa)'])
            if not np.isfinite(stressamplitudes[index]) \
                    or not np.isfinite(strainamplitudes[index]) \
                    or np.isclose(0, stressamplitudes[index]) \
                    or np.isclose(0, strainamplitudes[index]):
                print(f'Error encountered for: {os.path.splitext(os.path.basename(file))[0]}'
                      f'\nMean of stable stress or strain is 0, inf or NaN, because threshold > end of stable zone'
                      '\nDefault calculation method used.')
                strainamplitudes[index] = np.mean(Sample.loc[Sample['Stable'] == 'Stable']['Strain Amplitude (%)'])
                stressamplitudes[index] = np.mean(Sample.loc[Sample['Stable'] == 'Stable']['Stress Amplitude (MPa)'])

        else:
            strainamplitudes[index] = np.mean(Sample.loc[Sample['Stable'] == 'Stable']['Strain Amplitude (%)'])
            stressamplitudes[index] = np.mean(Sample.loc[Sample['Stable'] == 'Stable']['Stress Amplitude (MPa)'])

    Samples = [os.path.splitext(os.path.basename(file))[0][:-18] for file in filepaths]
    Data = pd.DataFrame({'Samples': Samples,
                         'Strain Amplitude [%]': strainamplitudes,
                         'Stress Amplitude [MPa]': stressamplitudes})

    def rambergosgoodfunction(stressamplitudes, K, n):
        return (np.divide(stressamplitudes, YoungsModulus) + pow(np.divide(stressamplitudes, K), np.divide(1, n))) * 100

    c, cov = curve_fit(rambergosgoodfunction, stressamplitudes, strainamplitudes, maxfev=100000)
    # Strain Amplitude has to be in absolute unit

    stressplot = np.linspace(0, 1.05 * Data['Stress Amplitude [MPa]'].max(), 10000)
    strainplot = rambergosgoodfunction(stressplot, c[0], c[1])
    # Transformation from absolute to percentage strain
    colormap = sns.color_palette(plotstyles[plotstyle], n_colors=len(Data) + 1)
    if plotstyle == 'red-blue':
        hue = False
        del colormap[0]
    elif plotstyle in ['seaborn-deep', 'seaborn-colorblind']:
        del colormap[0]
    else:
        del colormap[0]

    plt.figure(figsize=figsize)
    if hue:
        sns.scatterplot(data=Data, x='Strain Amplitude [%]', y='Stress Amplitude [MPa]', hue='Samples',
                        palette=colormap)
        plt.plot(strainplot, stressplot, label=f'ramberg-osgood\nK = {c[0]:.2f}\nn = {c[1]:.2f}',
                 color='b')
    else:
        sns.scatterplot(data=Data, x='Strain Amplitude [%]', y='Stress Amplitude [MPa]', label='Samples',
                        color=colormap[0])
        plt.plot(strainplot, stressplot, label=f'ramberg-osgood\nK = {c[0]:.2f}\nn = {c[1]:.2f}',
                 color='b')

    if axisunitstyle == 'square-brackets':
        plt.xlabel('Strain [%]')
        plt.ylabel('Stress [MPa]')
    elif axisunitstyle == 'round-brackets':
        plt.xlabel('Strain (%)')
        plt.ylabel('Stress (MPa)')
    else:
        plt.xlabel('Strain in % →')
        plt.ylabel('Stress in MPa →')

    plt.legend(loc='center right')
    if title is not None and isinstance(title, str):
        plt.title(title)
    else:
        plt.title('Ramberg-Osgood Curve Fit')
    plt.tight_layout()

    plt.savefig(savedirectory + os.sep + 'Ramberg-Osgood-fit.' + filetype, dpi=dpi)
    if savedata:
        Data.to_excel(savedirectory + os.sep + 'Ramberg-Osgood_curve_fit.xlsx', index=False)
    plt.show()
