import math
import random
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns


def createData(difficulty):
    if difficulty == "easy":
        num_of_job_types, num_of_employees, friendship_percentage = 10, 10, 0.95
    elif difficulty == "medium":
        num_of_job_types, num_of_employees, friendship_percentage = 30, 30, 0.8
    elif difficulty == "hard":
        num_of_job_types, num_of_employees, friendship_percentage = 30, 100, 0.6
    else:
        print("please insert one of the following: \"easy\" / \"medium\" / \"hard\"")
        return
    two_dim_array = np.zeros((num_of_job_types * num_of_employees, num_of_job_types * num_of_employees))
    possible_friends = []
    for i in range(num_of_job_types):
        for j in range(num_of_job_types):
            for k in range(num_of_employees):
                for l in range(num_of_employees):
                    if j<i:
                        two_dim_array[i * num_of_employees + k][j * num_of_employees + l]=-2
                    elif i==j:
                        two_dim_array[i * num_of_employees + k][j * num_of_employees + l]=-1
                    elif j>i:
                        possible_friends.append((i * num_of_employees + k, j * num_of_employees + l))
                    # print(i*num_of_employees+k,j*num_of_employees+l) #print indexes
    counter = 0
    amount_of_friends = ((math.pow(num_of_job_types * num_of_employees, 2) - num_of_job_types * math.pow(
        num_of_employees, 2)) / 2)*friendship_percentage
    print("amount_of_friends: ", amount_of_friends)
    while counter < amount_of_friends:
        choice = random.choice(possible_friends)
        if two_dim_array[choice[0]][choice[1]] == 0:
            two_dim_array[choice[0]][choice[1]] = 1
            counter += 1
    print("total vertices: ", np.sum(two_dim_array))
    # todo : transfer two_dim_array to nx library graph
    np.savetxt("writtenData/" + difficulty + ".txt", two_dim_array, delimiter=',', fmt='%d')
    return two_dim_array


def readData(file_name):
    try:
        data = np.loadtxt("writtenData/" + file_name + ".txt", delimiter=',').astype(int)  # reads as int instead float
        print(data.size)
        print("total vertices: ", np.sum(data))
        return data
    except OSError:
        print("File name does not exist")
    except Exception as e:
        print(e)
    return


def figure_collision_matrix(matrix,  title: str):
    plt.suptitle(title)
    colors = ('#f0f5f5', '#c1d7d7', '#003300', '#33cccc')
    cmap = LinearSegmentedColormap.from_list('Custom', colors, len(colors))
    ax = sns.heatmap(matrix, cbar=True, cmap=cmap)
    colorbar = ax.collections[0].colorbar
    colorbar.set_ticks([-1.5, -0.75, 0, 0.75])
    colorbar.set_ticklabels(['symmetry unnecessary', 'same job type', 'not friends', 'friends'])

    plt.savefig("drawnData/" + title + ".png", bbox_inches='tight')

    plt.show()
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()

if __name__ == '__main__':
    matrix = createData("medium")  # easy/medium/hard
    matrix = readData("medium")
    if matrix.any():
        figure_collision_matrix(matrix, "medium")
