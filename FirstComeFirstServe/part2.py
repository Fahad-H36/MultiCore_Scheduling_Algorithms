import pandas as pd
import statistics



# Reading data from inputs file and deleting the Priority column as it is not important
df = pd.read_csv("inputs2.csv")



# seting up data in the format that will be used later on
d = df.set_index('Process_ID').T.to_dict('list')

# seting up variables for later calculations

resoucesArray = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
topLevelQueue = []

avrCPU = []
avrMemory = []
avrNumProcesses = []
VM_List = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]





# This function simulates the Multicore FIFO CPU scheduling algorithm,
# it takes NO arguments.
def FCFS():
    
    # Opening a text file in which Process_IDs of rejected tasks will be recorded
    rej_tasks = open('rejected_tasks2.txt', 'a')
    rej_tasks.write("\t\t\t REJECTED PROCESSES\n\nPROCESS_ID:")

    # Opening a text file in which Process_IDs of completed tasks will be recorded
    cmp_tasks = open('completed_tasks2.txt', 'a')
    cmp_tasks.write("\t\t\t COMPLETED PROCESSES\n\nPROCESS_ID:")


    # Opening a text file in which system_performance will be recorded
    performance = open('system_performance2.txt', 'a')

    # seting up variables for later use


    clock = 0
    executingTasks = []


    index = 0
    
    flag = True

    # This is the main loop that will stop when every process is delt with
    while (index < len(df) or len(executingTasks)!=0) or flag:
        

        # This conditional is to push the next process in the topLevelQueue queue if it's arrival time has come
        if index < len(df) and clock == df["Arrival_Time"][index]:
            topLevelQueue.append([df["Process_ID"][index], df["Arrival_Time"][index],  df["Execution_Time"][index], df["Memory_Percent"][index],df["CPU_Percent"][index]])

        # This conditional is to decide which VM gets the task, if any.
        if len(topLevelQueue)>0:    
            rejected = True
            for i in range(len(resoucesArray)):
                if 1 - resoucesArray[i][0] >= topLevelQueue[0][4] and 1 - resoucesArray[i][1] >= topLevelQueue[0][3] :
                    executingTasks.append([topLevelQueue[0][0], topLevelQueue[0][2], i])
                    VM_List[i].append(topLevelQueue[0][0])
                    resoucesArray[i][0] = resoucesArray[i][0]+topLevelQueue[0][4]
                    resoucesArray[i][1] = resoucesArray[i][1]+topLevelQueue[0][3]
                    rejected = False
                    topLevelQueue.pop(0)
                    print("PUSHED: "+str(df["Process_ID"][index]) + " " + str(df["Arrival_Time"][index]) + " " + str(clock) + " in VM_" + str(i+1))
                    flag = False
                    break
            
            # This Block is activated if a process is rejected
            if rejected:
                topLevelQueue.pop(0)
                print("rejected task {} Found".format(df["Process_ID"][index]))
                rej_tasks.write("\n" + str(df["Process_ID"][index]))
                                
            index+=1
                

        # This conditional is to pop a process out of queue if it is fully executed
        cmpIndex = 0
        clear = False
        while not clear:
            clear = True
            for i in range(cmpIndex, len(executingTasks)):
                if executingTasks[i][1] == 0:
                    t = executingTasks.pop(i)
                    VM_List[t[2]].remove(int(t[0]))
                    cmpIndex = i
                    resoucesArray[t[2]][0] -= d[t[0]][3]
                    resoucesArray[t[2]][1] -= d[t[0]][2]
                    print("Completed Task " + str(t[0]) + " in VM_" + str(t[2]))
                    cmp_tasks.write("\n" + str(t[0]))
                    clear=False
                    break
        
        # Decreamenting the execution time of each process under execution
        executingTasks = [[i[0], i[1]-1, i[2]] for i in executingTasks] 
        
        # Calculating Commulative Averages
        memoryList = [i[1] for i in resoucesArray]
        cpuList = [i[0] for i in resoucesArray]

        avrMemory.append(statistics.mean(memoryList))
        avrCPU.append(statistics.mean(cpuList))
        avrNumProcesses.append(statistics.mean([len(i) for i in VM_List]))


        clock+=1
        
    



    # # Writes all the required information in the text file
    performance.write("\n\n\nCOMMULATIVE AVERAGE CPU USAGE:    {}\n".format(statistics.mean(avrCPU)))
    performance.write("\n\n\nCOMMULATIVE AVERAGE MEMORY USAGE:    {}\n".format(statistics.mean(avrMemory)))
    performance.write("\n\n\nCOMMULATIVE AVERAGE NUMBER OF TASKS PER CPU:    {}\n".format(statistics.mean(avrNumProcesses)))
 



FCFS()
