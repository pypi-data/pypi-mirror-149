import pandas as pd
import os
from tkinter.filedialog import askdirectory, askopenfilenames
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import RangeSlider, Button
import seaborn as sns
from tqdm import tqdm

matplotlib.use('TkAgg')
sns.set()
sns.set_color_codes()


def evaluate_raw_data(cols=None, normalize=False):
    """Reads excel or csv files, calculates cyclic data and saves as excel to be imported later.

    Keyword arguments:
        normalize           -- True/False whether to set the first entry as 0 or not. Default is False
        cols                -- Columns of file that map to the data representing:
                            ['Total Time (s)', 'Elapsed Cycles', 'Strain (%)', 'Stress (MPa)']
                            Default concerning the data at the chair of metal structures is [0,3,8,10]

        """
    if cols is None:
        cols = [0, 3, 8, 10]
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

        filename = os.path.splitext(os.path.basename(file))[0]
        Data.to_excel(savedirectory + os.sep + filename + '_cleaned.xlsx')


def evaluate_stable_zone(save=True, dpi=500, filetype='pdf'):
    """Reads cleaned excel files and graphically determines the stable cyclic zones.

    Keyword arguments:
        save                -- True/False decide whether to save the final plot as a pdf
        dpi                 -- Dpi to save figure with. Int Value.
        filetype            -- specify filetype as one of the following:
                                    - 'pdf' --> Default
                                    - 'png'
                                    - 'ps'
                                    - 'eps'
                                    - 'svg'

        """
    if filetype not in ['png', 'pdf', 'ps', 'eps', 'svg']:
        print('Filetype not in list\n run "help(rambergosgood)" for details.')
        return

    filepaths = askopenfilenames(filetypes=[("Excel Files", '*.xlsx')], title='Which files shall be evaluated?')
    savedirectory = askdirectory(title='Where to save the results?')

    for file in tqdm(filepaths):
        Data = pd.read_excel(file, engine='openpyxl')
        Data["Stable"] = 'Stable'

        fig, ax = plt.subplots(figsize=(16, 9))
        plt.subplots_adjust(bottom=0.25)

        slider_ax = plt.axes([0.20, 0.1, 0.60, 0.03])
        slider = RangeSlider(ax=slider_ax, label="Stable Zone", valmin=1, valmax=Data["Elapsed Cycles"].max(),
                             valstep=1, valfmt='%0.0f', valinit=(0, Data["Elapsed Cycles"].max()))

        donebuttonax = plt.axes([0.8, 0.025, 0.1, 0.04])
        button = Button(donebuttonax, 'Done', hovercolor='0.975')

        ax.scatter(Data['Elapsed Cycles'], Data['Stress Amplitude (MPa)'], color='b', label='stable')
        ax.set_xlabel('Elapsed Cycles →')
        ax.set_ylabel('Stress Amplitude in MPa →')
        ax.legend(loc='upper right')
        ax.set_title('Stable Zone')

        def update(val):
            matplotlib.axes.Axes.clear(ax)
            # Left part
            ax.scatter(Data.loc[Data['Elapsed Cycles'] < int(val[0])]['Elapsed Cycles'],
                       Data.loc[Data['Elapsed Cycles'] < int(val[0])]['Stress Amplitude (MPa)'], color='r')
            # Middle part
            ax.scatter(
                Data.loc[Data['Elapsed Cycles'].between(int(val[0]), int(val[1]), inclusive='both')]['Elapsed Cycles'],
                Data.loc[Data['Elapsed Cycles'].between(int(val[0]), int(val[1]), inclusive='both')][
                    'Stress Amplitude (MPa)'], color='b', label='stable')
            # Right Part
            ax.scatter(Data.loc[Data['Elapsed Cycles'] > int(val[1])]['Elapsed Cycles'],
                       Data.loc[Data['Elapsed Cycles'] > int(val[1])]['Stress Amplitude (MPa)'], color='r',
                       label='unstable')
            ax.set_xlabel('Elapsed Cycles →')
            ax.set_ylabel('Stress Amplitude in MPa →')
            ax.set_title('Stable Zone')
            ax.legend(loc='upper right')
            ax.set_title('Stable Zone')

            fig.canvas.draw()

        def finished(event):
            Data.loc[Data["Elapsed Cycles"] < int(slider.val[0]), 'Stable'] = 'Unstable'
            Data.loc[Data["Elapsed Cycles"] > int(slider.val[1]), 'Stable'] = 'Unstable'

            filename = os.path.splitext(os.path.basename(file))[0]

            Data.to_excel(savedirectory + os.sep + filename + '_evaluated.xlsx', index=False)
            if save:
                plt.savefig(savedirectory + os.sep + filename + '_evaluated.' + filetype, dpi=dpi)
            plt.close(fig)

        slider.on_changed(update)
        button.on_clicked(finished)
        plt.show()
