# OS
import os
import subprocess

def run_unit_test(cmd: list, test_name: str) -> int:
    """Run the unit test script and capture the return status."""
    try:
        # Run the test script as a subprocess
        result = subprocess.run(cmd,
            capture_output=True,
            text=True
        )
        # Print the output of the test
        #print("STDOUT:\n", result.stdout)
        #print("STDERR:\n", result.stderr)

        # Return the exit code
        return result.returncode
    except Exception as e:
        print(f"Error running the {test_name} unit test: {e}")
        return 1  # Non-zero status to indicate failure

if __name__ == "__main__":
    
    # Overall check
    status = 0

    file_paths = [os.path.join("densities", "examples", "example1.py"),
                  os.path.join("densities", "examples", "example2.py"),
                  os.path.join("densities", "examples", "example3.py"),
                 ]
    test_names = ["BSFG database load",
                  "Load all density databases",
                  "RIPL MS shell correction database location",
                 ]
    commands   = [["python", "-m", "unittest", fp] for fp in file_paths]

    # Total tests
    num_tests = len(file_paths)

    # Loop over all tests
    for cmd,name in zip(commands, test_names):
        status += run_unit_test(cmd, name)
    
    print(f"Total tests: {num_tests}")
    print(f"Successes  : {num_tests-status}")
    print(f"Failures   : {status}")
