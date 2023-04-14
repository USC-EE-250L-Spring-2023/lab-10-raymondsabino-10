#Raymond Sabino
#https://github.com/USC-EE-250L-Spring-2023/lab-10-raymondsabino-10

import time
import numpy as np
from typing import List, Optional

import threading
import pandas as pd
import requests
import plotly.express as px

def generate_data() -> List[int]:
    """Generate some random data."""
    return np.random.randint(100, 10000, 1000).tolist()

def process1(data: List[int]) -> List[int]:
    """Summary: Finds the next largest prime number from each element in data and returns them in a list.
    
    Args:
        data: The data (a list of ints) to be processed.

    Returns:
        List[int]: A list of the next largest prime numbers from each element in data."""
    def foo(x):
        """Find the next largest prime number."""
        while True:
            x += 1
            if all(x % i for i in range(2, x)):
                return x
    return [foo(x) for x in data]

def process2(data: List[int]) -> List[int]:
    """Summary: Finds the next largest perfect square of each element of the input data
    
    Args:
        data: The data (a list of ints) to be processed.

    Returns:
        List[int]: A list of the elements that are the next largest perfect squares from each element of data."""
    def foo(x):
        """Returns the closest greater value to the input x that is a perfect square."""
        while True:
            x += 1
            if int(np.sqrt(x)) ** 2 == x:
                return x
    return [foo(x) for x in data]

def final_process(data1: List[int], data2: List[int]) -> List[int]:
    """Summary: Finds the mean of the differences between data1 and data2.
    
    Args:
        data1: The first piece of data (a list of ints) to be processed.
        data2: The second piece of data (also a list of ints) to be processed

    Returns:
        List[int]: The mean of the differences between each element in data1 and data2."""
    return np.mean([x - y for x, y in zip(data1, data2)])

offload_url = 'http://192.168.56.1:5000' # TODO: Change this to the IP address of your server

def run(offload: Optional[str] = None) -> float:
    """Run the program, offloading the specified function(s) to the server.
    
    Args:
        offload: Which function(s) to offload to the server. Can be None, 'process1', 'process2', or 'both'.

    Returns:
        float: the final result of the program.
    """
    data = generate_data()
    data1 = None
    data2 = None
    if offload is None: # in this case, we run the program locally
        data1 = process1(data)
        data2 = process2(data)
    elif offload == 'process1':
        data1 = None
        def offload_process1(data):
            nonlocal data1
            # TODO: Send a POST request to the server with the input data
            response = requests.post(f'{offload_url}/offloadprocess1', json={'data':data})
            data1 = response.json()
        thread = threading.Thread(target=offload_process1, args=(data,))
        thread.start()
        data2 = process2(data)
        thread.join()
        # Question 2: Why do we need to join the thread here?
        # Question 3: Are the processing functions executing in parallel or just concurrently? What is the difference?
        #   See this article: https://oxylabs.io/blog/concurrency-vs-parallelism
        #   ChatGPT is also good at explaining the difference between parallel and concurrent execution!
        #   Make sure to cite any sources you use to answer this question.
    elif offload == 'process2':
        # TODO: Implement this case
        data2 = None
        def offload_process2(data):
            nonlocal data2
            # TODO: Send a POST request to the server with the input data
            response = requests.post(f'{offload_url}/offloadprocess2', json={'data':data})
            data2 = response.json()
        thread = threading.Thread(target=offload_process2, args=(data,))
        thread.start()
        data1 = process1(data)
        thread.join()
    elif offload == 'both':
        # TODO: Implement this case
        data1 = None
        data2 = None
        def offload_processes(data):
            nonlocal data1
            nonlocal data2
            # TODO: Send a POST request to the server with the input data
            response = requests.post(f'{offload_url}/offloadprocess1', json={'data':data})
            data1 = response.json()
            response = requests.post(f'{offload_url}/offloadprocess2', json={'data':data})
            data2 = response.json()
        thread = threading.Thread(target=offload_processes, args=(data,))
        thread.start()
        thread.join()
    ans = final_process(data1, data2)
    return ans 

def main():
    # TODO: Run the program 5 times for each offloading mode, and record the total execution time
    #   Compute the mean and standard deviation of the execution times
    #   Hint: store the results in a pandas DataFrame, use previous labs as a reference
    data = [] #Data point list
    offload_types = ['None','process1','process2','both']
    for offload_type in offload_types:
        timeData = [] #Empty array to store time data for each trial
        for i in range(5): #Runs 5 trials for each type
            time1 = time.time()
            print(offload_type)
            if (offload_type == 'None'):
                run()
            else:
                run(offload_type)
            timeData.append(time.time()-time1)
        timeData_mean = np.mean(timeData)
        timeData_std = np.std(timeData)
        data.append((offload_type, timeData_mean, timeData_std))

    df = pd.DataFrame(data, columns=['offload_type','timeData_mean','timeData_std'])


    # TODO: Plot makespans (total execution time) as a bar chart with error bars
    # Make sure to include a title and x and y labels
    fig = px.bar(df,x='offload_type',y='timeData_mean',error_y='timeData_std')

    # TODO: save plot to "makespan.png"
    fig.write_image("makespan.png")

    # Question 4: What is the best offloading mode? Why do you think that is?
    # Question 5: What is the worst offloading mode? Why do you think that is?
    # Question 6: The processing functions in the example aren't very likely to be used in a real-world application. 
    #   What kind of processing functions would be more likely to be used in a real-world application?
    #   When would you want to offload these functions to a server?
    
    
if __name__ == '__main__':
    main()