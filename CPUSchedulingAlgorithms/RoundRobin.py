import CPUProcess, ProcessList

class RoundRobin:

    # constructor
    def __init__(self, process_list: ProcessList, time_quantum: int):
        self.process_list = process_list                                         # internal list for every single process finished or not
        self.ready_list: ProcessList = ProcessList.ProcessList([])               # processes that are ready to run in the current RR cycle
        self.has_run_this_cycle: ProcessList = ProcessList.ProcessList([])       # processes that have already run in the current RR cycle
        self.timestamp = 0                                                       # a counter for keeping track of the current time
        self.time_quantum = time_quantum                                         # time quantum for RR


    def run(self) -> None:

        # while there exists at least one process whose finished flag is false
        while not self.process_list.get_all_finished():

            # if the ready list is not empty
            if not len(self.ready_list.get_internal_list()) == 0:
                current_process = self.ready_list.get_internal_list()[0]
                self.ready_list.context_switch(current_process)

                for i in range(self.time_quantum):
                    self.ready_list.tick_all()
                    self.timestamp += 1

                self._handle_new_arrivals(self.timestamp) # add the newly arrived processes to the ready list

                # remove the current process from the ready_list and add it into the has_run_this_cycle list
                self.ready_list.get_internal_list().pop(0)
                self.has_run_this_cycle.get_internal_list().append(current_process)


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
            updated_ready_list = self.ready_list.get_internal_list() + new_arrivals # put the new processes at the end of the ready list
            self.ready_list.set_internal_list(updated_ready_list)                   # set the ready list to this









