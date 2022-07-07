"""
Plots cores vs time collected from output/timings.txt generated by Assignment3.sh
"""
import matplotlib.pyplot as plt

def plotter(file):
    """
    Reads in the thread-time file and creates timings.png
    Threads are on the x axis
    Times are on the y axis
    """
    threadtimes = []

    with open(file, "r", encoding = "utf8") as data:
        for line in data:
            if line[0].isdigit():
                threadtimes.append(line.strip().split(":"))
    
    plt.scatter([x[0] for x in threadtimes], [x[1] for x in threadtimes])
    plt.title("Time vs number of threads")
    plt.xlabel("Number of threads")
    plt.ylabel("Running time")
    plt.savefig("output/timings.png")

if __name__ == "__main__":
    plotter("output/timings.txt")