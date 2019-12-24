filename = r'C:\Users\admin\Desktop\dxsj-20191203\pis\HOUSEINFO.txt'
with open(filename,'r',encoding='utf-8')as f:
    for line in f.readlines():
        lines = str(line.replace("+","\n"))
        path = r'C:\Users\admin\Desktop\test.txt'
        g = open(path,'a')
        g.write(lines)
        print('已处理')
