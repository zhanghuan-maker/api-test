
import yaml
import os
import random
import string



seed="1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-<>?.,?;:]}{[|"
def getdata(case):
    # 读取yaml的值
    yamlinsex= open(case,'r',encoding='utf-8')
    # 把文件内容读取出来
    data = yaml.load(yamlinsex)
    return data

def generate_yaml(current_path_file,yaml_file):
    object = getdata(current_path_file)

    object=parameter_null(object)
    file = open(yaml_file, 'w', encoding='utf-8')
    print(yaml_file)
    yaml.dump(object, file,default_flow_style=False, allow_unicode=True)
    file.close()

#生成带null的字段
def parameter_null(object):

    new_dict={}
    sub_list=[]

    key=list(object.keys())[0]
    need_change = object[key][0]
    else_change1 = object[key][1]
    else_change2 = object[key][2]

    #generate_single null
    middle_list=[]
    for i in need_change:
         middle_dict = need_change.copy()
         middle_dict[i]= None
         c=middle_dict.copy()
         c.update(else_change2)
         middle_list.append(c)

    # generate_all null
    for i in need_change:
        middle_dict[i] = None
    c = middle_dict.copy()
    c.update(else_change2)
    middle_list.append(c)


    #generate_join_str
    for i in range(50):
        middle_dict = need_change.copy()
        for i in need_change:
            middle_dict[i] =insert_str(middle_dict[i])
        c = middle_dict.copy()
        c.update(else_change2)
        middle_list.append(c)

    sub_list=middle_list
    # happy_path
    k = need_change
    k.update(else_change1)
    sub_list.append(k)

    new_dict[key]=sub_list
    return (new_dict)

#随机位置插入字符
def insert_str(string1):

    stringList=list(string1)
    len1=len(stringList)
    insert_str=random.choice(seed)
    rand_num=random.randrange(0,len1+1)
    stringList.insert(rand_num,insert_str)
    return (''.join(stringList))


def main_generate_yaml(Case):
    case=[]
    filename=[]

    current_path = os.path.abspath("./conf/"+Case+"/old_yaml")
    generate_path = os.path.abspath("./conf/"+Case)

    for root, dirs, files in os.walk(current_path):
        for file in files:
            if file.endswith('yaml'):
                case.append(os.path.join(root, file))
                filename.append(file)

    for i in range(len(case)):

        generate_yaml(current_path+'/'+filename[i],generate_path+"/"+filename[i])