import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import norm

colors = ['gold', 'darkorange', 'red', 'darkred']


def plot_trends(np_feature_vectors, feature_names, window_size, analysis_directory, dict_change_points="",
                subgroup="", min_freq=50):
    np_feature_vectors = np.transpose(np_feature_vectors)
    intervals = range(1, np.shape(np_feature_vectors)[1]+1)
    for index, feature in enumerate(feature_names):
        feature_vector = np_feature_vectors[index]
        if np.sum(feature_vector) > min_freq:
            plt.figure(figsize=(8, 3))
            plt.plot(intervals, feature_vector, '-')
            y_max = max(10, np.amax(feature_vector))
            if dict_change_points is not "":
                idx = 0
                for penalty, change_points in dict_change_points.items():
                    for cp_index, cp in enumerate(change_points):
                        if cp_index + 1 == len(change_points):
                            plt.plot([cp, cp], [0, y_max], '--', label=penalty, color=colors[idx])
                        else:
                            plt.plot([cp, cp], [0, y_max], '--', color=colors[idx])
                    idx += 1
                plt.legend(loc="best")
            plt.ylim(0, y_max)
            plt.xlim(intervals[0], intervals[-1])
            plt.xlabel("Week")
            plt.ylabel("Count")
            # plt.show()
            plt.savefig(f"{analysis_directory}\\{window_size}day_{subgroup}_{feature}", bbox_inches='tight')
            plt.close()
            # print(feature)


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
