import os
import hashlib

hash_map={}
tfiles=0

def hashvalue(filepath):
    hashing=hashlib.md5()
    try:
        with open(filepath,'rb') as f:
            while True:
                part=f.read(4096)
                if not part:
                    break
                hashing.update(part)
    except:
        return None
    return hashing.hexdigest()

def scanfiles(folder):
    global tfiles
    for root,dirs,files in os.walk(folder):
        for file in files:
            path=os.path.join(root,file)
            tfiles+=1
            file_hash=hashvalue(path)
            if file_hash is None:
                continue
            if file_hash in hash_map:
                hash_map[file_hash].append(path)
            else:
                hash_map[file_hash]=[path]

def show_duplicates():
    found=False
    for h,files in hash_map.items():
        if(len(files))>1:
            found=True
            print("Duplicate files:")
            for f in files:
                size=os.path.getsize(f)
                print(f,"-Size",size,"bytes")
    if not found:
        print("No duplicates")

def wasted():
    total=0
    for files in hash_map.values():
        if len(files)>1:
            size=os.path.getsize(files[0])
            total+=size*(len(files)-1)
    print("Total space wasted",total,"bytes")

def save():
    with open("duplicate_report.txt","w") as f:
        for files in hash_map.values():
            if len(files)>1:
                f.write("Duplicate files\n")
                for file in files:
                    f.write(file+"\n")
                f.write("\n")

folder=input("Enter folder ")
scanfiles(folder)
print("Total files scanned ",tfiles)
show_duplicates()
wasted()
save()
print("Report saved to duplicate_report.txt")
print("Process completed")