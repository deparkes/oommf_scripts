import sys
def get_omf(path):
    # A function to find the omf magnetisation vector files in a particular folder.
    # Since I only want one I have an if statement to try and protect things. Needs improvements.
    # Use os.path.basename(path) to strip away everything but the file name from the path.
    import glob
    import os
    # print os.getcwd()
    # os.chdir('../output/15um90umBarWithCrosses.bmp/strain_0');
    omf_path = '%s/*.omf' % (path)
    #create an array of file names based on the search for omf files.
    files_array = glob.glob(omf_path)
    files = os.path.basename(files_array[0])
    return files

def main(argv):
    import os
    import subprocess
    import time
    import datetime
    start_dir = argv[1]
    path_to_omf = os.getcwd()
    path_tcl = 'C:/Program Files/Tcl/bin/tclsh83'
    path_oommf  = 'C:/oommf/oommf.tcl'
    #config_file = './avf2ppm.def'
    #start_dir = os.getcwd()

    for root, dirs, files in os.walk(start_dir):
        # make sure that we are at the end of the path
        # i.e. that there are no subdirectories
        if len(dirs) == 0:
            print root
            files = get_omf(root)
            os.chdir(root)
            #command_to_run = 'avf2ppm -config %s -format B24 %s' % (config_file,files)
            command_to_run = 'avf2ppm -format B24 %s' % (files)
            run_string = '%s %s %s' % (path_tcl, path_oommf, command_to_run)
            subprocess.call(run_string)
    os.chdir(start_dir)
    
    # For debugging. If I run this script in a windows command window the following will stop the window from closing before I can read the error message.
    print "Press return to continue"
    a=raw_input()


if __name__ == "__main__":
    main(sys.argv)
