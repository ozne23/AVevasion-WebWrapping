from configuration import Conf
from comp import Comp
import os
from flask import current_app as app
class ConfigCreator():


    def __init__(self):
        self.conf = Conf()
        self.listOfComp = self.conf.getComp()
        self.listOfSub = self.conf.getSub()
        self.tmpOpt1 = []
        self.tmpOpt2 = []

    def create(self,payload_file,template_file,special_char,payload_placeholder,rate,outputname,subs1,string1,compilers,
                                       option1_gcc,option2_gcc,option1_gplusplus,option2_gplusplus,value1_gcc,value2_gcc,value1_gplusplus,value2_gplusplus,hexed_filename):

        ops1_gcc = []
        ops2_gcc = []
        ops1_gplusplus = []
        ops2_gplusplus = []
        ops1_gcc.extend([option1_gcc,value1_gcc])
        ops1_gplusplus.extend([option1_gplusplus,value1_gplusplus])
        ops2_gcc.extend([option2_gcc,value2_gcc])
        ops2_gplusplus.extend([option2_gplusplus,value2_gplusplus])

        config_filename = hexed_filename+".conf.json"

        path = os.path.join(app.config['UPLOAD_FOLDER'],hexed_filename,"config",config_filename)

        self.conf.setTemplatePath(template_file)
        self.conf.setPayloadPath(payload_file)
        self.conf.setSpecialChar(special_char)
        self.conf.setPlaceholderPayload(payload_placeholder)

        rate = float(rate)
        self.conf.setFreq(rate)
        self.conf.setOut(outputname)
        for subs,string in zip(subs1,string1):
            self.conf.addToSub((subs,string))
        comps = []
        for compiler in compilers:
            comp = Comp()
            comp.setName(compiler)
            comp.setPath("edit")
            if compiler == "gcc":
                self.tmpOpt1.append(ops1_gcc)
                self.tmpOpt2.append(ops2_gcc)
            elif compiler == "g++":
                self.tmpOpt1 = []
                self.tmpOpt2 = []
                self.tmpOpt1.append(ops1_gplusplus)
                self.tmpOpt2.append(ops2_gplusplus)

            for t in self.tmpOpt1:
                comp.addOpt1(t)
            for t in self.tmpOpt2:
                comp.addOpt2(t)
            comps.append(comp)

        self.tmpOpt1 = []
        self.tmpOpt2 = []
        for comp in comps:
            self.listOfComp.append(comp)

        with open(path, "w") as f:
            tmp = str(self.conf)
            tmp = tmp.replace("\'", "\"")
            f.write(tmp)
        return config_filename
