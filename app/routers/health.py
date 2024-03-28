import os
import psutil
import datetime
from fastapi import APIRouter

router = APIRouter()


def cpu_usage():
    """
    Get CPU usage percentage.

    Returns:
        float: CPU usage percentage.
    """
    try:
        load1, load5, load15 = psutil.getloadavg()
        cpu_percent = round((load15 / psutil.cpu_count()) * 100, 2)
    except Exception as e:
        print(f"Error retrieving CPU usage: {e}")
        cpu_percent = None
    return cpu_percent


def memory_usage():
    """
    Get memory usage percentage.

    Returns:
        float: Memory usage percentage.
    """
    try:
        total_memory, used_memory, free_memory = map(
            int, os.popen("free -t -m").readlines()[-1].split()[1:]
        )
        memory_percent = round((used_memory / total_memory) * 100, 2)
    except Exception as e:
        print(f"Error retrieving memory usage: {e}")
        memory_percent = None
    return memory_percent


@router.get("/health/", tags=["health"])
async def read_system_health():
    return {
        "CPU_usage": cpu_usage(),
        "RAM_usage": memory_usage(),
        "generatedAt": datetime.datetime.now(),
    }


@router.get("/health/cpu", tags=["health"])
async def read_system_health():
    return {
        "CPU_usage": cpu_usage(),
        "generatedAt": datetime.datetime.now(),
    }


@router.get("/health/ram", tags=["health"])
async def read_system_health():
    return {
        "RAM_usage": memory_usage(),
        "generatedAt": datetime.datetime.now(),
    }
