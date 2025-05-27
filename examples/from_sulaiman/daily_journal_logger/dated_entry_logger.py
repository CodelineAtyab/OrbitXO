import datetime
import sys

if 1 < len(sys.argv):
    path = "examples/from_sulaiman/daily_journal_logger/logger.txt"
    if sys.argv[1] == "read":
        try:
            logger = open(path, "r")
            list_logs = logger.readlines()
            if len(sys.argv) == 2:
                for logs in list_logs:
                    print(logs[:-2])
            elif len(sys.argv) == 3:
                for log in list_logs:
                    if sys.argv[2] == log[:10]:
                        print(log[:-1])
            else:
                print("1 argument for reading the whole")
            logger.close()
        except FileNotFoundError:
            print("File not found")

    if sys.argv[1] == "search":
        if len(sys.argv) != 3:
            print("Invalid number of arguments, your second argument should be the keyword for searching")
        else:
            try:
                logger = open(path, "r")
                list_logs = logger.readlines()
                count = 1
                for log in list_logs:
                    if sys.argv[2] in log[log.rfind(":")+1:]:
                        print(str(count) + ". " + log[:-1])
                        count+=1
                logger.close()

            except FileNotFoundError:
                print("File not found")

    if sys.argv[1] == "write":
        if len(sys.argv) != 3:
            print("Invalid number of arguments, you need at least 2 for writing")
        else:
            try:
                logger = open(path, "a")
                logger.write(str(datetime.datetime.now()) + ":" + sys.argv[2] + "\n")
                
                logger.close()

            except FileNotFoundError:
                print("File not found")
else:
    print("invalid number of arguments")