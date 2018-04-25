# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 15:54:56 2018

@author: abhim
"""
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd

"""
This function takes two sets of OKTA- CMDB APP names, and produces a  a set number (default=5)
of matches with a score that shows the percentage of match
 
master: file containing the master list of okta application names
using: file containing using list of CMDB applicaiton names, each of these is matches against the universe of okta application names from the master file
The choice of matching applications is written to Application_Matches.csv
Non matching applicaiton names are written to Application_Non_Matches.csv
"""

def matcher(master, using, master_name, master_Id, using_Name, using_Id):
    master_dists = pd.read_csv(master,encoding = "ISO-8859-1", skipinitialspace = True, sep = ',')
    using_dists = pd.read_csv(using,encoding = "ISO-8859-1", skipinitialspace = True, sep = ',')
    
    master = master_dists.set_index("Okta_ID").Display_Name.to_dict()
    master_full_df = pd.DataFrame(master_dists,columns=["Display_Name", "Okta_ID"])
    using_df = pd.DataFrame(using_dists,columns=["Application_Name", "Application_ID"])
    
    columnTitleRow = "Application_Name, App_Id, Okta_Name, Okta_Id \n"
    with open("C:/Users/abhim/Application_Matches.csv", 'a') as csvoutput:        
        csvoutput.write(columnTitleRow)
        for i,id in list(zip(master_full_df.iloc[:,0],master_full_df.iloc[:,1])):
            for found,score,matchrow in process.extract(i, using_df.iloc[:,0],scorer=fuzz.token_sort_ratio):
                if score == 100:
                    Okta_Id = id
                    App_Id = using_df['Application_ID'].get(matchrow,"00")
                    full_matches = found + "," + App_Id +"," + i + "," + Okta_Id
                    csvoutput.write(full_matches + "\n")
    columnTitleRow_NM = "Application_Name, App_Id, Okta_Name, Okta_Id \n"
    with open("C:/Users/abhim/Application_Non_Matches.csv", 'a') as csvoutput_NM:        
        csvoutput_NM.write(columnTitleRow_NM)
    
    print ("Welcome to matcher.py")
    choice = 0
    
    while True:
        
        loop = 1
        
        for i in using_df.index:
            val = using_df.loc[i,'Application_Name']
            id_val = using_df.loc[i,'Application_ID']
            
            
            print("")
            
            print ("Application_Name:"+ val)
        
            print ("Your options are:")
            

            extract = process.extract(val, master, limit=5,scorer=fuzz.token_sort_ratio)
            data = [possible for possible in extract if possible[1] <= 99]
            master_df = pd.DataFrame(data,columns = ["matched" , "score","Id"])
            #print (master_df)
            
            for number,(index, row) in enumerate(master_df.iterrows(),1):
                
                print("Option",number,":",row['matched'] , ", Score:",row['score'])
            print("***********************************************************************")
            print ("Option 6: No Matches  Option 7: Quit matcher.py  Option 8: Remove a Match")
            
            while 1:
                
                
                #choice = int(choice)
                with open("C:/Users/abhim/Application_Matches.csv", 'a') as csvoutput:
                    
                    try:
                        choice = int(input("Choose your option: "))
                    
                
                        if choice == 1:                
                            line = val + "," + id_val +"," + master_df['matched'].iloc[0] + "," + master_df['Id'].iloc[0] 
                            print (line)
                            csvoutput.write(line + "\n")
    
                        elif choice == 2:
                            line = val+ "," + id_val  + "," + master_df['matched'].iloc[1] + "," + master_df['Id'].iloc[1] 
                            print (line)
                            csvoutput.write(line + "\n")
                        elif choice == 3:
                            line = val + "," + id_val  + "," + master_df['matched'].iloc[2] + "," + master_df['Id'].iloc[2] 
                            print (line)
                            csvoutput.write(line + "\n")
                        elif choice == 4:
                            line = val + "," + id_val  + "," + master_df['matched'].iloc[3] + "," + master_df['Id'].iloc[3] 
                            print (line)
                            csvoutput.write(line + "\n")
                        elif choice == 5:
                            line = val + "," + id_val  + "," + master_df['matched'].iloc[4] + "," + master_df['Id'].iloc[4] 
                            print (line)
                            csvoutput.write(line + "\n")
                        elif choice ==6:
                            print("No Matches")
                            with open("C:/Users/abhim/Application_Non_Matches.csv", 'a') as csvoutput_NM:
                                line_NM= val + "," + id_val 
                                csvoutput_NM.write(line_NM + "\n")
                        
                        elif choice == 7:
                            print ("Thankyou for using matcher.py!" )
                            os._exit(0)
                        elif int(choice) == 8:
                            user_input = input("Enter the choice you want to delete:")
                            with open("C:/Users/abhim/Application_Matches.csv", "r+") as f:
                                new_f = f.readlines()
                                f.seek(0)
                                for line in new_f:
                                    del_data = int(user_input) - 1#
                                    del_line = master_df['matched'].iloc[del_data]
                                    if del_line not in line:
                                        f.write(line)
                                f.truncate()
                    except:
                        break
                  

                    
                            

                    
    
    
    loop+=1
    
       
 
# -- Replace below path with your correct directory structure
baseDir = os.path.join("C:/Users/abhim")
"""
MATCHING CMDB APPLICATIONS FILE and OKTA APPLICATION FILE
"""
master_file = os.path.join(baseDir, "okta_applications.csv")
CMDB_file = os.path.join(baseDir, "CMDB_ApplicationsUAT.csv")

 
def main():
    matcher( master_file, CMDB_file, 'Display_Name', 'Okta_ID' , 'Application_Name', 'Application_ID')
    #print (app_matches)
main()


 