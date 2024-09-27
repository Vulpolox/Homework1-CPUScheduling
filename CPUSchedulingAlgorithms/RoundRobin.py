import CPUProcess, ProcessList, time

class RoundRobin:

    # constructor
    def __init__(self, process_list: ProcessList, time_quantum: int):
        self.process_list = process_list                                         # internal list for every single process finished or not
        self.ready_list: ProcessList = ProcessList.ProcessList([])               # processes that are ready to run in the current RR cycle
        self.has_run_this_cycle: ProcessList = ProcessList.ProcessList([])       # processes that have already run in the current RR cycle
        self.timestamp = 0                                                       # a counter for keeping track of the current time
        self.time_quantum = time_quantum                                         # time quantum for RR


    def run(self) -> None:

        # print message confirming start of algorithm
        print('Starting Round Robin Algorithm\n**********\n')

        # while there exists at least one process whose finished flag is false
        while not self.process_list.get_all_finished():

            time.sleep(0.5) # makes the program execution more fun

            # add the newly arrived processes to the ready list in order of their external priorities
            self._handle_new_arrivals(self.timestamp)

            # if the ready list is not empty
            if not len(self.ready_list.get_internal_list()) == 0:
                self.ready_list.get_internal_list().sort(key=lambda process: process.get_external_priority())
                current_process = self.ready_list.get_internal_list()[0] # assign the first process in the ready_list to current_process
                self._execute_time_quantum(current_process)

                # remove the current process from the ready_list and add it into the has_run_this_cycle list
                self.ready_list.get_internal_list().pop(0)
                self.has_run_this_cycle.get_internal_list().append(current_process)

            # if the ready_list is empty and the has_run is not, context switch in the first process from the has_run_this_cycle list for time_quantum time
            elif len(self.ready_list.get_internal_list()) == 0 and len(self.has_run_this_cycle.get_internal_list()) > 0:
                current_process = self.has_run_this_cycle.get_internal_list()[0]
                self._execute_time_quantum(current_process)

                # then move the current_process to the end of the has_run list
                self.has_run_this_cycle.get_internal_list().pop(0)
                self.has_run_this_cycle.get_internal_list().append(current_process)

            # if both the ready_list and the has_run list are empty, the CPU needs to be idle
            elif len(self.ready_list.get_internal_list()) == 0 and len(self.has_run_this_cycle.get_internal_list()) == 0:
                self.ready_list.context_switch(None) # context switch null into CPU

                # tick_all() both lists to update turnaround_time counters and increment timestamp
                # new processes will be checked for next iteration of outer loop using updated timestamp
                self.process_list.tick_all()
                self.timestamp += 1  # increment the timestamp by time_quantum

        print(f'''*********************************
Round Robin Completed in {self.timestamp} Time Units
Average Turnaround Time = {self.process_list.calculate_average_turnaround_time():.2f} Time Units
*********************************''')


    # method for handling processes that have newly arrived
    def _handle_new_arrivals(self, timestamp) -> None:

        # exit function if all processes have already entered the ready state i.e. no new arrivals possible
        if len(self.has_run_this_cycle.get_internal_list()) + len(self.ready_list.get_internal_list()) == len(self.process_list.get_internal_list()):
            return

        new_arrivals: list = []

        # iterate through process_list to look for newly arrived processes
        for process in self.process_list.get_internal_list():

            # if process's arrival time has been reached, and it's flag is not yet updated
            if not process.get_arrived() and process.get_arrival_time() <= self.timestamp:
                process.set_arrived(True)     # update its arrived flag
                new_arrivals.append(process)  # append process to new_arrivals list

        # add the new arrivals to the ready list if any exist
        if len(new_arrivals) > 0:
            updated_ready_list = self.ready_list.get_internal_list() + new_arrivals # add new processes to ready_list
            self.ready_list.set_internal_list(updated_ready_list)                   # set the ready list to this


    # method for context switching a process into the CPU and keeping it there for time_quantum time
    def _execute_time_quantum(self, current_process: CPUProcess) -> None:

        # if process passed to the function has already finished, exit the function
        if current_process.get_finished():
            return

        init_timestamp = self.timestamp                 # temporary timestamp for console message
        self.ready_list.context_switch(current_process) # context switch current_process into CPU

        print(f'Process #{current_process.get_process_number()} Entering CPU at Time {self.timestamp}')

        # execute the time_quantum
        for i in range(self.time_quantum):
            self.process_list.tick_all()
            self.timestamp += 1                                     # increment the timestamp by time_quantum
            current_process.check_finish_and_update(self.timestamp) # check if the process has finished and update its flags if so

            if current_process.get_finished(): break                # if current_process finishes before loop, break to avoid idle CPU time

        print(f'''Process #{current_process.get_process_number()} in CPU for {self.timestamp - init_timestamp} Units of Time
Process Finished? : {current_process.get_finished()}
Remaining Burst Time: {current_process.get_burst_time()}
-----
''')