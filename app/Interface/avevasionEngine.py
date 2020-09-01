import os
from pathlib import Path
from compEngine import CompilationEngine
from virusTotal import VirusTotal
from manipulator import Manipulator

vt = VirusTotal()

class avevasionEngine():

    def run_avevasion(self,hexed_filename,config_filename,path):
        #pickup config file based on hexed_filename and execute shell
        #conf =  Path("C:\\Users\\ozne2\\Desktop\\Tesi\\AVevasion\\Wrapper\\AVevasion\\app\\uploads\\"+hexed_filename+"\\config\\"+config_filename)
        conf = Path(path+"\\"+hexed_filename+"\\config\\"+config_filename)

        ce = CompilationEngine(conf)
        m = Manipulator(conf)
        m.generateSource()
        ce.createExes()
        complist = ce.getReport()
        print(os.path)
        global vt
        report = vt.getScore(complist)
        print(complist)
        print(report)

        return report



