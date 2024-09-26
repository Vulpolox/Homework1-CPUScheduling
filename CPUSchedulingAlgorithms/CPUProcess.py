
class CPUProcess:

    # constructor
    def __init__(self, process_number: int, arrival_time: int, burst_time: int, external_priority: int):
        self.process_number = process_number         # the unique identifier of the process
        self.arrival_time = arrival_time             # timestamp when the process first enters the ready state
        self.burst_time = burst_time                 # how long the process will run in the CPU before completing
        self.external_priority = external_priority   # decides the order of process execution if two processes have same main priority

        self.turnaround_time = 0                     # how long the process has been ready or in the CPU before finishing

        self.arrived = False                         # a flag to keep track of when the process first enters the ready state
        self.finished = False                        # a flag to keep track of when processes finishes execution
        self.in_CPU = False                          # a flag to keep track of when the process is in the CPU

        self.init_arrival_time = arrival_time        # for printing process information
        self.init_burst_time = burst_time            # for printing process information

    # accessors and mutators
    def set_arrived(self, arrived: bool):
        self.arrived = arrived
    def set_finished(self, finished: bool):
        self.finished = finished
    def set_in_CPU(self, in_CPU: bool):
        self.in_CPU = in_CPU
    def get_arrived(self):
        return self.arrived
    def get_finished(self):
        return self.finished
    def get_in_CPU(self):
        return self.in_CPU

    # for printing processes
    def __str__(self) -> str:
        return f'''Process #{self.process_number}
   Arrival Time: {self.init_arrival_time}
   Burst Time: {self.init_burst_time}
   External Priority: {self.external_priority}
  ---
   Turnaround Time: {self.turnaround_time}
  ------------------'''

    # method for updating process fields for each unit of time
    def tick(self) -> None:

        # if the process has finished or hasn't arrived, exit the function
        if self.finished or not self.arrived:
            return

        else:
            self.turnaround_time += 1 # increment the turnaround_time counter

            if self.in_CPU:
                self.burst_time -= 1  # decrement the burst_time counter

            if self.burst_time == 0:  # if the burst time has reached zero, mark the process as finished
                self.finished = True