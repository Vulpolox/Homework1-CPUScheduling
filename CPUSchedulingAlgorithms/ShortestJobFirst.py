import CPUProcess, ProcessList, time

class ShortestJobFirst:
    def __init__(self, process_list: ProcessList):
        self.process_list = process_list
        self.ready_list = ProcessList.ProcessList([])

        self.timestamp = 0             # counter for keeping track of current time
        self.previous_finish_time = 0  # holds the timestamp of when the previous process completed

    def run(self):

        print(f'Starting SJF Algorithm\n*****************')
        time.sleep(2)

        while not self.process_list.get_all_finished():

            time.sleep(1)

            # check for new processes that are ready to enter the ready_list
            for process in self.process_list.get_internal_list():

                # if process hasn't already been marked as arrived and its arrival_time has passed
                if not process.get_arrived() and process.get_arrival_time() <= self.timestamp:
                    process.set_arrived(True)                           # mark it as arrived
                    self.ready_list.get_internal_list().append(process) # add it to the ready_list

            # if ready list is empty, idle the CPU --> increment time stamp & re-run outer loop until a proces arrives
            if len(self.ready_list.get_internal_list()) == 0:
                self.timestamp += 1
                continue

            # if there are processes in the ready_list
            else:
                self.ready_list.get_internal_list().sort(key=lambda process: process.get_burst_time()) # sort them by shortest job
                current_process = self.ready_list.get_internal_list().pop(0)                           # pop and store the process with the shortest job in current_process


                self.process_list.context_switch(current_process)                                      # context switch current_process into CPU
                print(f'\nProcess #{current_process.get_process_number()} Entering CPU at Time {self.timestamp}')

                while not current_process.get_finished():
                    self.timestamp += 1
                    self.process_list.tick_all()
                    current_process.check_finish_and_update(self.timestamp)

                time.sleep(0.5)
                print(f'Process #{current_process.get_process_number()} Finished at Time {self.timestamp}\n--------')

        print(f'''*********************************************
SJF Algorithm Completed in {self.timestamp} Time Units
Average Turnaround Time: {self.process_list.calculate_average_turnaround_time()} Time Units
*********************************************''')
        time.sleep(10)