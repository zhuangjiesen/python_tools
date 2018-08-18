import time
import datetime
import uuid


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




def switchTimeToLong(dateStr):
    timeArray = time.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    timeStamp = timeStamp * 1000;
    return timeStamp;

def getStartTodayDate():
    # 获取当前时间, 其中中包含了year, month, hour, 需要import datetime
    today = datetime.date.today()
    today = str(today) + ' 00:00:00';
    return today;

def getEndTodayDate():
    # 获取当前时间, 其中中包含了year, month, hour, 需要import datetime
    today = datetime.date.today()
    today = str(today) + ' 23:59:59';

def getUUIDString():
    text = uuid.uuid1();
    text = str(text)
    text = text.replace('-' , '');
    return text;

