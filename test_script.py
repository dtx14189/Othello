from concurrent.futures import ProcessPoolExecutor
import subprocess

#INFORMATION ABOUT THE PROJECT IS WRITTEN IN THE README

#magic number for determining the number of each time to run
#CHANGE 1
magic_number = 2

#These are the times that we actually tested when collecting our data
#CHANGE 2
# times = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50]

#The script is set to run the times through for a much smaller sample of times
#This way, it will finish in a couple of minutes at most
times = [0.1, 0.2, 0.5]

#CHANGE 3
#6 different possible matchups between agents
matchups = [_ for _ in range(3, 6)]

#Function to run a single trial, which involves a particular time limit 
#and a particular agent matchup for a certain number of playouts as 
#determined by the magic number
def run_trial(time_limit, matchup, playouts):
    #Run one experiment of compare_agents for a single matchup of agents

    cmd = [
        "pypy3",
        "compare_agents.py",
        "--time", str(time_limit),
        "--count", str(playouts),  #specify the number of games to run per matchup
        "--random", "0.1",  #specify the randomness
        "--matchup", str(matchup)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout  # Return the output for data compilation
    except subprocess.CalledProcessError as e:
        return f"Error in trial: {e.stderr}"

def main():
    # Use ProcessPoolExecutor to parallelize all of the trial runs
    with ProcessPoolExecutor() as executor:

        #Create a list of all trials
        trials = []
        for time_limit in times:
            for matchup in matchups:

                trials.append((time_limit, matchup))

        #Submit each trial to the executor
        futures_to_trial = {
            executor.submit(run_trial, time_limit, matchup, int(magic_number / time_limit)): (time_limit, matchup)
            for time_limit, matchup in trials
        }

        i = 0
        # Wait for all tasks to complete and process results
        for future in futures_to_trial:
            time_limit, matchup = futures_to_trial[future]

            try:
                result = future.result()
                #CHANGE 4
                with open(f'scratch_{magic_number}_{matchup}_{time_limit}.txt', 'w') as oo:
                    print(result, file=oo, end="")
            except Exception as e:
                with open(f'{i}_{matchup}.txt', 'w') as oo:
                    print(f"Error for matchup {matchup} with time limit {time_limit}", file=oo)
            i += 1

if __name__ == "__main__":
    main()
