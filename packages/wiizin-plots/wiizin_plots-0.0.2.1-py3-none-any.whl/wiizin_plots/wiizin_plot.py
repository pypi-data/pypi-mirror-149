import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

def basic_info(data):
    print(data.info())
    print('\033[1m''\n -------------------------------------------- \n' + '\033[0m')
    print(f'Number of Rows: {data.shape[0]}')
    print(f'Number of Columns: {data.shape[1]}')
    print('\033[1m''\n -------------------------------------------- \n' + '\033[0m')
    print(f'MISSING VALUES:')
    print(data.isnull().sum())
    print('\033[1m''\n -------------------------------------------- \n' + '\033[0m')
    print(f'DUPLICATED VALUES:')
    print(data.duplicated().sum())


def get_cat_num_variables(data, threshold = 15):
    cat_cols = []
    num_cols = []
    for col in data.columns:
        if data[col].nunique() > threshold :
            num_cols.append(col)
        else:
            cat_cols.append(col)
    
    return cat_cols, num_cols


def eda_class_plot(data, target, threshold = 15):
    print('\033[1m''TARGET VARIABLE' + '\033[0m')
    if data[target].nunique() <= threshold:
        plt.figure(figsize = (15,6))
        ax = sns.countplot(data[target])
        for p in ax.patches:
            height = p.get_height()
            width = p.get_width()
            ax.text(x = p.get_x()+(p.get_width()/2), y = height*1.02, s = height, ha = 'center')
        plt.show()
        
    
    print('\033[1m''\n -------------------------------------------- \n' + '\033[0m')
    print('\033[1m'+'CATEGORICAL EDA' + '\033[0m')
    
    cat_cols, num_cols = get_cat_num_variables(data, threshold)
    for col in cat_cols:
        if data[col].nunique() <= threshold:
            g = sns.catplot(x = col, kind='count', col = target, data=data, sharey=False)
            g.set_xticklabels(rotation=60)
            for i in range(data[target].nunique()):
                number_rows = data[data[target] == data[target].unique()[i]].shape[0]
                ax = g.facet_axis(0,i)
                for p in ax.patches:
                    height = p.get_height()
                    ax.text(x = p.get_x()+(p.get_width()/2), y =height * 1.02 , s = '{:.1f}%'.format(height/number_rows*100), ha = 'center')
            plt.show()
            
    print('\033[1m''\n -------------------------------------------- \n' + '\033[0m')
    print('\033[1m''NUMERICAL EDA' + '\033[0m')
    
    for col in num_cols:
        
        try:
            plt.figure(figsize = (15,6))

            max_value = data[col].max()
            min_value = data[col].min()
            delta = (max_value - min_value)/threshold
            intervals = []

            for i in range(threshold+1):
                intervals.append(min_value + delta*(i))

            for i in range(len(data[target].unique())):
                plt.subplot(1, len(data[target].unique()), i + 1)
                data_new = data[data[target] == data[target].unique()[i]]
                g = sns.countplot(pd.cut(data_new[col], intervals))
                plt.xticks(rotation = 90)
                plt.title(f'{target}: {data[target].unique()[i]}')
                for p in g.patches:
                    n_rows = data_new.shape[0]
                    height = p.get_height()
                    g.text(x = p.get_x()+(p.get_width()/2), y = height * 1.02 , s = '{:.1f}%'.format(height*100/n_rows), ha = 'center',
                          fontsize = 8)

            plt.show()
        except:
            print('\033[1m'+'NÃO FOI POSSIVEL PLOTAR A VARIAVEL '+ col + '\033[0m')

    
    for col in num_cols:
        try:
            plt.figure(figsize = (15,6))
            sns.boxplot(x = data[col], y = data[target].apply(str), showmeans = True)
        except:
            print('\033[1m'+'NÃO FOI POSSIVEL PLOTAR A VARIAVEL '+ col + '\033[0m')


def eda_reg_plot(data, target, threshold = 15):
    print('\033[1m''TARGET VARIABLE' + '\033[0m')
    if data[target].nunique() >= threshold:
        plt.figure(figsize = (15,6))
        sns.distplot(data[target])
    
    cat_cols, num_cols = get_cat_num_variables(data, threshold)
    
    print('\033[1m''\n -------------------------------------------- \n' + '\033[0m')
    print('\033[1m'+'CATEGORICAL EDA' + '\033[0m')
    
    for col in cat_cols:
        try:
            plt.figure(figsize = (15,12))

            max_value = data[target].max()
            min_value = data[target].min()
            delta = (max_value - min_value)/threshold
            intervals = []

            for i in range(threshold+1):
                intervals.append(min_value + delta*(i))

            for i in range(len(data[col].unique())):
                plt.subplot(1, len(data[col].unique()), i + 1)
                data_new = data[data[col] == data[col].unique()[i]]
                g = sns.countplot(pd.cut(data_new[target], intervals))
                plt.xticks(rotation = 90)
                plt.title(f'{col}: {data[col].unique()[i]}')
                for p in g.patches:
                    n_rows = data_new.shape[0]
                    height = p.get_height()
                    g.text(x = p.get_x()+(p.get_width()/2), y = height * 1.02 , s = '{:.1f}%'.format(height*100/n_rows), ha = 'center',
                          fontsize = 8)

            plt.show()
        except:
            print('\033[1m'+'NÃO FOI POSSIVEL PLOTAR A VARIAVEL '+ col + '\033[0m')
            
    for col in cat_cols:
        plt.figure(figsize = (15,6))
        sns.boxplot(x = data[target], y = data[col].apply(str) , showmeans = True)
        plt.show()
    
    
    print('\033[1m''\n -------------------------------------------- \n' + '\033[0m')
    print('\033[1m'+'Numerical EDA' + '\033[0m')
    
    for col in num_cols:
        try:
            plt.figure(figsize = (15,6))
            sns.scatterplot(x = data[col], y = data[target])
            plt.show()
        except:
            print('\033[1m'+'NÃO FOI POSSIVEL PLOTAR A VARIAVEL '+ col + '\033[0m')


def best_interval(data, target, threshold = 15):
    cat_cols, num_cols = get_cat_num_variables(data, threshold)
    for col in num_cols:
        plt.figure(figsize = (15,6))
        
        max_value = data[col].max()
        min_value = data[col].min()
        delta = (max_value - min_value)/threshold
        intervals = []

        for i in range(threshold+1):
            intervals.append(min_value + delta*(i))
        
        data_1 = data[data[target] == data[target].unique()[0]]
        data_2 = data[data[target] == data[target].unique()[1]]
        
        data_1_cut = pd.cut(data_1[col], intervals).value_counts(normalize = True)
        data_2_cut = pd.cut(data_2[col], intervals).value_counts(normalize = True)
        
        dif_data = abs(data_1_cut - data_2_cut)
        sns.barplot(y = dif_data, x = dif_data.index)
        plt.xticks(rotation = 90)
        plt.title(col)
        plt.show()