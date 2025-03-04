import subprocess

def run_command(command: list[str], cwd: str) -> None:
    process = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if process.returncode != 0:
        raise Exception(f"Command failed with exit code {process.returncode}. Error: {process.stderr}")