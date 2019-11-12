import glob
import os
import sys

def main():
    fails = glob.glob("./fail/*")
    succ = glob.glob("./success/*")


    times = 1


    for arch in fails:
        failed = False
        print("running test # {}".format(times))
        print("expecting to throw\n")
        val = os.system("python3 ./../PPCDSALVC.py {} {}".format(arch, "./../../logs/err.txt") )
        if val != 0:
            print('\33[42m' + "SUCCESS TEST #{}: the program failed as expected, check logs. Program : {}\33[0m\n".format(times, arch))
            failed = True

        if failed == False:
            print('\33[41m'+"FAILURE TEST #{}: the program was suppose to throw but it didnt. program : {}\33[0m\n".format(times, arch))
        times = times+1
            


    for arch in succ:
        failed = False
        print("running test # {}".format(times))
        print("expecting NOT to throw\n")
        val = os.system("python3 ./../PPCDSALVC.py {} {}".format(arch, "./../../logs/err.txt") )
        if val != 0:
            print('\33[41m'+"FAILURE TEST #{}: the program failed but it wasnt suppose to throw, check logs. Program : {}\33[0m\n".format(times, arch))
            failed = True

        if failed == False:
            print('\33[42m'+"SUCCESS TEST #{}: the program didnt throw as expected. program : {}\33[0m\n".format(times, arch))
        times = times+1



if __name__ == "__main__":
    main()

