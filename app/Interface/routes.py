from flask import Blueprint, render_template, redirect, url_for,flash,request,send_from_directory
import os
from werkzeug.utils import secure_filename
from flask import current_app as app
from FileManager import FileManager
from ConfigCreator import ConfigCreator
from avevasionEngine import avevasionEngine



# Blueprint Configuration
main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@main_bp.route('/', methods=['GET'])
@main_bp.route('/index', methods=['GET'])
def index():
    return render_template("index.html")

# @main_bp.route('/', methods=['GET'])
# @main_bp.route('/index', methods=['GET'])
# def index():
#     return render_template("download.html",num=4)

@main_bp.route('/upload', methods=['GET','POST'])
def upload():
    #TODO UPLOAD FILES, CALL FILE MANAGER TO MODIFY JSON PATH
    if request.method == 'POST':
        #Print files just for check, delete this code
        # uploaded_files = request.files.getlist("config-file")
        # uploaded_files.append(request.files.getlist("payload-file"))
        # uploaded_files.append(request.files.getlist("template-file"))
        # uploaded_files.append(request.files.getlist("compilers"))
        # print(uploaded_files)
        #get refrences to files
        config_file = request.files['config-file']
        payload_file = request.files['payload-file']
        template_file = request.files['template-file']
        #compilers_dir = request.files.getlist('compilers')
        if config_file.filename == "" or payload_file.filename == "" or template_file == "":
            return render_template("results.html")
        try:
            fm = FileManager()
            #Generate random hex as filename
            hexed_filename=fm.generate_random_hexed_name()

            #create directory structure
            fm.create_directories(hexed_filename)

            #upload files to directories
            fm.save_files(config_file,payload_file,template_file,hexed_filename)

            #modify paths of uploaded config files, so that ther are relevent to the server side
            fm.modifyConfigFile(config_file.filename,template_file.filename,payload_file.filename,hexed_filename)
            compilers = fm.getCompilers(hexed_filename,config_file.filename)
            #Call module to run AVevasion
            engine = avevasionEngine()
            report = engine.run_avevasion(hexed_filename,config_file.filename,app.config['UPLOAD_FOLDER'])
            #MOVE OUTPUT FILES IN THE USER OUTPUT DIR
            fm.move_outputFile(hexed_filename,config_file.filename)
            fm.compress_user_directory(app.config['OUTPUT_FOLDER'],hexed_filename)
            # num_outfiles = fm.get_num_outputfiles(app.config['OUTPUT_FOLDER']+"\\"+hexed_filename)
            # folders = fm.get_folder_name_paths(app.config['OUTPUT_FOLDER']+"\\"+hexed_filename)
            # print(filenames)
            print("Report var: ")
            print(report)
        except:
            flash("Something went wrong please check your files")
            return redirect(url_for('main_bp.index'))
    #TODO RIDERECT TO PAGE TO DOWNLOAD THE RESULT
    #return render_template("results.html",num_outfiles=num_outfiles,folders=folders,filenames=filenames)
    hexed_filename = hexed_filename+".zip"
    return render_template("results.html",filename=hexed_filename,report=report,compilers=compilers)


@main_bp.route('/download/<filename>', methods=['GET', 'POST'])
def download(filename):
    #downloads = os.path.join(app.root_path, app.config['OUTPUT_FOLDER'])
    downloads = app.config['OUTPUT_FOLDER']
    return send_from_directory(directory=downloads, filename=filename)

@main_bp.route('/createconf',methods=['GET','POST'])
def createconf():
    if request.method == 'POST':
        payload_file = request.files['payload-file']
        template_file = request.files['template-file']
        special_char = request.form['specialchar']
        payload_placeholder = request.form['payloadplaceholder']
        rate = request.form['rate']
        outputname = request.form['outputname']
        subs1 = request.form.getlist('subs')
        string1 = request.form.getlist('strings')
        compilers = request.form.getlist('compilers')
        for sub in subs1:
            print(sub)
        for string in string1:
            print(string)
        option1_gcc = request.form['option1-gcc']
        option2_gcc = request.form['option2-gcc']
        option1_gplusplus = request.form['option1-g++']
        option2_gplusplus = request.form['option2-g++']
        value1_gcc = request.form.getlist('value1-gcc')
        value2_gcc = request.form.getlist('value2-gcc')
        value1_gplusplus = request.form.getlist('value1-g++')
        value2_gplusplus = request.form.getlist('value2-g++')

        try:
            fm = FileManager()
            #Generate random hex as filename
            hexed_filename=fm.generate_random_hexed_name()

            #create directory structure
            fm.create_directories(hexed_filename)

            #TODO MAKE THIS MORE SCALABLE
            builder = ConfigCreator()
            config_filename= builder.create(payload_file.filename,template_file.filename,special_char,payload_placeholder,rate,outputname,subs1,string1,compilers,
                                           option1_gcc,option2_gcc,option1_gplusplus,option2_gplusplus,value1_gcc,value2_gcc,value1_gplusplus,value2_gplusplus,hexed_filename)

            #upload files to directories
            fm.save_files("",payload_file,template_file,hexed_filename)

            #modify paths of uploaded config files, so that ther are relevent to the server side
            fm.modifyConfigFile(config_filename,template_file.filename,payload_file.filename,hexed_filename)
            compilers = fm.getCompilers(hexed_filename,config_filename)
             #Call module to run AVevasion
            engine = avevasionEngine()
            report = engine.run_avevasion(hexed_filename,config_filename,app.config['UPLOAD_FOLDER'])
            #MOVE OUTPUT FILES IN THE USER OUTPUT DIR
            fm.move_outputFile(hexed_filename,config_filename)
            fm.compress_user_directory(app.config['OUTPUT_FOLDER'],hexed_filename)
        except:
            flash("Something went wrong please check your files")
            return redirect(url_for('main_bp.index'))

    download_filename = hexed_filename+".zip"
    return render_template("results.html",filename=download_filename,report=report,compilers=compilers)
