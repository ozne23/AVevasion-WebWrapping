from FileManager import FileManager
from ConfigCreator import ConfigCreator
from pathlib import Path
import json
from virusTotal import VirusTotal
from avevasionEngine import avevasionEngine
import os
import tempfile
import secrets
fm = FileManager()

compilers = fm.getCompilers('1ba7a8940471a9a61613cc641f380d','config1.conf.json')
print(compilers)
scores = []
scores.append("2,2")
scores.append("2,4")
print(scores)

for index,score in enumerate(scores):
    print(compilers[index]+":"+ score)

# cc = ConfigCreator()
# path = "C:\\Users\\ozne2\\Desktop\\Tesi\\AVevasion\\Wrapper\\AVevasion\\app\\uploads"
#
# hex = "0d22e0ae132b89e508a6e49cd75a4d"
# compilers = ['gcc','g++']
# cc.create("payload_file","template_file","special_char","payload_placeholder",1,"outputname","subs1","string1",compilers,
#                                        "option1_gcc","option2_gcc","option1_gplusplus","option2_gplusplus","value1_gcc","value2_gcc","value1_gplusplus","value2_gplusplus",hex,path)




#fm.modifyConfigFile("enzo_config.conf.json","template_enzo.txt","enzo_payload.txt","4bf57b02a5d7b7d14e476fcad035c5")
#fm.modifyConfigFile("read_compilers_test.conf.json","template1.txt","enzo_payload.txt","38ad7c870ed08872c04c574f0059ce")


# engine = avevasionEngine()
# engine.run_avevasion("3dfb7276653f18b5ea2ad77fac00a6","config1.conf.json")

#os.system('python main.py -c C:\\Users\\ozne2\\Desktop\\Tesi\\AVevasion\\Wrapper\\AVevasion\\app\\uploads\\config1.conf.json')


# for i in range(20):
#      s = secrets.token_hex(15)
#      print(s)

#fm.check_compilers("C:\\Users\\ozne2\\Desktop\\Tesi\\AVevasion\\Wrapper\\AVevasion\\read_compilers_test.conf.json")
# output_names = {}
# manipulation_names ={}
# config_path = "C:\\Users\\ozne2\\Desktop\\Tesi\\AVevasion\\Wrapper\\AVevasion\\config1.conf.json"
# with open(config_path, "r") as jsonFile:
#     data = json.load(jsonFile)
#
# if 'out' in data['manipulations']:
#     manipulation_names['out'] = data['manipulations']['out']
#     print(output_names)
#
#     for compiler in data['compilers']:
#         if 'options1' in data['compilers'][compiler] and 'value' in data['compilers'][compiler]['options1'][0]:
#             output_names[compiler] = data['compilers'][compiler]['options1'][0]['value']
#             print(data['compilers'][compiler]['options1'][0]['value'])
#         elif 'options2' in data['compilers'][compiler] and 'value' in data['compilers'][compiler]['options2'][0]:
#             output_names[compiler] = data['compilers'][compiler]['options2'][0]['value']
#             print(data['compilers'][compiler]['options2'][0]['value'])
#
# output_path = "C:\\Users\\ozne2\\Desktop\\Tesi\\AVevasion\\Wrapper\\AVevasion\\app\\Output"
# for source_compiler in output_names:
#     command1 = 'echo move '+output_names[source_compiler][0]+" "+os.getcwd()+"\\"+source_compiler
#     print(command1)
# for source_compiler in output_names:
#     command = 'move '+source_compiler+" "+output_path+"\\" +"hexed_filename"
#     print(command)
#
# print(output_names)
# command = 'move '+manipulation_names['out']+" "+output_path+"\\"+"hexed_filename"+"\\code"
# print(command)
# result = manipulation_names,output_names
# print(result)

# path = Path("C:\\Users\\ozne2\\Desktop\\Tesi\\AVevasion\\Wrapper\\AVevasion\\app\\Output\\fc44c3e075fc92564650937f227965")
# def fcount(path, map = {}):
#   count = 0
#   for f in os.listdir(path):
#     child = os.path.join(path, f)
#     if os.path.isdir(child):
#       child_count = fcount(child, map)
#       count += child_count + 1 # unless include self
#   map[path] = count
#   return count
#
# map = {}
# res = fcount(path, map)
# print(res)

# path = Path("C:\\Users\\ozne2\\Desktop\\Tesi\\AVevasion\\Wrapper\\AVevasion\\app\\Output\\fc44c3e075fc92564650937f227965")
# def fcount(path):
#   count =[]
#   for f in os.listdir(path):
#     count.append(f)
#
#   return count.__len__()
#
#
# map = {}
# res = fcount(path)
# print(res)

# import shutil
# os.chdir("C:\\Users\\ozne2\\Desktop\\Tesi\\AVevasion\\Wrapper\\AVevasion\\app\\Output")
# shutil.make_archive("e46b173d239070c698df7f94464ab1", 'zip', "C:\\Users\\ozne2\\Desktop\\Tesi\\AVevasion\\Wrapper\\AVevasion\\app\\Output\\e46b173d239070c698df7f94464ab1")
