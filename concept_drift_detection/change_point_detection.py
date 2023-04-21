import ruptures as rpt
import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from numpy.linalg import norm


def rpt_pelt(series, pen=3):
    '''Applies the PELT-algorithm with the provided penalty
    args:
        series: (Reduced) time series, retrieved when applying dimensionality reduction
        pen: penalty value for classifying change points
    returns:
        list of change points
    '''
    algo = rpt.Pelt(model="rbf", min_size=1, jump=1).fit(series)
    result = algo.predict(pen=pen)
    # display
    rpt.display(series, result)
    plt.show()
    return result[:-1]


def windows(series, window_size=20, pen=2):
    algo = rpt.Window(width=window_size, model="l2").fit(series)
    result = algo.predict(pen=2)
    rpt.display(series, result)
    plt.show()
    return


def plot_cosine_similarity(np_feature_vectors, feature_names, window_size, analysis_directory):
    df_cosine_similarities = pd.DataFrame()
    df_cosine_similarities['time_window'] = [i for i in range(1, np.shape(np_feature_vectors)[0])]
    for index in range(1, np.shape(np_feature_vectors)[0]):
        A = np_feature_vectors[index - 1]
        B = np_feature_vectors[index]
        cosine_similarity = np.dot(A, B) / (norm(A) * norm(B))
        df_cosine_similarities.loc[df_cosine_similarities['time_window'] == index, 'cs'] = cosine_similarity
    df_cosine_similarities.plot.line(x='time_window', y='cs')
    plt.savefig(f"{analysis_directory}\\cos_sim_{feature_names}_{window_size}")
    plt.show()
