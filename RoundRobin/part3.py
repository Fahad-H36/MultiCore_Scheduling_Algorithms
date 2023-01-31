import pandas as pd
import statistics
import sys



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
def RoundRobin():
    
    # Opening a text file in which Process_IDs of rejected tasks will be recorded
    rej_tasks = open('rejected_tasks3.txt', 'a')
    rej_tasks.write("\t\t\t REJECTED PROCESSES\n\nPROCESS_ID:")

    # Opening a text file in which Process_IDs of completed tasks will be recorded
    cmp_tasks = open('completed_tasks3.txt', 'a')
    cmp_tasks.write("\t\t\t COMPLETED PROCESSES\n\nPROCESS_ID:")


    # Opening a text file in which system_performance will be recorded
    performance = open('system_performance3.txt', 'a')

    # seting up variables for later use
    j = 0
    lastVM = 15

    clock = 0
    executingTasks = []


    index = 0
    flag = True

    # This is the main loop that will stop when every process is delt with
    while (index < len(df) or len(executingTasks)!=0 or len(topLevelQueue)!=0) or flag:
        

        # This conditional is to push the next process in the topLevelQueue queue if it's arrival time has come
        if index < len(df) and clock == df["Arrival_Time"][index]:
            topLevelQueue.append([df["Process_ID"][index], df["Arrival_Time"][index],  df["Execution_Time"][index], df["Memory_Percent"][index],df["CPU_Percent"][index]])
            index+=1

        # This conditional is to decide which VM gets the task, if any.
        if len(topLevelQueue)>0:    
            rejected = True
            breakLoop = False

            while not breakLoop:
                
                if j == lastVM:
                    breakLoop = True

                if 1 - resoucesArray[j][0] >= topLevelQueue[0][4] and 1 - resoucesArray[j][1] >= topLevelQueue[0][3] :
                    executingTasks.append([topLevelQueue[0][0], topLevelQueue[0][2], j])
                    VM_List[j].append(topLevelQueue[0][0])
                    resoucesArray[j][0] = resoucesArray[j][0]+topLevelQueue[0][4]
                    resoucesArray[j][1] = resoucesArray[j][1]+topLevelQueue[0][3]
                    rejected = False
                    pushedTask = topLevelQueue.pop(0)
                    
                    print("PUSHED: "+str(pushedTask[0]) + " " + str(pushedTask[1]) + " " + str(pushedTask[2]) + " " + str(clock) + " in VM_" + str(j+1))
                    
                    # This block of code is to fairly distribute the processes among the VMs as per requirement
                    lastVM = j
                    j = (j+1) % 16
                    flag = False
                    break
                else:
                    j = (j+1) % 16
            
            # This Block is activated if a process is rejected
            if rejected:
                rejectedTask = topLevelQueue.pop(0)
                print("rejected task {} Found".format(rejectedTask[0]))
                rej_tasks.write("\n" + str(rejectedTask[0]))
                                
            
                

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
                    print("Completed Task " + str(t[0]) + " in VM_" + str(t[2]+1))
                    cmp_tasks.write("\n" + str(t[0]))
                    clear=False
                    break
        
        # Decreamenting the execution time of each process under execution
        executingTasks = [[i[0], i[1]-1, i[2]] for i in executingTasks] 
        

        # This Block pre-empts one process from each VM after every 100 clock cycles
        if clock % 100 == 0:
            for i in range(len(VM_List)):
                if len(VM_List[i])>0:
                    task = VM_List[i].pop(0)
                    for k in executingTasks:
                        if k[0] == task:
                            indexInExec = executingTasks.index(k)
                            
                    taskWithInfo = executingTasks.pop(indexInExec)
                    topLevelQueue.append([task, int(d[task][0]),  taskWithInfo[1], d[task][2],d[task][3]])

                    resoucesArray[i][0] -= d[task][3]
                    resoucesArray[i][1] -= d[task][2]

                    print("PRE-EMPED TASK {} FROM VM_{}".format(task, i+1))


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
 



RoundRobin()
