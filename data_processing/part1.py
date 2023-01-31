import pandas as pd

# Reads data and write some proccessed information about it in a text file.




# Reading data from inputs file
df = pd.read_csv("inputs2.csv")


# df = df.sort_values(by=["Execution_Time"])



cpu_index = list(df["CPU_Percent"]).index(max(list(df["CPU_Percent"])))
memory_index = list(df["Memory_Percent"]).index(max(list(df["Memory_Percent"])))
    

# Opening a text file in which results will be recorded
the_file = open('results1.txt', 'a')

the_file.write(
    """PROCESS WITH MAX CPU USAGE:\n\n
    Process_ID: {}\n
    Arrival_Time: {}\n
    Execution_Time: {}\n
    Memory_Usage: {}\n
    CPU_Usage: {}""".format(list(df["Process_ID"])[cpu_index], list(df["Arrival_Time"])[cpu_index], list(df["Execution_Time"])[cpu_index], list(df["Memory_Percent"])[cpu_index], list(df["CPU_Percent"])[cpu_index])
    )

the_file.write(
    """\n\n\nPROCESS WITH MAX MEMORY USAGE:\n\n
    Process_ID: {}\n
    Arrival_Time: {}\n
    Execution_Time: {}\n
    Memory_Usage: {}\n
    CPU_Usage: {}""".format(list(df["Process_ID"])[memory_index], list(df["Arrival_Time"])[memory_index], list(df["Execution_Time"])[memory_index], list(df["Memory_Percent"])[memory_index], list(df["CPU_Percent"])[memory_index]))

the_file.close()
