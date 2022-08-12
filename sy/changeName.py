import os

def changeName(path):
    count = 1
    filenames = [filename for filename in os.listdir(path) if filename.endswith("jpg")]
    for filename in filenames:
        print(filename)
        print(path+filename)
        os.rename(path+filename, path+ str(count)+ ".jpg")
        count += 1

changeName("C:\\Users\\SSAFY\\Downloads\\")