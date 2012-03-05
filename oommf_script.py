# oommf script test
##C:\Tcl\bin\tclsh84.exe C:\oommf\oommf.tcl boxsi -exitondone 0
##-parameters "Ks %1 "
##C:/oommf/duncan/FeGa_Simulations/FeGa_Bar_Field_1.mif
def main():
    import os
    import subprocess
    import time
    path_tcl = 'C:/Tcl/bin/tclsh84'
    path_boxsi_base = 'C:/oommf/oommf.tcl boxsi -exitondone 1 -parameters'
    path_mif_file = './FeGa_Bar_Field_1.mif'
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
    strain_list = ['0']
    # loop through the different devices
    ##array_length = len(list1)
    ##x = 0
    ##while x < array_length:
    ##    list1 = list2
    ##    print(list1[x])
    ##    x = x + 1
    ##    array_length = len(list1)
    img_count = 0
    img_list_length = len(img_list)
    while img_count < img_list_length:
                      
        ##        Set the output directory name. if this directory doesn't
        ##        exist make it. This means that we can have an automatic
        ##        output folder in the mif file.
        img_dir = '../output/%s' % (img_count)
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)

        # loop through different values of strain energy for each of
        # the devices
        for strain_count in strain_list:
            path_boxsi = path_boxsi_base + ' \"Ks %s img %s \"' % (strain_count,img_list[img_count])
            oommf_string = "%s %s %s" % (path_tcl, path_boxsi,path_mif_file)
            print (' %s \n') % (oommf_string)
            localtime = time.asctime( time.localtime(time.time()) )
            print "Start time :", localtime
            subprocess.call(oommf_string)
            print('Running OOMMF script number %d...') % (img_count)
            localtime = time.asctime( time.localtime(time.time()) )
            print "End time :", localtime,"\n"
        #            I want the script to output the start and end time.
        ## Reload img_list and check if they are the same
        wait_string = raw_input('Please update file structures.txt and press enter.')
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


