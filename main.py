import numpy as np


def createData(difficulty):
    if difficulty == "easy":
        num_of_job_types, num_of_employees, friendship_percentage = 10, 10, 0.95
    elif difficulty == "medium":
        num_of_job_types, num_of_employees, friendship_percentage = 30, 30, 0.8
    elif difficulty == "hard":
        num_of_job_types, num_of_employees, friendship_percentage = 30, 100, 0.6
    else:
        print ("please insert one of the following: \"easy\" / \"medium\" / \"hard\"")
        return
    two_dim_array = np.random.choice(2, size=(num_of_job_types, num_of_employees),
                           p=[1 - friendship_percentage, friendship_percentage])
    np.savetxt("writtenData/" + difficulty + ".txt", two_dim_array, delimiter=',', fmt='%d')


def readData(file_name):
    try:
        data = np.loadtxt("writtenData/" + file_name + ".txt", delimiter=',').astype(int)  # reads as int instead float
        print(data)
    except OSError:
        print("File name does not exist")
    except Exception as e:
        print(e)



if __name__ == '__main__':
    createData("easy")  # easy/medium/hard
    readData("easy")
