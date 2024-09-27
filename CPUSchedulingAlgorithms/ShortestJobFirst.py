import CPUProcess, ProcessList, time

class ShortestJobFirst:
    def __init__(self, process_list: ProcessList):
        # initialize the process list to have the constituent processes be in the final order of execution
        self.process_list = process_list.get_internal_list().sort(key=lambda process: process.get_burst_time())

        self.timestamp = 0             # counter for keeping track of current time
        self.previous_finish_time = 0  # holds the timestamp of when the previous process completed

    def run(self):

        # iterate through each process in the process_list
        for process in self.process_list.get_internal_list():

            time.sleep(1) # for fun

            # check if CPU is waiting on a process to arrive
            ################################################

            if self.previous_finish_time < process.get_arrival_time():
                start_idle_time = self.timestamp
                total_idle_time = 0

                time.sleep(3) # for fun

                # idle the CPU until the next process arrives
                while self.timestamp < process.get_arrival_time():
                    self.timestamp += 1
                    total_idle_time += 1

                # display idle time message
                print(f'No Processes in Ready List.  Start Idle Time: {start_idle_time} ; Total Idle Time: {total_idle_time}')


            # if a process is ready to run
            ##############################

            # print to console that the process is entering CPU and context switch it in
            print(f'Process #{process.get_process_number()} entering CPU at Time {self.timestamp}')
            self.process_list.context_switch(process)

            # while the process is not finished (SJF is non-preemptive)
            while not process.get_finished():
                self.timestamp += 1                              # increment timestamp
                self.process_list.tick_all()                     # update fields of processes in process_list
                process.check_finish_and_update(self.timestamp)  # check for process completion and update flags

            # update previous_finish_time to check for potential waiting time for next process
            self.previous_finish_time = self.timestamp

            # print message to console
            print(f'''Process #{process.get_process_number()} Finished at Time {self.timestamp}''')

