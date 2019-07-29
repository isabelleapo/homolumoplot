import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class HOMOLUMOPlot:

    '''
Takes IP and EA values for multiple structures and plots the -IP and -EA in the form of an energy
level diagram, where -IP and -EA represent the HOMO and LUMO, respectively.

Parameters
----------

data_path: :class:'str'
    Path to an excel spreadsheet containing the relevant data.
    The spreadsheet must contain at least two columns with the labels 'IP' and 'EA'.

xlabels: :class:'str'
    The x-axis label and also the label assigned to the column in the Excel spreadsheet containing the structure name or number.
    e.g. 'Molecule number'

homo_colour: :class:'str'
    Any matplotlib colour

lumo_colour: :class:'str'
    Any matplotlib colour

filename: :class:'str'
    Filename plot is to be saved as

figsize: :class:'tuple'
    Figure width and height. Floats or ints in tuple.

redoxTEA: :class;'bool'
    If True, redox level for TEAR/TEA is added to plot

redoxH2: :class;'bool'
    If True, redox level for H+/H2 is added to plot
'''
    def __init__(self,
                data_path,
                xlabels,
                homo_colour = 'skyblue',
                lumo_colour = 'orange',
                filename = 'homolumoplot.png',
                figsize = (12,4),
                redoxTEA = False,
                redoxH2 = False
                ):

        self.data_path = data_path
        self.xlabels = xlabels
        self.homo_colour = homo_colour
        self.lumo_colour = lumo_colour
        self.filename = filename #string
        self.figsize = figsize #tuple
        self.redoxTEA = redoxTEA
        self.redoxH2 = redoxH2

    def plot(self):
        data = self._load_data()
        self._plot(data)

    def _plot(self, data):
        fig, ax = plt.subplots(figsize=self.figsize)


        homo_values = data['newIP']
        lumo_values = data['newEA']
        mol_number = data[self.xlabels]


        ax.bar(mol_number, homo_values, bottom=5, align='center', color=self.homo_colour)
        ax.bar(mol_number, lumo_values, bottom=-5, align='center', color=self.lumo_colour)
        ax.tick_params(axis='x',rotation=45)

        ax.set_ylabel('E / V')
        ax.set_xlabel(self.xlabels)
        sns.set()
        sns.set_style('white')

        if self.redoxH2 == True:
            ax.axhline(y=-0.68, linestyle='--', linewidth=1)
            ax.text(35.5, -0.8, r'$H^+/\ H_2$')

        if self.redoxTEA == True:
            ax.axhline(y=0.69, linestyle='--', linewidth=1)
            ax.text(34.5, 1.2, r'$TEAR\ /\ TEA$')

        plt.gca().invert_yaxis()
        plt.tight_layout()

        plt.savefig(self.filename, dpi=900)




    def _load_data(self):
        data = pd.read_excel(self.data_path)
        data['newIP'] = -5 - data['IP']*-1
        data['newEA'] = 5 - data['EA']*-1
        try:
            data = data.sort_values(self.xlabels)
        except Exception as e:
            pass
        data[self.xlabels] = data[self.xlabels].astype(str)
        return data
