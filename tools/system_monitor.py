
import psutil
import os
import platform


def get_cpu_usage():
    """Collect CPU utilization."""
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    """Collect RAM utilization."""
    memory = psutil.virtual_memory()

    return {
        "total_gb": round(memory.total / (1024 ** 3), 2),
        "used_gb": round(memory.used / (1024 ** 3), 2),
        "available_gb": round(memory.available / (1024 ** 3), 2),
        "usage_percent": memory.percent
    }


def get_disk_usage():
    """Collect system disk utilization."""
    drive = os.environ.get("SystemDrive", "C:")

    disk = psutil.disk_usage(drive + "\\")

    return {
        "drive": drive,
        "total_gb": round(disk.total / (1024 ** 3), 2),
        "used_gb": round(disk.used / (1024 ** 3), 2),
        "free_gb": round(disk.free / (1024 ** 3), 2),
        "usage_percent": disk.percent
    }


def get_system_info():
    """Collect complete system information."""

    return {
        "hostname": platform.node(),
        "os": platform.system(),
        "os_version": platform.version(),
        "cpu_usage": get_cpu_usage(),
        "memory": get_memory_usage(),
        "disk": get_disk_usage()
    }


if __name__ == "__main__":
    import json

    metrics = get_system_info()

    print(json.dumps(metrics, indent=4))
