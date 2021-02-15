# Global settings for the sclbl CLI commands

# Settings:
EXEC_MODE = "live"  # or "develop" or "live"
DEBUG = False  # Set debug mode (extensive printing from sclblpy package)

# Servers
USER_MANAGER_URL: str = "https://usermanager.sclbl.net:8008"  # Location of the user manager.
TOOLCHAIN_URL: str = "https://toolchain.sclbl.net:8010"  # Location of the toolchain server.
TASK_MANAGER_URL: str = "https://taskmanager.sclbl.net:8080"  # Location of the taskmanager.

if EXEC_MODE == "local":
    USER_MANAGER_URL = "http://localhost:8008"
    TOOLCHAIN_URL = "http://localhost:8010"
    TASK_MANAGER_URL = "http://localhost:8080"
elif EXEC_MODE == "develop":
    USER_MANAGER_URL = "https://dev.usermanager.sclbl.net:8008"
    TOOLCHAIN_URL = "https://dev.toolchain.sclbl.net:8010"
    TASK_MANAGER_URL = "https://dev.taskmanager.sclbl.net:8080"

if __name__ == '__main__':
    print("No command line options available for _globals.py.")