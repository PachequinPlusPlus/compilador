import glob
import os
import sys

def main():
    fails = glob.glob("./fail/*")
    succ = glob.glob("./success/*")

    LOGS = "./../../logs/err.txt"
    QUADS = "./../../quad/"

    EXECUTABLE_PATH = "./../PPCDSALVC.py"

    

    #number of test
    times = 1


    for arch in fails:
        failed = False
        print(f"running test # {times}")
        print("expecting to throw\n")
        val = os.system(f"python3 {EXECUTABLE_PATH} --programa {arch} --logs {LOGS} --quads {QUADS}")
        if val != 0:
            print('\33[42m' + f"SUCCESS TEST #{times}: the program failed as expected, check logs. Program : {arch}\33[0m\n")
            failed = True

        if failed == False:
            print('\33[41m'+ f"FAILURE TEST #{times}: the program was suppose to throw but it didnt. program : {arch}\33[0m\n")
        times = times+1
            


    for arch in succ:
        failed = False
        print(f"running test # {times}")
        print("expecting NOT to throw\n")
        val = os.system(f"python3 {EXECUTABLE_PATH} --programa {arch} --logs {LOGS} --quads {QUADS}")
        if val != 0:
            print('\33[41m'+ f"FAILURE TEST #{times}: the program failed but it wasnt suppose to throw, check logs. Program : {arch}\33[0m\n")
            failed = True

        if failed == False:
            print('\33[42m'+ f"SUCCESS TEST #{times}: the program didnt throw as expected. program : {arch}\33[0m\n")
        times = times+1



if __name__ == "__main__":
    main()

