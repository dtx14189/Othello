import os
import matplotlib.pyplot as plt
import re

#Times for versus agents
# times = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50]

#Times for versus greedy
# times = [0.05, 0.1, 0.2, 0.5, 1]

#Times for lightweight grading version
times = [0.1, 0.2, 0.5]

#Extracting the numbers from each file
def parse_file(file_name):
    with open(f'{folder_path}/{file_name}') as data_file:
        for line in data_file:
            if not line.startswith("NET"):
                continue
            data_parts = line.strip().split(";")
            numbers = [float(data.strip().split(":")[1]) for data in data_parts]
            #should only be one line of aggregated data per file
            return numbers


#Insert the path to your results folder below
folder_path1 = './graph_results'

data_map = {}
final_data = {}

#CURRENTLY SET UP TO RUN PLAYOUTS 3 through 6
#Initializing the data map
for matchup in range(3, 6):
    for time in times:
        data_map[(matchup, time)] = [0, 0]

folders = [folder_path1]

#Collecting the data across all files
for folder_path in folders:
    for filename in os.listdir(folder_path):
        # name = filename.strip(".txt").split('_')

        # #Getting rid of the zoo node name
        # if len(name) == 4:
        #     name.pop(0)

        name_nums = re.findall(r'\d+\.\d+|\d+', filename)
        name = [float(num) if '.' in num else int(num) for num in name_nums]

        #parsing the file to extract the data
        magic_number = int(name[0])
        matchup = int(name[1])
        time = float(name[2])

        #Keep track of the aggregated statistics
        data_map[(matchup, time)][0] += magic_number
        data_map[(matchup, time)][1]+= parse_file(filename)[1] * magic_number

#CURRENTLY SET UP TO RUN PLAYOUTS 3 through 6
for matchup in range(3, 6):
    for time in times:
        final_data[(matchup, time)] = data_map[(matchup, time)][1] / data_map[(matchup, time)][0]

print(final_data)


#Accumulating all of the data for matplotlib
graph_data = {}

for (matchup, time), win_rate in final_data.items():
    if matchup not in graph_data:
        graph_data[matchup] = {"times": [], "p1_wins": []}
    graph_data[matchup]["times"].append(time)
    graph_data[matchup]["p1_wins"].append(win_rate)

matchups = ["mcts vs greedy", "alpha/beta vs greedy", 
                "scout vs greedy", "mcts vs alpha/beta", "mcts vs scout", "alpha/beta vs scout"]

#Generating the graph
plt.figure(figsize=(10, 6))
for matchup, points in graph_data.items():
    times = points["times"]
    win_rates = points["p1_wins"]

    # Sort by time so that the plot loooks correct
    sorted_indices = sorted(range(len(times)), key=lambda i: times[i])
    sorted_times = [times[i] for i in sorted_indices]
    sorted_p1_wins = [win_rates[i] for i in sorted_indices]
    
    plt.plot(sorted_times, sorted_p1_wins, marker='o', label=f"{matchups[matchup]}")

#Title
plt.title("Agent Win Rate for 3 Comp Intelligence Agents vs. Greedy")

#Legend for labels
plt.legend()
#Axis Names
plt.xlabel('Computation Time')
plt.ylabel('Agent Win Rate')

plt.savefig("lightweight_results.png")
