#################################################################################################
#FileManager is used to modify the path to compiler payload and template so that they are relevent
#to the servers path
import json
from pathlib import Path
import os
import secrets
from flask import current_app as app
from werkzeug.utils import secure_filename
import shutil

compilers_supported = {"gcc","g++"}

class FileManager:
    def modifyConfigFile(self,config_filename, template_filename, payload_filename, user_folder_name):
        """
        Modifies the configuration file paths so that they are relevant to server filesystem.
        :param config_filename:
        :param template_filename:
        :param payload_filename:
        :param user_folder_name:
        :return:
        """
    #receives in input the config file name to search and modify.

        #TODO MAKE PATH MORE DYNAMIC
        template_location = Path(app.config['UPLOAD_FOLDER']+"\\"+user_folder_name+"\\template")
        payload_location = Path(app.config['UPLOAD_FOLDER']+"\\"+user_folder_name+"\\payload")
        config_location = Path(app.config['UPLOAD_FOLDER']+"\\"+user_folder_name+"\\config")
        gcc_path = Path(app.config['GCC_COMPILER_FOLDER'])
        gplusplus_path = Path(app.config['GPLUSPLUS_COMPILER_FOLDER'])
        path = config_location / config_filename
        new_template_path = template_location / template_filename
        new_payload_path = payload_location / payload_filename
        print(path)

        #Negotiate compilers with server
        negotiated_compilers = self.check_compilers(path)

        with open(path, "r") as jsonFile:
            data = json.load(jsonFile)
            print(data)

        #Modify config files
        data["manipulations"]["template"] = new_template_path.__str__()
        data["manipulations"]["payload"]["path"] = new_payload_path.__str__()
        for compiler in  negotiated_compilers:
            print(compiler)
            if compiler == "gcc":
                data["compilers"][compiler]["path"] = gcc_path.__str__()
            if compiler == "g++":
                data["compilers"][compiler]["path"] = gplusplus_path.__str__()

        with open(path, "w") as jsonFile:
            json.dump(data, jsonFile)

    def create_directories(self,hashed_filename):
        """
        Creates the User Directory, and output directory
        :param hashed_filename:
        :return:
        """
        #uploads directory
        path1 = hashed_filename+"\\config"
        path2 = hashed_filename+"\\payload"
        path3 = hashed_filename+"\\template"
        try:
            os.chdir(app.config['UPLOAD_FOLDER'])
            os.makedirs(path1)
            os.makedirs(path2)
            os.makedirs(path3)
        except OSError:
            print ("Creation of the directory failed")
        else:
            print ("Successfully created the directory")
        #output dir
        dir_name = hashed_filename
        path4 = dir_name+"\\code"
        try:
            os.chdir(app.config['OUTPUT_FOLDER'])
            os.mkdir(dir_name)
            os.makedirs(path4)

        except OSError:
            print ("Creation of the directory failed")
        else:
            print ("Successfully created the directory ")

    def save_files(self, config_file, payload_file, template_file, hexed_filename):
        """
        Uploads files to server
        :param config_file:
        :param payload_file:
        :param template_file:
        :param hexed_filename:
        :return:
        """
        if config_file != "":
            filename = secure_filename(config_file.filename)
            config_file.save(os.path.join(app.config['UPLOAD_FOLDER'], hexed_filename + "\\", "config", filename))
            filename = secure_filename(payload_file.filename)
            payload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], hexed_filename + "\\", "payload", filename))
            filename = secure_filename(template_file.filename)
            template_file.save(os.path.join(app.config['UPLOAD_FOLDER'], hexed_filename + "\\", "template", filename))
            # for file in compilers_dir:
            #     filename = secure_filename(file.filename)
            #     file.save(os.path.join(app.config['UPLOAD_FOLDER'],hexed_filename+"\\","compiler", filename))
        else:
            filename = secure_filename(payload_file.filename)
            payload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], hexed_filename + "\\", "payload", filename))
            filename = secure_filename(template_file.filename)
            template_file.save(os.path.join(app.config['UPLOAD_FOLDER'], hexed_filename + "\\", "template", filename))
            pass

    def generate_random_hexed_name(self):
        """
        Generates a random hex string
        :return: random hex string
        """
        s = secrets.token_hex(15)
        return s

    def move_outputFile(self,hexed_filename,config_filename):
        """
        Moves generated source code and executables to the right User Directory and output directory
        :param hexed_filename:
        :param config_filename:
        :return:
        """
        #TODO AVevasion will save file somewhere random, get the output files and place them in the right directory,
        #TODO READ ALL COMPILERS AND ALL OUTPUTS
        output_names = {}
        manipulation_names ={}
        config_location = Path(app.config['UPLOAD_FOLDER']+"\\"+hexed_filename+"\\config")
        config_path = config_location / config_filename
        #READ CONF FILE
        with open(config_path, "r") as jsonFile:
            data = json.load(jsonFile)

        if 'out' in data['manipulations']:
            manipulation_names['out'] = data['manipulations']['out']

        for compiler in data['compilers']:
            if 'options1' in data['compilers'][compiler] and 'value' in data['compilers'][compiler]['options1'][0]:
                output_names[compiler] = data['compilers'][compiler]['options1'][0]['value']
            elif 'options2' in data['compilers'][compiler] and 'value' in data['compilers'][compiler]['options2'][0]:
                output_names[compiler] = data['compilers'][compiler]['options2'][0]['value']
        output_path = app.config['OUTPUT_FOLDER']

        #moves outputs generated by compilers in the compiler for which it came
        for source_compiler in output_names:
            command1 = 'move '+output_names[source_compiler][0]+" "+os.getcwd()+"\\"+source_compiler
            print(command1)
            os.system(command1)
        #os.system('move out1.c C:\\Users\\ozne2\\Desktop\\Tesi\\AVevasion\\Wrapper\\AVevasion\\app\\Interface\\gcc')
        #moves entire compiler dir to output dir
        for source_compiler in output_names:
            command = 'move '+source_compiler+" "+output_path+"\\" +hexed_filename
            print(command)
            os.system(command)
        command = 'move '+manipulation_names['out']+" "+output_path+"\\"+hexed_filename+"\\code"
        os.system(command)


    def check_compilers(self,config_path):
        """
        Negotiates supported compilers between user and server.
        :param config_path:
        :return:
        """
        global compilers_supported
        user_compilers = []
        result = []

        with open(config_path, "r") as jsonFile:
            data = json.load(jsonFile)

        for compiler in data['compilers']:
            user_compilers.append(compiler)
            print(user_compilers)
        for compiler in user_compilers:
            if compiler in compilers_supported:
                result.append(compiler)
            else:
                #remove non supported compilers from config file
                del data['compilers'][compiler]

        with open(config_path, "w") as jsonFile:
            json.dump(data, jsonFile)

        return result

    def get_num_outputfiles(self,path):
        #TODO DELETE THIS FUNCTION IF NOT NEEDED
        count = []
        for f in os.listdir(path):
            count.append(f)
        return count.__len__()
        # count = 0
        # for f in os.listdir(path):
        #     child = os.path.join(path, f)
        #     if os.path.isdir(child):
        #         child_count = self.get_num_outputfiles(child,map)
        #         count += child_count + 1
        # map[path] = count
        # return count

    def get_folder_name_paths(self,path, map ={}):
        #TODO DELETE THIS FUNCTION IF NOT NEEDED
        folders = []
        for f in os.listdir(path):
            folders.append(f)
        return folders

    def compress_user_directory(self,path,hexed_filename):
        """
        Creates zip file in output directory
        :param path:
        :param hexed_filename:
        :return:
        """
        os.chdir(path)
        shutil.make_archive(hexed_filename, 'zip', path+"\\"+hexed_filename)
    def getCompilers(self,hex,filename):
        config_location = Path(app.config['UPLOAD_FOLDER']+"\\"+hex+"\\config")
        #config_location = Path('C:\\Users\\ozne2\\Desktop\\Tesi\\AVevasion\\Wrapper\\AVevasion\\app\\uploads\\'+hex+'\\config')
        path = config_location / filename
        compilers = []
        with open(path, "r") as jsonFile:
            data = json.load(jsonFile)

        for compiler in data['compilers']:
            compilers.append(compiler)

        return compilers
