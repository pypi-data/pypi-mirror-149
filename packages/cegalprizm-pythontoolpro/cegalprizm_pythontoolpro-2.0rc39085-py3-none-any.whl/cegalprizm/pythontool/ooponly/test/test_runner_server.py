# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import re
import socket
import glob
import sys
from timeit import default_timer as timer
import runpy
import traceback
import os
import io
import csv


class TestRunnerServer():
    def __init__(self, port_number):
        self._port_number = port_number
        self._host = '127.0.0.1'
        self._test_results = {}

    def start_listening(self, timeout_seconds):
        socket.setdefaulttimeout(timeout_seconds)        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self._host, self._port_number))
            s.listen()
            conn, addr = s.accept()
           
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                while data:
                    result = self._handle_received(data, conn)
                    if not result:
                        break
                    
                    returned_message = bytes(str(result), 'utf8')
                    conn.sendall(returned_message)
                    data = conn.recv(1024)

    def _handle_received(self, data, conn):
        test_folder = data.decode('utf8')
        if test_folder == 'EXIT':
            conn.close()
            result = None
        elif test_folder == 'VERIFY CONNECTION':
            result = 'CONNECTION OK'
        else:
            result = self._run_test_script(test_folder)

        return result

    def _run_test_script(self, test_folder):
        test_folder += "\\"
        print(test_folder)
        if os.environ.get("PTP_DO_PROFILE", "0") == "PY" or os.environ.get("PTP_DO_PROFILE", "0") == "GRPC":
            result = self._run_test_with_profile(test_folder)
        else:
            result = self._run_test(test_folder)
        print(result)
        self._test_results[test_folder] = result
        if not result:
            result = 'Test failed to run'

        return result

    def _run_test_with_profile(self, test_folder):
        import cProfile
        import pstats
        from flameprof import render
        success = False
        testcode_path = glob.glob(f'{test_folder}*_testcode.py')
        try:
            with open(testcode_path[0]) as f:
                first_line = f.readline()
            if '# OOP SKIP' in first_line:
                return {test_folder: 'ooo SKIPPED\t          '}
        except Exception as e:
            print(e)
            return

        global debug_filter
        if debug_filter:
            with open(testcode_path[0]) as f:
                for line in f.readlines():
                    if debug_filter in line:
                        print('***************** ', f.name)

        try:
            original_stdout = sys.stdout    
            resultfile_name = f'{test_folder}oop_result.txt'
            with open(resultfile_name, 'w', encoding='utf8') as f:
                sys.stdout = f
            
                start = timer()
            
                try:
                    prof = cProfile.Profile()
                    prof.enable()
                    os.environ["PTP_TESTDIR"] = '{}'.format(os.path.dirname(os.path.abspath(testcode_path[0])))
                    runpy.run_path(testcode_path[0])
                except Exception as e:
                    print(type(e).__name__, " ", e)
                    print(traceback.format_exc())
                finally:
                    prof.disable()
                    s = pstats.Stats(prof)
                    svg_file = os.path.splitext(testcode_path[0])[0]+".svg"
                    with open(svg_file, "w") as f:
                        render(s.stats, f)

                    sf = io.StringIO()
                    ps = pstats.Stats(prof, stream=sf)
                    ps.sort_stats('cumulative')
                    ps.print_stats()

                    with open(os.path.splitext(testcode_path[0])[0]+"_pstats.csv", "w", newline="") as f:
                        writer = csv.writer(f,  delimiter='\t')
                        writer.writerow(["cprofile_calls", "tottime", "percall", "cumtime", "percall","filename", "function"])
                        _re = re.compile(r"\s+(\d+)(?:/\d+)?\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(.:\\.+\\*.+\..+):\d+\((\w+)\)")
                        for line in sf.getvalue().split("\n")[5:]:
                            m = re.search(_re, line)
                            if m:
                                writer.writerow([m.group(i) for i in range(1,8)])

                    grpc_calls_file = os.path.join(os.environ["PTP_TESTDIR"], "gprc_calls.csv")
                    cprofile_calls_file = os.path.splitext(testcode_path[0])[0]+"_pstats.csv"
                    chattines_file = os.path.join(os.environ["PTP_TESTDIR"], "chattines.csv")
                    if os.path.exists(grpc_calls_file):
                        import pandas as pd
                        grpc_calls_df = pd.read_csv(grpc_calls_file, delimiter="\t")
                        cprofile_calls_df = pd.read_csv(cprofile_calls_file, delimiter="\t")
                        joined_df = pd.merge(grpc_calls_df, cprofile_calls_df, on=["filename", "function"])
                        joined_df["chattiness"] = joined_df["gprc_calls"]/joined_df["cprofile_calls"]
                        joined_df.to_csv(chattines_file, sep="\t")
                        
                    del os.environ["PTP_TESTDIR"]
            
                ellapsed_time = timer() - start

            sys.stdout = original_stdout

            timing_message = '{:8.1f}'.format(ellapsed_time*1000) + 'ms'
            success = self._compare_with_expected(test_folder)   
        except Exception as e:
            print(type(e).__name__, '' '', e)

        return '+++ PASSED\t' + timing_message if success else '--- FAILED\t' + timing_message 
                    
    def _run_test(self, test_folder):    
        success = False
        testcode_path = glob.glob(f'{test_folder}*_testcode.py')
        try:
            with open(testcode_path[0]) as f:
                first_line = f.readline()
            if '# OOP SKIP' in first_line:
                return {test_folder: 'ooo SKIPPED\t          '}
        except Exception as e:
            print(e)
            return

        global debug_filter
        if debug_filter:
            with open(testcode_path[0]) as f:
                for line in f.readlines():
                    if debug_filter in line:
                        print('***************** ', f.name)

        try:
            original_stdout = sys.stdout    
            resultfile_name = f'{test_folder}oop_result.txt'
            with open(resultfile_name, 'w', encoding='utf8') as f:
                sys.stdout = f
            
                start = timer()
            
                try:
                    os.environ["PTP_TESTDIR"] = '{}'.format(os.path.dirname(os.path.abspath(testcode_path[0])))
                    runpy.run_path(testcode_path[0], None)
                except Exception as e:
                    print(type(e).__name__, " ", e)
                    print(traceback.format_exc())
                    del os.environ["PTP_TESTDIR"]
            
                ellapsed_time = timer() - start

            sys.stdout = original_stdout

            timing_message = '{:8.1f}'.format(ellapsed_time*1000) + 'ms'
            success = self._compare_with_expected(test_folder)   
        except Exception as e:
            print(type(e).__name__, '' '', e)

        return '+++ PASSED\t' + timing_message if success else '--- FAILED\t' + timing_message 


    def _compare_with_expected(self, folder):
        with open(folder + 'oop_result.txt', 'r') as f:
            oop_result_lines = f.readlines()

        oop_result = self._join_non_blanks(oop_result_lines)

        with open(folder + 'expected_result.txt', 'r') as f:
            expected_result_lines = f.readlines()

        expected_result = self._join_non_blanks(expected_result_lines)
        passed = expected_result in oop_result
        with open(folder + 'compare_result.txt', 'w') as f:
            f.write('*** Expected ***\n')
            f.write(expected_result + '\n')
            f.write('*** Actual ***\n')
            f.write(oop_result + '\n')
            f.write('*** End ***\n')
            f.write('+++ PASSED' if passed else "--- FAILED")

        return passed

    def _join_non_blanks(self, lines):
        non_blanks = tuple(line.strip() for line in lines if line.strip() != '')
        return '\n'.join(non_blanks)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port_number = int(sys.argv[1])
    else:
        port_number = 10135

    timeout_seconds = 120
    debug_filter = None
    runner = TestRunnerServer(port_number)
    print('Starting listening for test folders on port', port_number)
    print('Will exit if recieved message is "EXIT" or if no message received in', timeout_seconds, 'seconds.')
    runner.start_listening(timeout_seconds)
