"""this is the main part of the assignment"""

# Copyright Julian Trinh julest@bu.edu
# Copyright Emily Stern emistern@bu.edu
# Copyright Dennis Your dyour@bu.edu

import unittest
import subprocess
#import sys

# please change this to valid author emails
AUTHORS = ['julest@bu.edu', 'emistern@bu.edu', 'dyour@bu.edu']

PROGRAM_TO_TEST = "collision__0"


def runprogram(program, args, inputstr):
    ''' Runs the program, return -1 if can't'''
    try:
        coll_run = subprocess.run(
            [program, *args],
            input=inputstr.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=.2)
    except:
        return (-1, "", "")

    ret_code = coll_run.returncode
    program_output = coll_run.stdout.decode()
    program_errors = coll_run.stderr.decode()
    return (ret_code, program_output, program_errors)


def does_output_match_expected(output, expected_output):
    ''' Parse all lines from output and expected output to see if they match '''
    output_lines = output.split('\n')
    expected_lines = expected_output.split('\n')

    if len(output_lines) != len(expected_lines):
        return False

    # Extract induvidual lines into lists
    for index in range(0, len(expected_lines)):
        output_line = output_lines[index].split(" ")
        expected_line = expected_lines[index].split(" ")

        if len(output_line) != len(expected_line):
            return False

        if is_line_correct(output_line, expected_line) is False:
            return False

    return True


def is_line_correct(line, expected_line):
    ''' Compare lines and ensure that they syntactically similar and mathematically almost
        equal. Input variables are lists that represent a space-delimited line '''
    for index in range(0, len(expected_line)):
        word = line[index]
        expected_word = expected_line[index]
        # If the word strings are not equal, see if its because of float rounding
        if word != expected_word:
            # If the expected word is not a number, then the comparison is just wrong
            if is_number(expected_word) is False:
                return False

            # If the expected word is a number, but the input line is not, then its wrong
            if is_number(word) is False:
                return False

            # Otherwise, check if the absolute difference if the values is small enough
            if abs(float(word) - float(expected_word)) > 0.000001:
                return False

    return True


def is_number(num):
    try:
        float(num)
        return True
    except:
        return False


