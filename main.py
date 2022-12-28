import numpy as np


def createData(difficulty):
    if difficulty == "easy":
        num_of_job_types, num_of_employees, friendship_percentage = 10, 10, 0.95
    elif difficulty == "medium":
        num_of_job_types, num_of_employees, friendship_percentage = 30, 30, 0.8
    elif difficulty == "hard":
        num_of_job_types, num_of_employees, friendship_percentage = 30, 100, 0.6
    elif difficulty == "test":
        num_of_job_types, num_of_employees, friendship_percentage = 2, 4, 0.5
    else:
        print ("please insert one of the following: \"easy\" / \"medium\" / \"hard\"")
        return
    two_dim_array = np.zeros((num_of_job_types*num_of_employees, num_of_job_types*num_of_employees))
    for i in range(num_of_job_types):
        for j in range(i+1,num_of_job_types):
            for k in range(num_of_employees):
                for l in range(num_of_employees):
                    #print(i*num_of_employees+k,j*num_of_employees+l) #print indexes
                    two_dim_array[i*num_of_employees+k][j*num_of_employees+l]=np.random.choice([0,1], 1, p=[1-friendship_percentage,friendship_percentage])
    # print("total vertices: " ,np.sum(two_dim_array))
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
    #createData("hard")  # easy/medium/hard
    readData("hard")
