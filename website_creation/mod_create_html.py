def create_html(file1,param1,param2,outputfile):
    input_name =param1
    input_subject =param2
    f1 =open(file1,'r')
    list1 =f1.read().split('$$$')
    info1= ""
    params =[]
    params.append(param1)
    params.append(param2)
    list2= list1
    for i in range(0,2,1):
        list2[2*i+1]=params[i]
    
    info1 ="".join(list2)
    outputfile.write(info1)
    outputfile.close()

