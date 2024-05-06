from astropy.time import Time
import os
from astroquery.mast import Observations
import numpy as np
import pandas as pd
import glob
from astropy.io import fits
#Get all the IDs for the target

#AllProposalIDs = np.genfromtxt('obs_table.csv', delimiter="&", dtype='str', skip_header=1)
#print(AllProposalIDs)

AllData = pd.read_csv('obs_table.csv', delimiter=",")
AllProposalIDs = np.array(AllData['proposal_id'])
ProposalIDsUnique = np.unique(AllProposalIDs)

AllInstrumentName = np.array(AllData['instrument_name'])
AllFilters = np.array(AllData['filters'])
AllRA = np.array(AllData['s_ra'])
AllDEC = np.array(AllData['s_dec'])


#Get the proposal IDs
AllTargetName = np.array(AllData['target_name'])

AllUniqueTargetName = np.unique(AllTargetName)[9:]
file_path = os.path.dirname(os.path.abspath("__file__"))



for Counter, TargetName in enumerate(AllUniqueTargetName): 
    SelectedProposalID = np.unique(AllProposalIDs[AllTargetName==TargetName])

   
    for ProposalID in SelectedProposalID:
        SelectedInstruments = np.unique(AllInstrumentName[AllProposalIDs==ProposalID])
        
        for Instrument in SelectedInstruments:
            SaveFolder = "HST_"+TargetName.replace(" ", "").replace("-","")+"_"+Instrument
            SaveFolder = SaveFolder.replace("/","_")
            
            if "HST_ANY" in SaveFolder:
                continue
            if "HST_CCDFLAT" in SaveFolder:
                continue
            #removing the directory if it already exists.
            os.system("rm -rf mastDownload")

            print("*"*100)
            print("The save folder is: ", SaveFolder)
            print("The proposal ID is: ", ProposalID)
            print("*"*100)

            proposal_obs = Observations.query_criteria(proposal_id=int(ProposalID), instrument_name=Instrument, project='HST')
            data_products = Observations.get_product_list(proposal_obs)
            

            data_products_ima = data_products[data_products['productSubGroupDescription'] == 'IMA']
            
            Text = "Successfully downloaded:" +SaveFolder +","+str(ProposalID)+","+Instrument+"\n" 
            try:
                Observations.download_products(data_products_ima,mrp_only=False)   
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


            #input("Wait here...")    
            #except:
            #    Text = "Problem with reading:", FileItem
                #    with open("DownloadLog.txt", "a") as f:
                #        f.write(Text)
                #    print(Text)
                #    continue
