import os
import re
import argparse

# Please tune the hyperparameters
parser = argparse.ArgumentParser()
parser.add_argument("--train", default=1, type=int)
parser.add_argument("--train_dir", default="./data/train")
parser.add_argument("--test_dir", default="./data/test")
args = parser.parse_args()


class Preprocess(object):
    def __init__(self,path=args.train_dir):
        self.path=path
        self.allSentence=[]
    def extract(self):
        allFiles=os.listdir(self.path)
        allFiles.sort()
        for fileName in allFiles:
            fileId.append(fileName)
            f=open(os.path.join(self.path,fileName),'r')
            content=f.read()
            self.allSentence.append(self.split(content))
            if "CURRENT SMOKER" in fileName:
                label.append(0)
            elif "NON-SMOKER" in fileName:
                label.append(1)
            elif "PAST SMOKER" in fileName:
                label.append(2)
            elif "UNKNOWN" in fileName:
                label.append(3)
            else:
                #testing data omitted
                pass
        return self.allSentence
    def split(self,content):
        s=re.split("[\n|,]",content)
        return s

class Regulation(object):
    def __init__(self,allSentence):
        self.allSentence=allSentence
    def pred(self):    
        for s in self.allSentence:
            if self.r2(s):
                pred.append(2)
            elif self.r1(s):
                pred.append(1)
            elif self.r0(s):
                pred.append(0)
            else:
                pred.append(3)
    def r0(self,s):
        flag=False
        for index,sentence in enumerate(s):
            if "smokes" in sentence.lower() or "smoking" in sentence.lower() or "smoker" in sentence.lower():
                flag=True
            elif "tobacco use" in sentence.lower() or "nicotine use" in sentence.lower():
                flag=True
            elif "tobacco" in sentence.lower() or "nicotine" in sentence.lower():
                if "abuse" in sentence.lower():
                    flag=True
            elif "cigs" in sentence.lower() or "cigar" in sentence.lower():
                flag=True
        return flag
    def r1(self,s):
        flag=False
        probability=0
        for index,sentence in enumerate(s):
            if "not smoke" in sentence.lower() or "no smoking" in sentence.lower():
                flag=True
            elif "tobacco" in sentence.lower() or "nicotine" in sentence.lower() or "cigs" in sentence.lower() or "cigar" in sentence.lower():
                if "denies" in sentence.lower():
                    flag=True
            if "ventricular" in sentence.lower():  
                probability+=1
            if "coronary" in sentence.lower(): 
                probability+=1
            if  "artery" in sentence.lower():
                probability+=1
            if  "cardiac" in sentence.lower():
                probability+=1           
            if  "vein" in sentence.lower():
                probability+=1
            if  "circumflex" in sentence.lower():
                probability+=1
            if "smok" in sentence.lower():
                probability=-100
            if "tobacco" in sentence.lower() or "nicotine" in sentence.lower() or "cigs" in sentence.lower() or "cigar" in sentence.lower():
                probability=-100
        if probability>=3:
                flag=True
        return flag
    def r2(self,s):
        flag=False
        for index,sentence in enumerate(s):
            if "tobacco" in sentence.lower() or "nicotine" in sentence.lower() or "cigs" in sentence.lower() or "cigar" in sentence.lower():
                if "quit" in sentence.lower() or "quit" in s[index-1].lower() or "quit" in s[index+1].lower():
                    if "years ago" in sentence.lower() or "years ago" in s[index-1].lower() or "years ago" in s[index+1].lower() :
                        flag=True
                    elif "year ago" in sentence.lower() or "year ago" in s[index-1].lower() or "year ago" in s[index+1].lower()  :
                        flag=True
                    elif "in " in sentence.lower():
                        flag=True
                elif "former" in sentence.lower():
                    flag=True
            elif "quit smoking" in sentence.lower() or "smoked" in sentence.lower() or "smoker" in sentence.lower():
                if "years ago" in sentence.lower() or "years ago" in s[index-1].lower()  or "years ago" in s[index+1].lower()  :
                    flag=True
                elif "year ago" in sentence.lower() or "year ago" in s[index-1].lower()  or "year ago" in s[index+1].lower()  :
                    flag=True               
                elif "in " in sentence.lower():
                    flag=True
            elif "spo2" in sentence.lower() or "desaturate" in sentence.lower():
                if not self.r0(s) and not self.r1(s):
                    num=''.join([x for x in sentence if x.isdigit()])
                    if int(num) <= 96:
                        flag=True
            elif "oxygen saturation" in sentence.lower() or "oxygen saturations" in sentence.lower() :
                if not self.r0(s) and not self.r1(s):
                    num=''.join([x for x in sentence if x.isdigit()])
                    if int(num) <= 96:
                        flag=True
        return flag

def main():
    pre=Preprocess()    
    allSentence=pre.extract()
    reg=Regulation(allSentence)
    reg.pred()
    print("File ID order:")
    print(fileId)
    print("Smoker status prediction:")
    print(pred)
    print("Smoker status label:")
    print(label)
    f=open("case1_11.txt","w")
    for item in pred:
        if item==0:
            f.write("CURRENT SMOKER\n")    
        elif item==1:
            f.write("NON-SMOKER\n")
        elif item==2:
            f.write("PAST SMOKER\n")
        elif item==3:
            f.write("UNKNOWN\n")
    f.close()

def test():
    pre=Preprocess(args.test_dir)    
    allSentence=pre.extract()
    reg=Regulation(allSentence)
    reg.pred()
    print("File ID order:")
    print(fileId)
    print("Smoker status prediction:")
    print(pred)
    f=open("case1_11.txt","w")
    for item in pred:
        if item==0:
            f.write("CURRENT SMOKER\n")    
        elif item==1:
            f.write("NON-SMOKER\n")
        elif item==2:
            f.write("PAST SMOKER\n")
        elif item==3:
            f.write("UNKNOWN\n")
    f.close()

if __name__ == "__main__" :
    fileId=[]
    label=[]
    pred=[]
    if args.train:
        main()
    else:
        test()
