#------------------------------------------#
# Title: CD_Inventory.py
# Desc: The CD Inventory App main Module
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# DBiesinger, 2030-Jan-02, Extended functionality to add tracks
# PBandy, 2020-Sep-09, Added initiate_cd_inventory()
# PBandy, 2020-Sep-09, Added code for "Add CD" option
#------------------------------------------#

import ProcessingClasses as PC
import IOClasses as IO

lstFileNames = ['AlbumInventory.txt', 'TrackInventory.txt']
IO.FileIO.initiate_cd_inventory(lstFileNames)
lstOfCDObjects = IO.FileIO.load_inventory(lstFileNames)

while True:
    IO.ScreenIO.print_menu()
    strChoice = IO.ScreenIO.menu_choice()

    if strChoice == 'x':
        break
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('Type \'yes\' to continue and reload from file. Otherwise, reload will be canceled:\n')
        if strYesNo.lower() == 'yes':
            print('Reloading...')
            lstOfCDObjects = IO.FileIO.load_inventory(lstFileNames)
            IO.ScreenIO.show_inventory(lstOfCDObjects)
        else:
            input('Canceling... inventory data not reloaded. Press [ENTER] to continue to the menu.')
            IO.ScreenIO.show_inventory(lstOfCDObjects)
        continue  # start loop back at top.
    elif strChoice == 'a':
        tplCdInfo = IO.ScreenIO.get_CD_info()
        PC.DataProcessor.add_CD(tplCdInfo, lstOfCDObjects)
        IO.ScreenIO.show_inventory(lstOfCDObjects)
        continue  # start loop back at top.
    elif strChoice == 'd':
        IO.ScreenIO.show_inventory(lstOfCDObjects)
        continue  # start loop back at top.
    elif strChoice == 'c':
        IO.ScreenIO.show_inventory(lstOfCDObjects)
        cd_idx = input('Select the CD / Album index: \n')
        cd_object = PC.DataProcessor.select_cd(lstOfCDObjects, cd_idx)
        
        while True:
            IO.ScreenIO.print_CD_menu(cd_idx)
            sub_menu_choice = IO.ScreenIO.menu_CD_choice()
            print()

            if sub_menu_choice == 'x':
                break
            elif sub_menu_choice == 'a':
                # Add track
                track_tuple = IO.ScreenIO.get_track_info()
                track_tuple += (cd_object.cd_id,)
                PC.DataProcessor.add_track_from_tuple(track_tuple, cd_object)
            elif sub_menu_choice == 'd':
                # Display CD / Album details
                try:
                    IO.ScreenIO.show_tracks(cd_object)
                except Exception as e:
                    if str(e) == 'No tracks saved for this Album':
                        print('\nNo tracks saved for this Album\n')
                        continue
                    else:
                        raise Exception('General error!')
            elif sub_menu_choice == 'r':
                # Remove track
                IO.ScreenIO.show_tracks(cd_object)
                track_id = input('Select the track to delete: \n')
                cd_object.rmv_track(int(track_id))
            else:
                print('Invalid selection')
                continue
    elif strChoice == 's':
        IO.ScreenIO.show_inventory(lstOfCDObjects)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        if strYesNo == 'y':
            IO.FileIO.save_inventory(lstFileNames, lstOfCDObjects)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    else:
        print('General Error')