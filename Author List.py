Listname = "F:/Emerging Media/Author Index 150910/12.txt"
Bookname = "F:/Emerging Media/BookChs/12.txt"
RawNamelist = open(Listname)
Namelist = RawNamelist
def Firstname(Rawname):
    firstname = Rawname[:Rawname.rfind(",")]
    return firstname
def PageNo(line):
    KeyPos = line.find('indd')
    Sp1Pos = line.find(' ',KeyPos)
    Sp2Pos = line.find(' ',Sp1Pos+1)
    Page =  line[Sp1Pos:Sp2Pos]
    Page = int (Page)
    return Page
def same(str1,str2):
##line = str1
##firstname = str2
    try:
        value = (str1[str1.find(str2)+len(str2)] == ",") or (str1[str1.find(str2)+len(str2)] == " ")
        return value
    except:
        return 1
key = "indd"
Namecount = 0
for name in Namelist:
    Pages = list()
    Booktext = open(Bookname)
    name = name.rstrip()
    Namecount = Namecount +1
    #print ("Begin with name:",Namecount)
    firstname = Firstname(name)
    Linecount = 0
    for line in Booktext.readlines()[Linecount:len(Booktext.readlines())-1]:
        Booktext = open(Bookname)
        line = line.rstrip()
        Linecount = Linecount +1
        Page = 0
        Linecount2 = 0
        #print ("Searching name :",Namecount, "in line:",Linecount)
        if not firstname in line :
            #print("Name", Namecount, "not found in line", Linecount)
            continue
        #print("Name", Namecount, "found in line", Linecount)
        if not (("(" in line) or (")" in line) or ("&" in line) or ("," in line)):
            continue
        if not same(line,firstname):
            continue
        for line in Booktext.readlines()[Linecount:len(Booktext.readlines())-1]:
            Linecount2 = Linecount2 + 1
            #print ("Searching page number for name ",Namecount, "in",Linecount, "in",Linecount2,"lines after the name")
            if not key in line:
                #print ("Page number for name ",Namecount, "in",Linecount, "Not found in",Linecount2,"lines after the name")
                continue
            Page = PageNo(line)
            #print ("Page number for name ",Namecount, "in",Linecount, "found in",Linecount2,"lines after the name")
            break
        if (Page  not in Pages):
            Pages.append(Page)
        else:
            a = 1 
    print (name,"\t""\t""\t""\t",Pages)
    #print ("Done with name ", Namecount)