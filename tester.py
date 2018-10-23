"""this is the main part of the assignment"""

# Copyright Julian Trinh julest@bu.edu
import unittest
import subprocess

#please change this to valid author emails
AUTHORS = ['julest@bu.edu']

PROGRAM_TO_TEST = "collisionc_0"

def runprogram(program, args, inputstr):
    try:
        coll_run = subprocess.run(
        [program, *args],
        input=inputstr.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=1)
    except:
        return (-1, "", "")

    ret_code = coll_run.returncode
    program_output = coll_run.stdout.decode()
    program_errors = coll_run.stderr.decode()
    return (ret_code, program_output, program_errors)

class CollisionTestCase(unittest.TestCase):
    def test_missing_initial_coordinates(self):
        strin = "one 0 0"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["10"],strin)
        self.assertEqual(rc,1)

    def test_missing_second_initial_coordinates(self):
        strin = "one 0 0 0 1\ntwo 5 5"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["10"],strin)
        self.assertEqual(rc,1)

    def test_only_id_for_stdin(self):
        strin = "one"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["10"],strin)
        self.assertEqual(rc,1)

    def test_two_missing_initial_coordinates(self):
        strin = "one 0 0\ntwo 0 0"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["10"],strin)
        self.assertEqual(rc,1)

    def test_too_many_stdin_inputs(self):
        strin = "one 0 0 10 10 10 10 10 10 10"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["10"],strin)
        self.assertEqual(rc,1)

    def test_two_too_many_stdin_inputs(self):
        strin = "one 0 0 10 10 10 10 10 10 10\ntwo 10 10 10 10 10 10 10 10 10"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["10"],strin)
        self.assertEqual(rc,1)

    def test_non_numeric_cmd(self):
        strin = "one 0 0 1 0"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["x"],strin)
        self.assertEqual(rc,2)

    def test_two_non_numeric_cmd(self):
        strin = "one 0 0 1 0"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["x", "y", "z"],strin)
        self.assertEqual(rc,2)

    def test_no_cmd(self):
        strin = "one 0 0 1 0"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,[""],strin)
        self.assertEqual(rc,2)

    def test_no_stdin(self):
        strin = ""
        correct_out="10\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["10"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_single_x_velocity(self):
        strin = "one 0 0 1 0"
        correct_out = ("10"
                    "\none 10 0 1 0"
                    "\n")
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["10"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_single_x_velocity_leading_zero_timestamp(self):
        strin = "one 0 0 1 0"
        correct_out = ("10"
                    "\none 10 0 1 0"
                    "\n")
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["0000000010"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_single_x_velocity_two_timestamps(self):
        strin = "one 0 0 1 0"
        correct_out = ("2"
                    "\none 2 0 1 0"
                    "\n4"
                    "\none 4 0 1 0"
                    "\n")
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["2","4"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_single_x_velocity_three_timestamps(self):
        strin = "one 0 0 1 0"
        correct_out = "2\none 2 0 1 0\n4\none 4 0 1 0\n6\none 6 0 1 0\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["2","4","6"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_single_y_velocity(self):
        strin = "one 0 0 0 1"
        correct_out = "10\none 0 10 0 1\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["10"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_single_x_neg_velocity(self):
        strin = "one 0 0 0 -1"
        correct_out = "10\none 0 -10 0 -1\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["10"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_single_y_neg_velocity(self):
        strin = "one 0 0 -1 0"
        correct_out = "10\none -10 0 -1 0\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["10"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_single_x_y_velocity(self):
        strin = "one 0 0 1 1"
        correct_out = "10\none 10 10 1 1\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["10"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_single_x_y_velocity_float_timestamp(self):
        strin = "one 0 0 1 1"
        correct_out = "5.7\none 5.7 5.7 1 1\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["5.7"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_single_x_y_velocity_float_timestamp_leading_zeros(self):
        strin = "one 0 0 1 1"
        correct_out = "5.7\none 5.7 5.7 1 1\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["00000005.7"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_single_x_y_velocity_float(self):
        strin = "one 0 0 .1 .1"
        correct_out = "10\none 1 1 0.1 0.1\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["10"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_single_x_y_velocity_non_consecutive_timestamp(self):
        strin = "one 0 0 1 1"
        correct_out = ("3"
                    "\none 3 3 1 1"
                    "\n10"
                    "\none 10 10 1 1"
                    "\n")
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["10", "3"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_single_x_y_velocity_neg_timestamp(self):
        strin = "one 0 0 1 1"
        correct_out = "10\none 10 10 1 1\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["-2", "10"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_single_x_y_velocity_neg_float_timestamp(self):
        strin = "one 0 0 1 1"
        correct_out = "10\none 10 10 1 1\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["-2", "10", "-6.7"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_single_x_y_velocity_neg_timestamps(self):
        strin = "one 0 0 1 1"
        correct_out = "10\none 10 10 1 1\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["-2", "10", "-5"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_single_correct_initial_conditions(self):
        strin = "one 0 0 1 1"
        correct_out = "0\none 0 0 1 1\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["0"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_two_correct_initial_conditions(self):
        strin = "one 0 0 1 1\ntwo 10 10 1 1"
        correct_out = ("0"
                    "\none 0 0 1 1"
                    "\ntwo 10 10 1 1"
                    "\n")
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["0"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_two_no_collision(self):
        strin = "one 10 10 0 1\ntwo 0 0 1 0"
        correct_out = ("2"
                    "\none 10 12 0 1"
                    "\ntwo 2 0 1 0"
                    "\n200"
                    "\none 10 210 0 1"
                    "\ntwo 200 0 1 0"
                    "\n")
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["2", "200"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_two_x_plane_collision(self):
        strin = "one -10 0 1 0\ntwo 10 0 -1 0"
        correct_out = ("1"
                    "\none -9 0 1 0"
                    "\ntwo 9 0 -1 0"
                    "\n5"
                    "\none -5 0 1 0"
                    "\ntwo 5 0 -1 0"
                    "\n6"
                    "\none -6 0 -1 0"
                    "\ntwo 6 0 1 0"
                    "\n10"
                    "\none -10 0 -1 0"
                    "\ntwo 10 0 1 0"
                    "\n")
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["1","5","6","10"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_two_y_plane_collision(self):
        strin = "one 0 -10 0 1\ntwo 0 10 0 -1"
        correct_out = ("1"
                    "\none 0 -9 0 1"
                    "\ntwo 0 9 0 -1"
                    "\n5"
                    "\none 0 -5 0 1"
                    "\ntwo 0 5 0 -1"
                    "\n6"
                    "\none 0 -6 0 -1"
                    "\ntwo 0 6 0 1"
                    "\n10"
                    "\none 0 -10 0 -1"
                    "\ntwo 0 10 0 1"
                    "\n")
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["1","5","6","10"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_five_newton_balls_x_plane(self):
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
                    "\nfour -10 0 4.4408921e-16 0"
                    "\nfive 5 0 3 0"
                    "\n")

        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["1","3","5","7","9","11","13","15"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_five_newton_balls_y_plane(self):
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
                    "\nfour 0 -10 0 4.4408921e-16"
                    "\nfive 0 5 0 3"
                    "\n")

        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["1","3","5","7","9","11","13","15"],strin)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

def main():
    unittest.main()

if __name__ == '__main__':
    main()

