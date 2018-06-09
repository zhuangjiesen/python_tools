
def containsKey(dict , key):
    if not dict :
        return False;
    if key in dict.keys():
        return True;

# 获取当前py 文件名 无后缀
def getThisPythonFileName(frame):
    file_type = '.py';
    file_name = frame.f_code.co_filename;
    file_name = file_name.split("\\")[-1];
    file_name = file_name.split("/")[-1];
    type_index = file_name.find(file_type);
    file_name = file_name[0 : type_index];
    # print('file_name : '  , file_name)
    return file_name;