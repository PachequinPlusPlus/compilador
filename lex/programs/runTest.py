import glob
import os
import sys

def main():
    fails = glob.glob("./fail/*")
    succ = glob.glob("./success/*")

    configs = open("../../logs/config", "r")

    times = int(configs.read())
    configs.close()

    configW = open("../../logs/config", "w")

    for arch in fails:
        failed = False
        try:
            print("running test # {}".format(times))
            print("expecting to throw\n")
            times = times+1
            os.system("python3 ../PPCDSALVC.py {} {}".format(arch, "./../../logs/err.txt") )
        except:
            print("SUCCESS: the program failed as expected, check logs. Program : {}\n".format(arch))
            failed = True

        if failed == False:
            print("FAILURE: the program was suppose to throw but it didnt. program : {}\n".format(arch))

            


    for arch in succ:
        failed = False
        try:
            print("running test # {}".format(times))
            print("expecting NOT to throw\n")
            times = self.times+1
            os.system("python3 ../PPCDSALVC.py {} {}".format(arch, "./../../logs/err.txt") )
        except:
            print("FAILURE: the program failed but it wasnt suppose to throw, check logs. Program : {}\n".format(arch))
            failed = True

        if failed == False:
            print("SUCCESS: the program didnt throw as expected. program : {}\n".format(arch))

    configW.write(str(times)+"\n")
    configW.close()


if __name__ == "__main__":
    main()

