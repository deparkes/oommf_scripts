# oommf script test
##C:\Tcl\bin\tclsh84.exe C:\oommf\oommf.tcl boxsi -exitondone 0
##-parameters "Ks %1 "
##C:/oommf/duncan/FeGa_Simulations/FeGa_Bar_Field_1.mif
## Todo:
## - add output of input parameters so I can easily see which parameters where used.
## - Add parameter file so I can import different parameter settings from a single file.

def get_omf(path):
    import glob
    import os
    print os.getcwd()
    # os.chdir('../output/15um90umBarWithCrosses.bmp/strain_0');
    omf_path = '%s/*.omf' % (path)
    files = glob.glob(omf_path)
    if len(files) == 1: 
        omf_file = files[0]
        return omf_file
    

def main():
    import os
    import subprocess
    import time
    path_tcl = 'C:/Tcl/bin/tclsh84'
    #path_tcl = 'C:/Program Files/Tcl/bin/tclsh83'
    #path_tcl = '//tsclient/C/Tcl/bin/tclsh84'
    path_boxsi_base = 'C:/oommf/oommf.tcl boxsi -exitondone 1 -parameters'
    #path_boxsi_base = 'C:/oommf_pcb/oommf.tcl boxsi -exitondone 1 -parameters'
    #path_boxsi_base = '//tsclient/C/oommf/oommf.tcl boxsi -exitondone 1 -parameters'
    path_mif_file = './FeGa_SweepStrain.mif'
    path_image = '../structure_files/'
    oommf_string = "%s %s %s" % (path_tcl, path_boxsi_base,path_mif_file)
    # this one is a bit quick and dirty, but might be ok
    #os.system(oommf_string)
    ##    img_list = ['Cross_4um.bmp','Lbar_2um.bmp','BarPad_7um_1um.bmp', 'Ring_10um_2um.bmp']
    ##    img_list = ['Square_5um.bmp','Ring_10um_2um.bmp','BarPad_3um_1um.bmp','BarPad_5um_1um.bmp','BarPad_6um_1um.bmp','BarPad_7um_1um.bmp']
    #    I want to allow the script to read in a list of image files to simulate.
    #I want the script to read in the file eaach time so that I can update my batch job on the fly.
    ##    img_list = ['Lbar_2um.bmp']


    ## Load the initial list of structure files. 
    img_list = open('./structures.txt').read().splitlines()
    img_list_length = len(img_list)
    # strain_list = ['1000', '5000']
    strain_list = open('./strains.txt').read().splitlines()
    strain_list_length = len(strain_list)

    img_count = 0
    strain_count = 0
    
    img_list_length = len(img_list)
    while img_count < img_list_length:
        # loop through different values of strain energy for each of
        # the devices
        while strain_count < strain_list_length:

        ##   Set the output directory name for this strain and structure.
        ##   If this directory doesn't exist make it.
            img_dir = '../output/sweep/%s/strain_%s' % (img_list[img_count], strain_list[strain_count])
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)
                
        ## I want to use the omf magnetisation file from the previous strain value as the
        # starting point for the simulation of the next strain value.
        # At the moment I need to have run the initial condition (probably strain = 0) separately.
        # The strain list needs to start from the first non-initial strain condition (something like 2000 maybe).
        # This first value will take as its starting value the magnetisation file of the strain_0 case.
        # Further strain values use the omf file from the previous value of strain as the starting point. The final
        # omf file will not be used like this as it is the finishing point.
            if strain_count == 0:
                initial_omf = '../output/sweep/%s/strain_0' % (img_list[img_count])
                omf_file =  get_omf(initial_omf)
                omf_path = '../output/sweep/%s/strain_0/%s' % (img_list[img_count], omf_file)
                
            else:
                omf_dir = '../output/sweep/%s/strain_%s' % (img_list[img_count], strain_list[strain_count-1])
                omf_file =  get_omf(omf_dir)
                omf_path = '../output/sweep/%s/strain_%s/%s' % (img_list[img_count], strain_list[strain_count-1], omf_file)
                
            print omf_file
            
                
        ## Set and run the full command for boxsi 
            path_boxsi = path_boxsi_base + ' \"Ks %s img %s InputOMF %s\"' % (strain_list[strain_count],img_list[img_count], omf_path)
            oommf_string = "%s %s %s" % (path_tcl, path_boxsi,path_mif_file)
            print (' %s \n') % (oommf_string)
            localtime = time.asctime( time.localtime(time.time()) )
            print "Start time :", localtime
            subprocess.call(oommf_string)
            print('Running OOMMF script number %d...') % (img_count)
            localtime = time.asctime( time.localtime(time.time()) )
            print "End time :", localtime,"\n"

            
            # For updating the strain list while the python script is running
            # wait_string = raw_input('Please update file strains.txt and press enter.')
            while True:
                try:
                    strain_list_new = open('./strains.txt').read().splitlines()
                    if strain_list != strain_list_new:
                        strain_list = strain_list_new
                        print(strain_list)
                        print('New list loaded successfully');
                    break
                except ValueError:
                    print('Error loading new strain file\nWill try again next time.')
            strain_list_length = len(strain_list)
            strain_count = strain_count + 1
        
        # Reload img_list and check if they are the same
        # wait_string = raw_input('Please update file structures.txt and press enter.')
        while True:
            try:
                img_list_new = open('./structures.txt').read().splitlines()
                if img_list != img_list_new:
                    img_list = img_list_new
                    print(img_list)
                    print('New list loaded successfully');
                break
            except ValueError:
                print('Error loading new structure file\nWill try again next time.')
        img_list_length = len(img_list)
        img_count = img_count + 1



if __name__ == "__main__":
    main()


# cmdstring = "some_other_script.py %s %s" % (argument1 argument2)
# os.system(cmdstring)

#the internet seems to prefer the use of 'subprocess' and 'call':
#no idea how to get it to work
#subprocess.call("dir")