class CollisionTestCase(unittest.TestCase):
    '''test cases'''
    def test_missing_initial_coords(self):
        ''' Test first set of coordinates '''
        strin = "one 0 0"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 1)
        self.assertEqual(out, "")

    def test_missing_2nd_initial_coords(self):
        ''' Test second coordinates'''
        strin = "one 0 0 0 1\ntwo 5 5"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 1)
        self.assertEqual(out, "")

    def test_only_id_for_stdin(self):
        ''' Test only id'''
        strin = "one"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 1)
        self.assertEqual(out, "")

    def test_two_missing_initial_coords(self):
        ''' Test missing coord'''
        strin = "one 0 0\ntwo 0 0"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 1)
        self.assertEqual(out, "")

    def test_too_many_stdin_inputs(self):
        ''' Test too many inputs'''
        strin = "one 0 0 10 10 10 10 10 10 10"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 1)
        self.assertEqual(out, "")

    def test_two_too_many_stdin_inputs(self):
        ''' Test two sets of too many inputs'''
        strin = "one 0 0 10 10 10 10 10 10 10\ntwo 10 10 10 10 10 10 10 10 10"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 1)
        self.assertEqual(out, "")

    def test_non_numeric_cmd(self):
        ''' Test non numeric '''
        strin = "one 0 0 1 0"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["x"], strin)
        self.assertEqual(return_code, 2)
        self.assertEqual(out, "")

    def test_two_non_numeric_cmd(self):
        ''' Test two non numeric'''
        strin = "one 0 0 1 0"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["x", "y", "z"], strin)
        self.assertEqual(return_code, 2)
        self.assertEqual(out, "")

    def test_no_cmd(self):
        ''' Test no command'''
        strin = "one 0 0 1 0"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, [""], strin)
        self.assertEqual(return_code, 2)
        self.assertEqual(out, "")

    def test_no_stdin(self):
        ''' Test no standard in'''
        strin = ""
        correct_out = "10\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_bad_initial_pos(self):
        ''' Test bad initial pos'''
        strin = "one 0 one 1 0"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 1)
        self.assertEqual(out, "")

    def test_non_unique_stdin_id(self):
        ''' Test non unique stdin id'''
        strin = "one 0 0 1 0\none 20 0 0 1"
        correct_out = ("1"
                       "\none 1 0 1 0"
                       "\none 20 1 0 1"
                       "\n2"
                       "\none 2 0 1 0"
                       "\none 20 2 0 1"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["1", "2"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_really_large_time_stamps(self):
        ''' Test large time stamp'''
        strin = "one 0 0 1 0"
        correct_out = ("10000"
                       "\none 10000 0 1 0"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10000"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_really_large_names(self):
        ''' Test really large names'''
        strin = ("onetwothreefourfivesix"
                 "seveneightnineteneleven"
                 "twelvethirteenfourteenfifteen 0 0 1 0")
        correct_out = ("10000"
                       "\nonetwothreefourfivesix"
                       "seveneightnineteneleven"
                       "twelvethirteenfourteenfifteen 10000 0 1 0"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10000"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_really_small_time_stamps(self):
        ''' Test small time stamp'''
        strin = "one 0 0 1 0"
        correct_out = ("0.00021"
                       "\none 0.00021 0 1 0"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["0.00021"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_scientific_notation_large(self):
        ''' Test large scientific notation'''
        strin = "one 0 0 1 0"
        correct_out = ("2.1e+21"
                       "\none 2.1e+21 0 1 0"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["2.1e+21"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_scientific_notation_small(self):
        ''' Test small scientific notation'''
        strin = "one 0 0 1 0"
        correct_out = ("2.1e-21"
                       "\none 2.1e-21 0 1 0"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["2.1e-21"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_positive_symbol(self):
        ''' Test plus sign'''
        strin = "one 0 0 1 0"
        correct_out = ("1"
                       "\none 1 0 1 0"
                       "\n2"
                       "\none 2 0 1 0"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["1", "+2"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_negative_symbol(self):
        ''' Test negative sign'''
        strin = "one 0 0 1 0"
        correct_out = ("1"
                       "\none 1 0 1 0"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["1", "-2"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_int_float_timestamps(self):
        ''' Test float+int timestamp'''
        strin = "one 0 0 1 0"
        correct_out = ("1"
                       "\none 1 0 1 0"
                       "\n1.5"
                       "\none 1.5 0 1 0"
                       "\n2"
                       "\none 2 0 1 0"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["1", "1.5", "2"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_same_time_stamps(self):
        ''' Test same timestamp'''
        strin = "one 0 0 1 0"
        correct_out = ("1"
                       "\none 1 0 1 0"
                       "\n1"
                       "\none 1 0 1 0"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["1", "1"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_number_id_name(self):
        ''' Test name as number'''
        strin = "1 0 0 1 0"
        correct_out = ("1"
                       "\n1 1 0 1 0"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["1"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_single_x_velocity(self):
        ''' Test x velocity'''
        strin = "one 0 0 1 0"
        correct_out = ("10"
                       "\none 10 0 1 0"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_single_x_leading_zero(self):
        ''' Test pad 0 timestamp'''
        strin = "one 0 0 1 0"
        correct_out = ("10"
                       "\none 10 0 1 0"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["0000000010"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_single_x_two_timestamps(self):
        ''' Test x velocity 2 timestamp'''
        strin = "one 0 0 1 0"
        correct_out = ("2"
                       "\none 2 0 1 0"
                       "\n4"
                       "\none 4 0 1 0"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["2", "4"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_single_x_three_timestamps(self):
        ''' Test 3 timestamp'''
        strin = "one 0 0 1 0"
        correct_out = "2\none 2 0 1 0\n4\none 4 0 1 0\n6\none 6 0 1 0\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["2", "4", "6"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_single_y_velocity(self):
        ''' Test y velocity'''
        strin = "one 0 0 0 1"
        correct_out = "10\none 0 10 0 1\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_single_x_neg_velocity(self):
        ''' Test neg velocity'''
        strin = "one 0 0 0 -1"
        correct_out = "10\none 0 -10 0 -1\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_single_y_neg_velocity(self):
        ''' Test neg velocity'''
        strin = "one 0 0 -1 0"
        correct_out = "10\none -10 0 -1 0\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_single_x_y_velocity(self):
        ''' Test xy velocity'''
        strin = "one 0 0 1 1"
        correct_out = "10\none 10 10 1 1\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_single_x_y_float_timestamp(self):
        ''' Test xy velocity float timestamp'''
        strin = "one 0 0 1 1"
        correct_out = "5.7\none 5.7 5.7 1 1\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["5.7"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_one_xy_floattime_w_zeros(self):
        ''' Test xy velocity float timestamp leading zero'''
        strin = "one 0 0 1 1"
        correct_out = "5.7\none 5.7 5.7 1 1\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["00000005.7"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_single_x_y_velocity_float(self):
        ''' Test xy float'''
        strin = "one 0 0 .1 .1"
        correct_out = "10\none 1 1 0.1 0.1\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_single_xy_not_ordered_time(self):
        ''' Test non consecutive timestamps'''
        strin = "one 0 0 1 1"
        correct_out = ("3"
                       "\none 3 3 1 1"
                       "\n10"
                       "\none 10 10 1 1"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10", "3"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_single_x_y_neg_timestamp(self):
        ''' Test xy neg timestamp'''
        strin = "one 0 0 1 1"
        correct_out = "10\none 10 10 1 1\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["-2", "10"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_single_xy_neg_float_time(self):
        ''' Test xy neg float timestamp'''
        strin = "one 0 0 1 1"
        correct_out = "10\none 10 10 1 1\n"
        (return_code, out, errs) = runprogram(
            PROGRAM_TO_TEST, ["-2", "10", "-6.7"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_single_x_y_neg_timestamps(self):
        ''' Test xy neg timestamp more'''
        strin = "one 0 0 1 1"
        correct_out = "10\none 10 10 1 1\n"
        (return_code, out, errs) = runprogram(
            PROGRAM_TO_TEST, ["-2", "10", "-5"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_one_correct_initial(self):
        ''' Test single correct initial conditions'''
        strin = "one 0 0 1 1"
        correct_out = "0\none 0 0 1 1\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["0"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_two_correct_initial(self):
        ''' Test two correct initial conditions'''
        strin = "one 0 0 1 1\ntwo 10 10 1 1"
        correct_out = ("0"
                       "\none 0 0 1 1"
                       "\ntwo 10 10 1 1"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["0"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_two_no_collision(self):
        ''' Test no collision'''
        strin = "one 10 10 0 1\ntwo 0 0 1 0"
        correct_out = ("2"
                       "\none 10 12 0 1"
                       "\ntwo 2 0 1 0"
                       "\n200"
                       "\none 10 210 0 1"
                       "\ntwo 200 0 1 0"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["2", "200"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_two_x_plane_collision(self):
        ''' Test two x plane collision'''
        strin = "one -10 0 1 0\ntwo 10 0 -1 0"
        correct_out = ("1"
                       "\none -9 0 1 0"
                       "\ntwo 9 0 -1 0"
                       "\n5"
                       "\none -5 0 -1 0"
                       "\ntwo 5 0 1 0"
                       "\n6"
                       "\none -6 0 -1 0"
                       "\ntwo 6 0 1 0"
                       "\n10"
                       "\none -10 0 -1 0"
                       "\ntwo 10 0 1 0"
                       "\n")
        (return_code, out, errs) = runprogram(
            PROGRAM_TO_TEST, ["1", "5", "6", "10"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_two_y_plane_collision(self):
        ''' Test 2 y plane collision'''
        strin = "one 0 -10 0 1\ntwo 0 10 0 -1"
        correct_out = ("1"
                       "\none 0 -9 0 1"
                       "\ntwo 0 9 0 -1"
                       "\n5"
                       "\none 0 -5 0 -1"
                       "\ntwo 0 5 0 1"
                       "\n6"
                       "\none 0 -6 0 -1"
                       "\ntwo 0 6 0 1"
                       "\n10"
                       "\none 0 -10 0 -1"
                       "\ntwo 0 10 0 1"
                       "\n")
        (return_code, out, errs) = runprogram(
            PROGRAM_TO_TEST, ["1", "5", "6", "10"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_five_newton_balls_x_plane(self):
        ''' Test newton balls x plane'''
        strin = ("one -80 0 3 0"
                 "\ntwo -60 0 0 0"
                 "\nthree -40 0 0 0"
                 "\nfour -20 0 0 0"
                 "\nfive 0 0 0 0")
        correct_out = ("1"
                       "\none -77 0 3 0"
                       "\ntwo -60 0 0 0"
                       "\nthree -40 0 0 0"
                       "\nfour -20 0 0 0"
                       "\nfive 0 0 0 0"
                       "\n3"
                       "\none -71 0 3 0"
                       "\ntwo -60 0 0 0"
                       "\nthree -40 0 0 0"
                       "\nfour -20 0 0 0"
                       "\nfive 0 0 0 0"
                       "\n5"
                       "\none -70 0 0 0"
                       "\ntwo -55 0 3 0"
                       "\nthree -40 0 0 0"
                       "\nfour -20 0 0 0"
                       "\nfive 0 0 0 0"
                       "\n7"
                       "\none -70 0 0 0"
                       "\ntwo -50 0 0 0"
                       "\nthree -39 0 3 0"
                       "\nfour -20 0 0 0"
                       "\nfive 0 0 0 0"
                       "\n9"
                       "\none -70 0 0 0"
                       "\ntwo -50 0 0 0"
                       "\nthree -33 0 3 0"
                       "\nfour -20 0 0 0"
                       "\nfive 0 0 0 0"
                       "\n11"
                       "\none -70 0 0 0"
                       "\ntwo -50 0 0 0"
                       "\nthree -30 0 0 0"
                       "\nfour -17 0 3 0"
                       "\nfive 0 0 0 0"
                       "\n13"
                       "\none -70 0 0 0"
                       "\ntwo -50 0 0 0"
                       "\nthree -30 0 0 0"
                       "\nfour -11 0 3 0"
                       "\nfive 0 0 0 0"
                       "\n15"
                       "\none -70 0 0 0"
                       "\ntwo -50 0 0 0"
                       "\nthree -30 0 0 0"
                       "\nfour -10 0 0 0"
                       "\nfive 5 0 3 0"
                       "\n")

        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, [
            "1", "3", "5", "7", "9", "11", "13", "15"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_five_newton_balls_y_plane(self):
        ''' Test newton balls y plane'''
        strin = ("one 0 -80 0 3"
                 "\ntwo 0 -60 0 0"
                 "\nthree 0 -40 0 0"
                 "\nfour 0 -20 0 0"
                 "\nfive 0 0 0 0")
        correct_out = ("1"
                       "\none 0 -77 0 3"
                       "\ntwo 0 -60 0 0"
                       "\nthree 0 -40 0 0"
                       "\nfour 0 -20 0 0"
                       "\nfive 0 0 0 0"
                       "\n3"
                       "\none 0 -71 0 3"
                       "\ntwo 0 -60 0 0"
                       "\nthree 0 -40 0 0"
                       "\nfour 0 -20 0 0"
                       "\nfive 0 0 0 0"
                       "\n5"
                       "\none 0 -70 0 0"
                       "\ntwo 0 -55 0 3"
                       "\nthree 0 -40 0 0"
                       "\nfour 0 -20 0 0"
                       "\nfive 0 0 0 0"
                       "\n7"
                       "\none 0 -70 0 0"
                       "\ntwo 0 -50 0 0"
                       "\nthree 0 -39 0 3"
                       "\nfour 0 -20 0 0"
                       "\nfive 0 0 0 0"
                       "\n9"
                       "\none 0 -70 0 0"
                       "\ntwo 0 -50 0 0"
                       "\nthree 0 -33 0 3"
                       "\nfour 0 -20 0 0"
                       "\nfive 0 0 0 0"
                       "\n11"
                       "\none 0 -70 0 0"
                       "\ntwo 0 -50 0 0"
                       "\nthree 0 -30 0 0"
                       "\nfour 0 -17 0 3"
                       "\nfive 0 0 0 0"
                       "\n13"
                       "\none 0 -70 0 0"
                       "\ntwo 0 -50 0 0"
                       "\nthree 0 -30 0 0"
                       "\nfour 0 -11 0 3"
                       "\nfive 0 0 0 0"
                       "\n15"
                       "\none 0 -70 0 0"
                       "\ntwo 0 -50 0 0"
                       "\nthree 0 -30 0 0"
                       "\nfour 0 -10 0 0"
                       "\nfive 0 5 0 3"
                       "\n")

        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, [
            "1", "3", "5", "7", "9", "11", "13", "15"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_fastball(self):
        ''' Test fastball'''
        strin = ("one 0 0 1000 0"
                 "\ntwo 15 0 0 0"
                 "\nthree 30 0 0 0"
                 "\nfour 45 0 0 0")
        correct_out = ("1"
                       "\none 5 0 0 0"
                       "\ntwo 20 0 0 0"
                       "\nthree 35 0 0 0"
                       "\nfour 1030 0 1000 0"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["1"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_superfastball(self):
        ''' Test superfastball'''
        strin = ("one 0 0 100000000 0"
                 "\ntwo 15 0 0 0"
                 "\nthree 30 0 0 0"
                 "\nfour 45 0 0 0")
        correct_out = ("1"
                       "\none 5 0 0 0"
                       "\ntwo 20 0 0 0"
                       "\nthree 35 0 0 0"
                       "\nfour 100000030 0 100000000 0"
                       "\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["1"], strin)
        self.assertEqual(return_code, 0)
        # if not does_output_match_expected(out, correct_out):
        #     print(PROGRAM_TO_TEST, file=sys.stderr)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_one_ball(self):
        ''' Test one ball'''
        strin = "one 20 10 -2 1"
        correct_out = "3\none 14 13 -2 1\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["3"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_null_input(self):
        ''' Test null input'''
        strin = ""
        #correct_out = ""
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, [""], strin)
        self.assertEqual(return_code, 2)
        #self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(out, "")

    def test_bad_times(self):
        ''' Test bad time'''
        strin = "one 20 10 -2 1"
        #correct_out = ""
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["cheese"], strin)
        self.assertEqual(return_code, 2)
        #self.assertTrue(does_output_match_expected(out, correct_out))
        # self.assertEqual(errs,"")

    def test_bad_coords(self):
        ''' Test bad coord'''
        strin = "one 20 10 -2 1 1 1 1 cat"
        #correct_out = ""
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["3"], strin)
        self.assertEqual(return_code, 1)
        # self.assertTrue(does_output_match_expected(out, correct_out))
        # self.assertEqual(errs,"")

    def test_mass_input(self):
        ''' Test mass input'''
        strin = ("one 0 0 0 0\ntwo 10 0 0 0\nthree 20 0 0 0\n"
                 "four 30 0 0 0\nfive 40 0 0 0\nsix 50 0 0 0\n"
                 "seven 60 0 0 0\neight 70 0 0 0\nnine 80 0 0 0\n"
                 "ten 90 0 0 0\neleven 100 0 0 0")
        correct_out = ("10\none 0 0 0 0\ntwo 10 0 0 0\nthree 20 0 0 0\n"
                       "four 30 0 0 0\nfive 40 0 0 0\nsix 50 0 0 0\n"
                       "seven 60 0 0 0\neight 70 0 0 0\nnine 80 0 0 0\n"
                       "ten 90 0 0 0\neleven 100 0 0 0\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_position_max(self):
        ''' Test large positions'''
        strin = ("Q1 100000 100000 1 1\nQ2 -100000 100000 1 1\n"
                 "Q3 -100000 -100000 1 1\nQ4 100000 -100000 1 1")
        correct_out = ("3\nQ1 100003 100003 1 1\nQ2 -99997 100003 1 1\n"
                       "Q3 -99997 -99997 1 1\nQ4 100003 -99997 1 1\n")
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["3"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_neg_horizontal(self):
        ''' Test negative horizontal'''
        strin = "one 0 0 -1 0\ntwo -15 0 0 0"
        correct_out = "10\none -5 0 0 0\ntwo -20 0 -1 0\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_horizontal(self):
        ''' Test horizontal'''
        strin = "one 0 0 1 0\ntwo 15 0 0 0"
        correct_out = "10\none 5 0 0 0\ntwo 20 0 1 0\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_no_movement(self):
        ''' Test no move'''
        strin = "one 10 0 0 0\ntwo 20 0 0 0"
        correct_out = "3\none 10 0 0 0\ntwo 20 0 0 0\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["3"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_neg_vertical(self):
        ''' Test neg vertical'''
        strin = "one 0 0 0 -1\ntwo 0 -15 0 0"
        correct_out = "10\none 0 -5 0 0\ntwo 0 -20 0 -1\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_vertical(self):
        ''' Test vertical'''
        strin = "one 0 0 0 1\ntwo 0 15 0 0"
        correct_out = "10\none 0 5 0 0\ntwo 0 20 0 1\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["10"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    def test_head_on(self):
        ''' Test head on collision'''
        strin = "one 0 -10 0 5\ntwo 0 10 0 -5"
        correct_out = "2\none 0 -10 0 -5\ntwo 0 10 0 5\n"
        (return_code, out, errs) = runprogram(PROGRAM_TO_TEST, ["2"], strin)
        self.assertEqual(return_code, 0)
        self.assertTrue(does_output_match_expected(out, correct_out))
        self.assertEqual(errs, "")

    # potentially might need to add one that the balls just skim each other but don't actually hit


def main():
    ''' Main method in case '''
    unittest.main()


if __name__ == '__main__':
    main()
