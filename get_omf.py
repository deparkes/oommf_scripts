def get_omf(path):
    import glob
    # os.chdir('../output/15um90umBarWithCrosses.bmp/strain_0');
    os.chdir(path);
    files = glob.glob('*.omf')
    omf_file = files[0]
    return omf_file
    

