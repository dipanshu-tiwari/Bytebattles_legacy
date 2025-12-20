import docker
import os
import tarfile
import io

from .utils import Image
from .utils import Extension


def loadTestCases(container, pid, testCount):
    tar_stream = io.BytesIO()

    with tarfile.open(fileobj=tar_stream, mode="w") as tar:
        for i in range(1, testCount + 1):
            path = f'test_case_data/{pid}/input/{i}.in'
            with open(path, 'rb') as file:
                data = file.read()
            tarinfo = tarfile.TarInfo(name=f'{i}.in')
            tarinfo.size = len(data)
            tar.addfile(tarinfo, io.BytesIO(data))

    tar_stream.seek(0)
    container.put_archive('/home/run/sandbox/testcases/', tar_stream)

def loadCode(container, task):
    tar_stream = io.BytesIO()

    with tarfile.open(fileobj=tar_stream, mode="w") as tar:
        data = task['code'].encode()
        filename = "main." + Extension[task['language']]
        tarinfo = tarfile.TarInfo(name=filename)
        tarinfo.size = len(data)
        tar.addfile(tarinfo, io.BytesIO(data))

    tar_stream.seek(0)
    container.put_archive('/home/run/sandbox/sub/', tar_stream)

def check(output, expected_output_path):
    output_tokens = output.split()
    with open(expected_output_path, 'rb') as file:
        expected_output_tokens = file.read().split()

    if len(expected_output_tokens) != len(output_tokens):
        return False
    
    for i in range(len(output_tokens)):
        if output_tokens[i] != expected_output_tokens[i]:
            return False
    return True

def get_commands(language):
    if language == "C":
        return {
            "compile": "gcc sandbox/sub/main.c -o main",
            "run": "./main"
        }
    elif language == "CPP":
        return {
            "compile": "g++ sandbox/sub/main.cpp -o main",
            "run": "./main"
        }
    elif language == "PY":
        return {
            "compile": None,   # no compilation
            "run": "python3 sandbox/sub/main.py"
        }
    else:
        raise ValueError("Unsupported language")

def execute(task):

    try:
        
        print(f"Executing Submission {task['sid']}")

        client = docker.from_env()
        image = Image[task['language']]

        container = client.containers.create(
            name=f"submission_{task['sid']}",
            image=image,
            tty=True,

            detach=True,
            auto_remove=True,
            cap_drop=["ALL"],
            network_mode="none",
            security_opt=["no-new-privileges"],
            pids_limit=64,
            user="run",
        )

        # Starting the container and loading data
        container.start()
        loadCode(container, task)
        loadTestCases(container, task['pid'], task['testCount'])

        # Compiling the code (Checking for Compilation errors)
        # out = container.exec_run(cmd='gcc sandbox/sub/main.c -o main', stdout=True, stdin=True, stderr=True)
        cmds = get_commands(task['language'])
        
        result = {
            'sid': task['sid'],
            'verdict': 'AC',
            'wallTime': 0,
            'maxMem': 0,
            'testcase': None
        }

        is_CA = False
        if cmds["compile"]:
            out = container.exec_run(
                cmd=cmds["compile"],
                stdout=True,
                stdin=True,
                stderr=True
            )

            if out.exit_code != 0:
                is_CA = True
                result['verdict'] = 'CA'
                result['testcase'] = 1

        if not is_CA:
            # If successfully compiled, running all the test cases
            for i in range(1, task['testCount']):

                # Breaking if we have gotten any verdict (other then the initial one which is AC)
                if result['verdict'] != 'AC':
                    break
                
                # Running on test with input
                cmd = f'/usr/bin/time -v timeout 2s \"./main < sandbox/testcases/{i}.in\"'

                # cmd = f'/bin/sh -c \"/usr/bin/time -f \'%e %M\' timeout -s KILL 2s ./main < sandbox/testcases/{i}.in\"'
                run_cmd = cmds["run"]

                cmd = (
                    f'/bin/sh -c '
                    f'"/usr/bin/time -f \'%e %M\' '
                    f'timeout -s KILL 2s {run_cmd} < sandbox/testcases/{i}.in"'
                )

                out = container.exec_run(cmd=cmd, demux=True)
                exit_code, (stdout, stderr) = out
                
                # Finding error bassed on exit code
                if exit_code == 137 or exit_code == 9 or exit_code == 124:
                    result['verdict'] = 'TLE'
                    result['testcase'] = i
                    result['wallTime'] = 1000 * task['timeLimit']
                    continue
                elif exit_code != 0:
                    result['verdict'] = 'RE'
                    result['testcase'] = i
                    continue

                # Updating max time taken and max memory usage
                stderr = stderr.decode()
                stats = stderr.split()
                result['wallTime'] = max(result['wallTime'], 1000 * float(stats[0]))
                result['maxMem'] = max(result['maxMem'], int(stats[1]))                

                # Checking for TLE and MLE
                if result['maxMem'] >= 1024 * (task['memLimit']):
                    result['verdict'] = 'MLE'
                    result['testcase'] = i
                elif result['wallTime'] >= 1000 * task['timeLimit']:
                    result['verdict'] = 'TLE'
                    result['testcase'] = i
                else:

                    # If programm wrote nothing, we consider this as an empty binary string
                    if stdout is None:
                        stdout = b''

                    # Checking with expected output
                    output_path = os.path.abspath(f'test_case_data/{task['pid']}/output/{i}.out')
                    if not check(stdout, output_path):
                        print(f"[FAILED]: failed at testcase {i}")
                        result['output'] = stdout.decode()
                        if len(result['output']) > 500:
                            result['output'] = result['output'][:497] + "..."
                        result['verdict'] =  'WA'
                        result['testcase'] = i

        # Execution completed, killing the container    
        container.kill()
        return result
    except Exception as e:
        print(f"[FATAL ERROR]: {e}")
        try:
            container.kill()
        except:
            pass
    
        finally:
            return {
                'sid': task['sid'],
                'verdict': 'SKP',
                'testcase': 1
            }