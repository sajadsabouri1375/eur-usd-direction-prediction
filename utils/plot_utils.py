from matplotlib import pyplot as plt
import math
import pandas as pd
from scipy.stats import norm
import numpy as np
from sklearn import metrics

class PlotUtils:
    
    @staticmethod
    def plot_percentage_stacked(dataset, columns_to_plot, super_title, saving_address, number_of_columns):
        
        number_of_rows = math.ceil(len(columns_to_plot)/number_of_columns)

        # create a figure
        fig = plt.figure(figsize=(25.6, 14.4))
        fig.suptitle(super_title, fontsize=20)
    
        # loop to each column name to create a subplot
        for index, column in enumerate(columns_to_plot, 1):

            # create the subplot
            ax = fig.add_subplot(number_of_rows, number_of_columns, index)

            # calculate the percentage of observations of the response variable for each group of the independent variable
            # 100% stacked bar plot
            prop_by_independent = pd.crosstab(dataset[column], dataset['label']).apply(lambda x: x/x.sum() * 100, axis=1)

            p = prop_by_independent.plot(
                kind='bar',
                ax=ax,
                stacked=True,
                rot=0,
                alpha=0.5,
                color=['orangered', 'lightgray','limegreen']
            )

            for c in p.containers:
                labels = [f'{round(v.get_height())}%' if v.get_height() > 0 else '' for v in c]
                
                ax.bar_label(c, labels=labels, label_type='center')
    
            # set the legend in the upper right corner
            ax.legend(
                loc="upper right",
                title='EUR Price Change\nClass in USD',
                fancybox=True
            )
                        
            # set title and labels
            ax.set_title(
                'Proportion of Observations by ' + column,
                fontsize=20,
                loc='center'
            )

            ax.tick_params(rotation='auto')

            # eliminate the frame from the plot
            spine_names = ('top', 'right', 'bottom', 'left')
            for spine_name in spine_names:
                ax.spines[spine_name].set_visible(False)

        plt.tight_layout()        
        plt.show(block=False)
        
        plt.savefig(
            saving_address,
            dpi=300
        )
        
    @staticmethod
    def plot_histogram(series, n_bins, saving_address):
        
        plt.figure(figsize=(25.6, 14.4))
        series = series.dropna()
        mu, std = norm.fit(series)
        plt.hist(
            series, 
            n_bins,
            density=True, 
            alpha=0.6,
            color='lightgray',
            edgecolor='black'
        )
        
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, color='orangered', linewidth=2)
        
        ymin, ymax = plt.ylim()
        ppf_33 = norm.ppf(0.33, loc=mu, scale=std)
        ppf_67 = norm.ppf(0.67, loc=mu, scale=std)
        plt.plot([ppf_33, ppf_33], [ymin, ymax], color='k', linestyle='--', linewidth=3, alpha=0.5)
        plt.plot([ppf_67, ppf_67], [ymin, ymax], color='k', linestyle='--', linewidth=3, alpha=0.5)

        plt.xlabel('Close Price Daily Difference', fontsize=30)
        plt.ylabel('Density', fontsize=30)
        plt.title('Close Price Daily Differences Histogram', fontsize=30)
        plt.tight_layout()
        plt.show(block=False)
        
        plt.savefig(
            saving_address,
            dpi=300
        )
    
    @staticmethod
    def histogram_plots(dataset, columns_to_plot, super_title, saving_address, number_of_columns):
    
        number_of_rows = math.ceil(len(columns_to_plot)/number_of_columns)
        
        # create a figure
        fig = plt.figure(figsize=(25.6, 14.4))
        fig.suptitle(super_title, fontsize=20)
    
        # loop to each demographic column name to create a subplot
        for index, column in enumerate(columns_to_plot, 1):

            # create the subplot
            ax = fig.add_subplot(number_of_rows, number_of_columns, index)

            # histograms for each class (normalized histogram)
            dataset[dataset['label']==-1][column].plot(
                kind='hist',
                ax=ax,
                density=True,
                alpha=0.5,
                color='orangered',
                label='Significant Drop',
                bins=30
            )
            
            dataset[dataset['label']==0][column].plot(
                kind='hist',
                ax=ax,
                density=True,
                alpha=0.5,
                color='lightgray',
                label='Almost Constant',
                bins=30
            )
            
            dataset[dataset['label']==1][column].plot(
                kind='hist',
                ax=ax,
                density=True,
                alpha=0.5,
                color='limegreen',
                label='Significant Rise',
                bins=30
            )
            
            # set the legend in the upper right corner
            ax.legend(
                loc="upper right",
                bbox_to_anchor=(0.5, 0.5, 0.5, 0.5),
                title='EUR Price Change\nClass in USD',
                fancybox=True
            )

            # set title and labels
            ax.set_title(
                'Distribution of ' + column + ' by Price Change Class',
                fontsize=16,
                loc='center'
            )

            ax.tick_params(rotation='auto')

            # eliminate the frame from the plot
            spine_names = ('top', 'right', 'bottom', 'left')
            for spine_name in spine_names:
                ax.spines[spine_name].set_visible(False)
                
        plt.tight_layout()
        plt.show(block=False)
        
        plt.savefig(
            saving_address,
            dpi=400
        )
    
    @staticmethod
    def plot_confusion_matrix(confusion_matrix, saving_address, title):
        
        plt.figure(figsize=(25.6, 14.4))
        cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = ['Significant Drop', 'Almost Constant', 'Significant Rise'])
        cm_display.plot(cmap='Reds')
        plt.title(title, fontsize=15)
        plt.tight_layout()
        plt.show(block=False)
        plt.savefig(
            saving_address,
            dpi=400
        )