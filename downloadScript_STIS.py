#import libraries
from astroquery.mast import Observations
import numpy as np
import pandas as pd
import os
import glob

# Import for: Plotting and specifying plotting parameters
from matplotlib import pyplot as plt
import matplotlib

AllData = pd.read_csv('obs_table.csv', delimiter=",")
ObservationalID = np.unique(np.array(AllData['obs_id']))

Instrument = "STIS"
file_path = os.path.dirname(os.path.abspath("__file__"))

for obs_id in ObservationalID:
    # Search target object by obs_id
    target = Observations.query_criteria(obs_id=obs_id)
    TargetName = str(target['target_name'][0])
    target_list = Observations.get_product_list(target)
    SaveFolder = "HST_"+TargetName.replace(" ", "").replace("-","")+"_"+Instrument
    SaveFolder = SaveFolder.replace("/","_")
    print("The save folder is given by:", SaveFolder)
    
    # Download fits files
    try:
        Observations.download_products(target_list, extension=['_flt.fits', '_x1d.fits'], productType=['SCIENCE'])
        Text = "Successfully downloaded:" +SaveFolder +","+str(obs_id)+","+Instrument+"\n"     
        with open("DownloadLog.txt", "a") as f:
            f.write(Text)
        print(Text) 
    except:
        Text = "Error in downloading:" +SaveFolder+"\n"# +","+ProposalID+","+Instrument 
        with open("DownloadLog.txt", "a") as f:
            f.write(Text)
        print(Text)
        continue
  
        

    root_dir = file_path + '/mastDownload/HST' # Specify root directory to be searched for .sav files.
    move_dir = file_path
    filelist = []

    # list all ima files in the subdirectories
    for tree,fol,fils in os.walk(root_dir):
        filelist.extend([os.path.join(tree,fil) for fil in fils if fil.endswith('.fits')])

    if not(os.path.exists(SaveFolder)):
        os.makedirs("%s" %SaveFolder)

    for fileName in filelist:
        os.system("mv %s %s" %(fileName, SaveFolder))

    #Now check if all the files are in the SaveFolder
    SavedFileList = glob.glob(SaveFolder+"/*.fits")
    
    
    os.system("rm -rf mastDownload")
    print("\n"*10)