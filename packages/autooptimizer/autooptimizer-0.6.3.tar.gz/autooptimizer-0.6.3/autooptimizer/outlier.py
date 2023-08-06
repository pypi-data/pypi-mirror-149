import numpy as np
import matplotlib.pyplot as plt

def interquartile_outlier_removal(array):
    Q1 = np.quantile(array, 0.25)
    Q3 = np.quantile(array, 0.75)
    IQR = Q3 - Q1
    lower_extreme = Q1 - (1.5 * IQR)
    upper_extreme = Q3 + (1.5 * IQR)
    new_array = np.delete(array, np.where((array < lower_extreme) | (array > upper_extreme)))
    outliers = [i for i in array if i < lower_extreme or i > upper_extreme]
    if len(outliers) == 0:
        print('No outlier')
    else:
        print('Outliers are {}'.format(outliers))
    return new_array

def plot_interquartile_outlier_removal(array):
    Q1 = np.quantile(array, 0.25)
    Q3 = np.quantile(array, 0.75)
    IQR = Q3 - Q1
    lower_extreme = Q1 - (1.5 * IQR)
    upper_extreme = Q3 + (1.5 * IQR)
    outliers = []
    for i in array:
        if (i < lower_extreme) | ( i > upper_extreme):
            outliers.append(i)
    new_array = np.delete(array,np.where((array < lower_extreme) | (array > upper_extreme)))
    plt.figure(figsize=(12,5))
    plt.subplot(1,2,1)
    for i in outliers:
        plt.annotate('Outlier',xytext=(1.1,i+2),xy=(1.01,i+1),fontsize=10,
                     arrowprops={'color':'violet','width':2,'headwidth':9})
    plt.title('Un-preprocessed dataset')
    plt.boxplot(array)
    plt.subplot(1,2,2)
    plt.title('Cleaned dataset')
    plt.boxplot(new_array)
    plt.show()
    if len(outliers) == 0:
        print('No outlier')
    else:
        print('Outliers are {}'.format(outliers))
    return np.array(new_array)

def zscore_outlier_removal(array):
    threshold = 3
    mean = np.mean(array)
    std = np.std(array, ddof=0)
    outliers = [i.astype(int) for i in array if abs((i - mean) / std) > threshold]
    new_array = [i for i in array if abs((i - mean) / std) < threshold]
    if len(outliers) == 0:
        print('No outlier')
    else:
        print('Outliers are {}'.format(outliers))
    return np.array(new_array)

def std_outlier_removal(array, std=3):
    upper_limit = array.mean() + std * array.std()
    lower_limit = array.mean() - std * array.std()
    outliers = [i for i in array if i > upper_limit or i < lower_limit]
    new_array = [i for i in array if i < upper_limit and i > lower_limit]
    if len(outliers) == 0:
        print('No outlier')
    else:
        print('Outliers are {}'.format(outliers))
    return np.array(new_array)
