import numpy as np
import pandas as pd
import os
from tkinter.filedialog import askdirectory, askopenfilenames
import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm
import seaborn as sns

matplotlib.use('TkAgg')


def plot_cycles_stress(normalizecycles=False, figurewidth='nature-doublecolumn', figureheight=None,
                       plotstyle='seaborn-deep',
                       figurestyle='whitegrid', axisunitstyle='arrow', title=None, dpi=500, filetype='pdf',
                       savedata=False,
                       usestablezonedata=True, logx=True):
    """Reads multiple evaluated excel files, calculates mean amplitudes, then fits Ramberg Osgood equation to the
    amplitudes and returns a fitting plot.

    Keyword arguments:
        normalizecycles     -- If True normalizes the Cycles of every sample between 0 and 1. Default is False.
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
                                    - 'seaborn-deep' --> Default
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
        filetype            -- specify filetype as one of the following:
                                    - 'pdf' --> Default
                                    - 'png'
                                    - 'ps'
                                    - 'eps'
                                    - 'svg'
        savedata            -- True/False whether to save the Dataframe as Excel file.
        usestablezonedata   -- True/False whether the evaluation from fileevaluator() should be used.
        logx                -- True/False whether to set the x-axis scale to logarithmic.

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
        print('Figure style not in list\n run "help(rambergosgood)" for details.')
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

    Data = pd.DataFrame()

    for file in filepaths:
        Samplename = os.path.splitext(os.path.basename(file))[0]
        if Samplename.endswith('_cleaned_evaluated'):
            Samplename = Samplename[:-18]
        elif Samplename.endswith('_cleaned'):
            Samplename = Samplename[:-8]

        temp = pd.read_excel(file, engine='openpyxl')

        if 'Stable' in temp.columns and usestablezonedata:
            temp = temp.iloc[:int(temp.index[temp['Stable'] == 'Stable'].tolist()[-1]), :]
        elif 'Stable' in temp.columns and not usestablezonedata:
            print('Stable zone data is present, but not used.')
        else:
            print('This Excel file has not yet been evaluated by fileevaluator().')
        temp.insert(0, 'Sample', Samplename)
        if normalizecycles:
            temp['Elapsed Cycles'] = temp['Elapsed Cycles'].divide(temp['Elapsed Cycles'].max())
        Data = pd.concat([Data, temp])

    colormap = sns.color_palette(plotstyles[plotstyle], n_colors=len(Data['Sample'].unique()))

    Data.reset_index(drop=True, inplace=True)
    plt.figure(figsize=figsize)
    sns.lineplot(data=Data, x='Elapsed Cycles', y='Stress Max (MPa)', hue='Sample', palette=colormap)
    sns.lineplot(data=Data, x='Elapsed Cycles', y='Stress Min (MPa)', hue='Sample', palette=colormap, legend=False)

    if logx and not normalizecycles:
        plt.xscale('log')
    if title is not None and isinstance(title, str):
        plt.title(title)
    else:
        plt.title('Elapsed Cycles - Stress')

    titles = Data.groupby("Sample")['Strain Amplitude (%)'].median()
    Legends = []
    for title in titles:
        Legends.append(r"$\varepsilon_a$ = {:10.1f} %".format(title))
    order = titles.reset_index().sort_values(by=["Strain Amplitude (%)"]).index.tolist()
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend(labels=[Legends[idx] for idx in order], handles=[handles[idx] for idx in order],
               title='Strain Amplitude', loc='center left')

    if axisunitstyle == 'square-brackets':
        plt.xlabel('Elapsed Cycles [-]')
        plt.ylabel('Stress [MPa]')
    elif axisunitstyle == 'round-brackets':
        plt.xlabel('Elapsed Cycles (-)')
        plt.ylabel('Stress (MPa)')
    else:
        plt.xlabel('Elapsed Cycles →')
        plt.ylabel('Stress in MPa →')

    plt.tight_layout()
    plt.savefig(savedirectory + os.sep + 'cycles-stress.' + filetype, dpi=dpi)
    plt.show()

    if savedata:
        Data.to_excel(savedirectory + os.sep + 'Plot-Cycles-Stress.xlsx', index=False)


def plot_hystereses(Cycles=None, useabsolutecycles=False, figurewidth='nature-doublecolumn', figureheight=None,
                    plotstyle='seaborn-deep',
                    figurestyle='whitegrid', axisunitstyle='arrow', title=None, dpi=500, filetype='pdf', cols=None,
                    normalize=False):
    """Reads multiple evaluated excel files, calculates mean amplitudes, then fits Ramberg Osgood equation to the
    amplitudes and returns a fitting plot.

    Keyword arguments:
        Cycles              -- List of Normalized cycles to plot the respective hystereses.
                                Will never plot the last, therefore the failing, cycle.
                                Defaults to [0.0, 0.25, 0.5, 0.75, 1.0]. Accepts:
                                    - numpy.array()
                                    - List
        figurewidth         -- Width of figure. Float value in cm or one of the following:
                                    - 'nature-singlecolumn'
                                    - 'nature-oneandhalfcolumn'
                                    - 'nature-doublecolumn'
                                    - 'elsevier-minimal' --> Default
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
        filetype            -- specify filetype as one of the following:
                                    - 'pdf' --> Default
                                    - 'png'
                                    - 'ps'
                                    - 'eps'
                                    - 'svg'
        cols                -- Columns of file that map to the data representing:
                            ['Total Time (s)', 'Elapsed Cycles', 'Strain (%)', 'Stress (MPa)']
                            Default concerning the data at the chair of metal structures is [0,3,8,10]
        normalize           -- True/False whether to set the first entry as 0 or not. Default is False

        """
    if Cycles is None:
        Cycles = [0.0, 0.25, 0.5, 0.75, 1.0]
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

    if cols is None:
        cols = [0, 3, 8, 10]

    sns.set_context('notebook')

    filepaths = askopenfilenames(filetypes=[("Excel and CSV Files", '*.csv *.xlsx *.xls')], title='Which files shall '
                                                                                                  'be evaluated?')
    savedirectory = askdirectory(title='Where to save the results?')

    for file in tqdm(filepaths):

        if file.endswith(".csv"):
            rawdata = pd.read_csv(file, usecols=cols)
        elif file.endswith(".xlsx"):
            rawdata = pd.read_excel(file, usecols=cols, engine='openpyxl')
        else:
            raise ValueError("Invalid file")

        rawdata.columns = ['Total Time (s)', 'Elapsed Cycles', 'Strain (%)', 'Stress (MPa)']
        if normalize:
            epsilonzero = rawdata['Strain (%)'][0]
            sigmazero = rawdata['Stress (MPa)'][0]

            rawdata['Strain (%)'] = rawdata['Strain (%)'].subtract(epsilonzero)
            rawdata['Stress (MPa)'] = rawdata['Stress (MPa)'].subtract(sigmazero)

        Data = pd.concat([rawdata.groupby('Elapsed Cycles')[['Strain (%)', 'Stress (MPa)']].min(),
                          rawdata.groupby('Elapsed Cycles')[['Strain (%)', 'Stress (MPa)']].max()], axis=1)

        Data.columns = ['Strain Min (%)', 'Stress Min (MPa)', 'Strain Max (%)', 'Stress Max (MPa)']

        Data[['Strain Max (%)', 'Strain Min (%)']] = Data[['Strain Max (%)', 'Strain Min (%)']].multiply(100)
        Data['Strain Amplitude (%)'] = (Data['Strain Max (%)'] - Data['Strain Min (%)']) / 2
        Data['Stress Amplitude (MPa)'] = (Data['Stress Max (MPa)'] - Data['Stress Min (MPa)']) / 2

        colormap = sns.color_palette(plotstyles[plotstyle], n_colors=len(Cycles)).as_hex()
        maxcycles = rawdata['Elapsed Cycles'].max()
        rawdata['Strain (%)'] = rawdata['Strain (%)'].multiply(100)
        plt.figure(figsize=figsize)

        for index, cycle in enumerate(Cycles):
            cycleindex = np.ceil(cycle * maxcycles)
            if cycle == 1.0:
                cycleindex = np.ceil(cycle * maxcycles) - 1
            elif cycle == 0.0:
                cycleindex = 1.0

            cycleframe = rawdata.loc[rawdata['Elapsed Cycles'] == cycleindex]
            stressamplitude = Data.loc[cycleindex]['Stress Amplitude (MPa)']
            if useabsolutecycles:
                plt.plot(cycleframe['Strain (%)'], cycleframe['Stress (MPa)'], color=colormap[index],
                         label=f'Cycle = {cycleindex:.0f},\n' + f'$\sigma_a$      = {stressamplitude:.2f}')
            else:
                plt.plot(cycleframe['Strain (%)'], cycleframe['Stress (MPa)'], color=colormap[index],
                         label=f'Cycle = {cycleindex * 100 / maxcycles:.1f} %,\n' + f'$\sigma_a$      = {stressamplitude:.2f}')

        plt.legend(loc='upper left')
        if axisunitstyle == 'square-brackets':
            plt.xlabel('Strain [%]')
            plt.ylabel('Stress [MPa]')
        elif axisunitstyle == 'round-brackets':
            plt.xlabel('Strain (%)')
            plt.ylabel('Stress (MPa)')
        else:
            plt.xlabel('Strain in % →')
            plt.ylabel('Stress in MPa →')

        strainamplitude = Data['Strain Amplitude (%)'].mean()
        if title is not None and isinstance(title, str):
            plt.title(f'{title}\n$\epsilon_a = {strainamplitude:.1f}$ %')
        else:
            plt.title(f'Hystereses\n$\epsilon_a = {strainamplitude:.1f}$ %')

        plt.tight_layout()
        filename = os.path.splitext(os.path.basename(file))[0]
        plt.savefig(savedirectory + os.sep + filename + '_Hystereses.' + filetype, dpi=dpi)
        plt.show()
