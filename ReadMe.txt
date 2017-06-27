%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@author    : Avichal Malhotra
@Date      : 21.01.2017
@Decription: This GUI is created to import data from the csvs to the HDF5 datasets.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Dynamics of the Algorithm:

[Button 1] -->  [Button 2] --> [Button 3] --> [Button 4] --> [Button 5]
  [XML]    -->   [Input]   -->  ['.h5']   -->    [Run]   -->   [Exit]

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

"""Functionality of the GUI"""

The GUI consistes of 5 buttons that can be selected.

1. "Choose the input XML file"  : This button is created to select the input XML file where the project name
                                  and the '.h5' file is created with the project name.

2. "Choose Input Data Folder"   : This pushbutton allows the user to select the folder from which the CSV 
                                  data has to be selected. This data is further imported into the '.h5' datasets.

3. "Choose file to be written"  : This pushbutton selects the already created '.h5' file that has been created using
				  the first "Choose the input XML file" button.

4. "RUN"                        : This button runs the algorithm and the groups, datasets and the data is imported 
				  into the '.h5' file.  

5. "EXIT"                       : This buttons opens a dialog box to be sure that the user wants to quit the program.
				  The window exits when the Exit ccommand is given.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%