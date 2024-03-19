import os
import psutil


def cpu_usage():

    # Getting loadover15 minutes
    load1, load5, load15 = psutil.getloadavg()
    cpu_usage = (load15 / os.cpu_count()) * 100
    return cpu_usage
    # print("The CPU usage is : ", cpu_usage)


def memory_usage():
    # Getting all memory using os.popen()
    total_memory, used_memory, free_memory = map(
        int, os.popen("free -t -m").readlines()[-1].split()[1:]
    )
    memory_usage = round((used_memory / total_memory) * 100, 2)
    return memory_usage
    # Memory usage
    # print("RAM memory % used:", round((used_memory / total_memory) * 100, 2))
