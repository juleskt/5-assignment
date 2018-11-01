""" Check all collision programs, record pass/fail

Using the tester (YOU must finish tester), check
all executable collision programs for correctness.

This program is provided to you 
as a service, so that you can focus on writing your
test suite not have to learn the json and glob modules
"""
import unittest
import importlib
import glob
import io
import sys
import json

import tester

SUPPRESS_OUTPUT = True


def check_all_files():
    overall_results={}

    Programs = glob.glob('collision__*')
    print(len(Programs),'programs to be tested.')
    for file_name in Programs:
        loader = unittest.loader.TestLoader()
        results = unittest.result.TestResult()

        try:

            if SUPPRESS_OUTPUT:
                s = io.StringIO()
                sys.stdout = s

            tester.PROGRAM_TO_TEST = file_name

            tests = loader.loadTestsFromTestCase(
                tester.CollisionTestCase)

            tests.run(results)


            overall_results[file_name]={'run':results.testsRun,'failures':len(results.failures),'errors':len(results.errors)}
            
            if SUPPRESS_OUTPUT:
                sys.stdout = sys.__stdout__

        except Exception as e:
            if SUPPRESS_OUTPUT:
                sys.stdout = sys.__stdout__

            print('exception', file_name, e)
            overall_results[file_name]={'exception':str(e)}
 

    return overall_results


if __name__ == "__main__":
    results =  check_all_files()
    passed = {x:results[x] for x in results if not results[x]['failures'] and not results[x]['errors']}
    failed = {x:results[x] for x in results if results[x]['failures'] or results[x]['errors']}
    print(len(passed),'passed')
    print(len(failed),'failed')
    with open('tester_results.json', 'w') as f:
        output_obj = {'failed':failed,'passed':passed,'authors':tester.AUTHORS}
        json.dump(output_obj, f, indent=4)
