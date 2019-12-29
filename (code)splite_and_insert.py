filename = r'C:\Users\admin\Desktop\dxsj-20191203\pis\PISTABLE0.txt'
list = []
with open(filename,'r',encoding='utf-8')as f:
    for line in f.readlines():
        lines = str(line.replace("+","\n").replace(",,,,,,,,",",").replace(",,,,",",").replace(",,,",",").replace(",,",","))
        #lines_fina = lines.join("\n")
        str1 = "insert into info_people values ("
        str2 = ")"
        str3 = ";"
        str4 = "\n"
        sql = str1 + lines + str2 + str3 + str4
        path = r'C:\Users\admin\Desktop\test.txt'
        g = open(path,'a')
        g.write(sql)



