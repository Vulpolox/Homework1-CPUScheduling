import CPUProcess

class ProcessList:

    # constructor
    def __init__(self, process_list: list):
        self.process_list = process_list
        self.process_in_CPU = None
        self.all_finished = False


    # accessors and mutators
    def get_internal_list(self):
        return self.process_list
    def set_internal_list(self, process_list: list):
        self.process_list = process_list
    def get_all_finished(self):
        return self.all_finished
    def get_process_in_CPU(self):
        return self.process_in_CPU


    # method for "context switching" processes in and out of CPU
    def context_switch(self, new_process: CPUProcess) -> None:

        # if both the new_process and the current_process are null, exit function
        if new_process is None and self.process_in_CPU is None: return

        # if new_process is None, then CPU is moving to idle state
        if new_process is None:
            self.process_in_CPU.set_in_CPU(False)
            self.process_in_CPU = None

        # if CPU is in idle state, put new_process in
        elif self.process_in_CPU is None:
            new_process.set_in_CPU(True)
            self.process_in_CPU = new_process

        # if there is an attempt to context switch a program that is already in the CPU, exit function
        elif self.process_in_CPU is new_process:
            return

        # otherwise, put new_process in CPU and take old one out
        else:
            new_process.set_in_CPU(True)
            self.process_in_CPU.set_in_CPU(False)
            self.process_in_CPU = new_process


    # method for calling tick() on each process in process_list, also checks if all processes are finished
    def tick_all(self) -> None:

        all_finished = not len(self.process_list) == 0 # make sure this flag is false if the list is empty
        for process in self.process_list:
            process.tick()

            # check each process for its finished flag ; short circuit if all_finished has been found to be false
            if not all_finished or not process.get_finished():
                all_finished = False

        self.all_finished = all_finished


    # method for printing all processes in process_list
    def print_processes(self) -> None:
        for process in self.process_list:
            print(process)
        print('\n\n\n')


    # method for calculating ATT
    def calculate_average_turnaround_time(self) -> float:
        sum = 0.0
        for process in self.process_list:
            turnaround_time = process.get_finish_time() - process.get_arrival_time()
#            print(f'''Process #{process.get_process_number()}; Turnaround Time = {turnaround_time}
#                  Arrival Time: {process.get_arrival_time()}; End Time: {process.get_finish_time()}''')
            sum += turnaround_time
        return sum / len(self.process_list)