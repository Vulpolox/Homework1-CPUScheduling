import CPUProcess, ProcessList, RoundRobin
from ShortestJobFirst import ShortestJobFirst

if __name__ == '__main__':
    sjf_process_list = ProcessList.ProcessList([CPUProcess.CPUProcess(process_number=1, arrival_time=0, burst_time=3),
                                                CPUProcess.CPUProcess(process_number=2, arrival_time=2, burst_time=6),
                                                CPUProcess.CPUProcess(process_number=3, arrival_time=4, burst_time=4),
                                                CPUProcess.CPUProcess(process_number=4, arrival_time=6, burst_time=5),
                                                CPUProcess.CPUProcess(process_number=5, arrival_time=8, burst_time=2),])

    rr_process_list = ProcessList.ProcessList([CPUProcess.CPUProcess(process_number=1, arrival_time=0, burst_time=2, external_priority=2),
                                            CPUProcess.CPUProcess(process_number=2, arrival_time=1, burst_time=1, external_priority=1),
                                            CPUProcess.CPUProcess(process_number=3, arrival_time=2, burst_time=8, external_priority=4),
                                            CPUProcess.CPUProcess(process_number=4, arrival_time=3, burst_time=4, external_priority=2),
                                            CPUProcess.CPUProcess(process_number=5, arrival_time=4, burst_time=5, external_priority=3)])

    shortest_job_first = ShortestJobFirst(sjf_process_list)
    shortest_job_first.run()

    roundrobin = RoundRobin.RoundRobin(rr_process_list, time_quantum=2)
    roundrobin.run()