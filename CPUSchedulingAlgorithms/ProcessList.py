import CPUProcess

class ProcessList:

    # constructor
    def __init__(self, process_list: list):
        self.process_list = process_list
        self.process_in_CPU = None


    # method for "context switching" processes in and out of CPU
    def context_switch(self, new_process: CPUProcess) -> None:

        # if new_process is None, then CPU is moving to idle state
        if new_process is None:
            self.process_in_CPU.set_in_CPU(False)
            self.process_in_CPU = None

        # if CPU is in idle state, put new_process in
        if self.process_in_CPU is None:
            new_process.set_in_CPU(True)
            self.process_in_CPU = new_process

        # otherwise, put new_process in CPU and take old one out
        else:
            new_process.in_CPU(True)
            self.process_in_CPU.set_in_CPU(False)
            self.process_in_CPU = new_process


    # method for calling tick() on each process in process_list
    def tick_all(self) -> None:
        for process in self.process_list:
            process.tick()


    # method for printing all processes in process_list
    def print_processes(self) -> None:
        for process in self.process_list:
            print(process)
        print('\n\n\n')