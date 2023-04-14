# Lab 10
[Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repo and clone it to your machine to get started!

## Team Members
- Raymond Sabino

## Lab Question Answers

Question 1: Under what circumstances do you think it will be worthwhile to offload one or both
of the processing tasks to your PC? And conversely, under what circumstances will it not be
worthwhile?

	Answer: It would be worthwhile to offload one or both processing tasks to my PC when the datasets are large enough such that the time it takes to send the task to my PC and the time it takes my PC to process and return the processed data is less than the time it would take to process in the Raspberry Pi's more limited hardware.

Question 2: Why do we need to join the thread here?

	Answer: The program needs to wait for offload_process1 to complete before continuing to make sure the data offloaded to the server is processed and received before final_process executes.

Question 3: Are the processing functions executing in parallel or just concurrently? What is the difference?
	
	Answer: The processing functions are executing in parallel when the task is offloaded to the PC. The PC server processes the data with whichever process is chosen to be offloaded while the other process runs in the system running main.py, in this case the Raspberry Pi. Since these run at the same time, it is parallel execution. Concurrent execution means the system has the ability to manage multiple tasks at once, but doesn't necessarily execute them at the same time.
	Source: https://oxylabs.io/blog/concurrency-vs-parallelism

Question 4: What is the best offloading mode? Why do you think that is?

	Answer: 

Question 5: What is the worst offloading mode? Why do you think that is?


Question 6: The processing functions in the example aren't very likely to be used in a real-world application. What kind of processing functions would be more likely to be used in a real-world application? When would you want to offload these functions to a server?