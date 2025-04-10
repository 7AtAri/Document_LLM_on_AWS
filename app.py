# simple python application as a first test to deploy on AWS Fargate
import time 

def main():
    print("Running app on Fargate!")
    time.sleep(300) # so that there are actually some logs from this short task

if __name__ == "__main__":
    main()
