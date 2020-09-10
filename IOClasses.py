#------------------------------------------#
# Title: IO Classes
# Desc: A Module for IO Classes
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# DBiesinger, 2030-Jan-02, Extended functionality to add tracks
# PBandy, 2020-Sep-09, Added initiate_cd_inventory() method
# PBandy, 2020-Sep-09, Added save_inventory() code
# PBandy, 2020-Sep-09, Added load_inventory() code
# PBandy, 2020-Sep-09, Updated print_CD_menu() method to accept CD ID arg
#------------------------------------------#

if __name__ == '__main__':
    raise Exception('This file is not meant to run by itself')

import DataClasses as DC
import ProcessingClasses as PC

from os import path

class FileIO:
    """Processes data to and from file:

    properties:

    methods:
        save_inventory(file_name, lst_Inventory): -> None
        load_inventory(file_name): -> (a list of CD objects)

    """
    @staticmethod
    def save_inventory(file_name: list, lst_Inventory: list) -> None:
        """
        
        Args:
            file_name (list): list of file names [CD Inventory, Track Inventory] that hold the data.
            lst_Inventory (list): list of CD objects.

        Returns:
            None.

        """

        file_name_cd = file_name[0]
        file_name_track = file_name[1]
        try:
            with open(file_name_cd, 'w') as cd_file:
                for disc in lst_Inventory:
                    cd_file.write(disc.get_record())
                    with open(file_name_track, 'w') as tracks_file:
                        for track in disc.cd_tracks:
                            tracks_file.write(track.get_record())
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n')

    @staticmethod
    def load_inventory(file_name: list) -> list:
        """


        Args:
            file_name (list): list of file names [CD Inventory, Track Inventory] that hold the data.

        Returns:
            list: list of CD objects.

        """
        lst_Inventory = []
        file_name_cd = file_name[0]
        file_name_track = file_name[1]
        try:
            with open(file_name_cd, 'r') as cd_file:
                for cd in cd_file:
                    cd_data = cd.strip().split(',')
                    cd_object = DC.CD(cd_data[0], cd_data[1], cd_data[2])
                    lst_Inventory.append(cd_object)
            with open(file_name_track, 'r') as track_file:
                for track in track_file:
                    track_data = track.strip().split(',')
                    cd = PC.DataProcessor.select_cd(lst_Inventory, int(track_data[3]))
                    track_object = DC.Track(int(track_data[0]), track_data[1], track_data[2], int(track_data[3]))
                    cd.add_track(track_object)
        except Exception as e:
            print('\nError in {}\n'.format('load_inventory'))
            print('{}'.format(e))
        return lst_Inventory

    @staticmethod
    def initiate_cd_inventory(file_names):
        """ Function to create the CDInventory.dat file if it doesn't exist.

        Args: 
            - file_names (list): A list of strings of the names of the files to be created

        Returns: 
            - None
        """
        for file in file_names:
            if not path.exists(file):
                obj_file = open(file, 'wb')
                obj_file.close()


class ScreenIO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Main Menu\n\n[l] load Inventory from file\n[a] Add CD / Album\n[d] Display Current Inventory')
        print('[c] Choose CD / Album\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, d, c, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'd', 'c', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, d, c, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def print_CD_menu(cd_id: str):
        """Displays a sub menu of choices for CD / Album to the user

        Args:
            - cd_id (str): The cd_id of a CD object (CD.cd_id)

        Returns:
            None.
        """

        print(f'CD Sub Menu for CD #{cd_id}\n\n[a] Add track\n[d] Display cd / Album details\n[r] Remove track\n[x] exit to Main Menu')

    @staticmethod
    def menu_CD_choice():
        """Gets user input for CD sub menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices a, d, r or x

        """
        choice = ' '
        while choice not in ['a', 'd', 'r', 'x']:
            choice = input('Which operation would you like to perform? [a, d, r or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print()
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print(row)
        print('======================================')
        print()

    @staticmethod
    def show_tracks(cd):
        """Displays the Tracks on a CD / Album

        Args:
            cd (CD): CD object.

        Returns:
            None.

        """
        print('====== Current CD / Album: ======')
        print(cd)
        print('=================================')
        print(cd.get_tracks())
        print('=================================')

    @staticmethod
    def get_CD_info():
        """function to request CD information from User to add CD to inventory


        Returns:
            cdId (string): Holds the ID of the CD dataset.
            cdTitle (string): Holds the title of the CD.
            cdArtist (string): Holds the artist of the CD.

        """

        cdId = input('Enter ID: ').strip()
        cdTitle = input('What is the CD\'s title? ').strip()
        cdArtist = input('What is the Artist\'s name? ').strip()
        return cdId, cdTitle, cdArtist

    @staticmethod
    def get_track_info():
        """function to request Track information from User to add Track to CD / Album


        Returns:
            trkId (string): Holds the ID of the Track dataset.
            trkTitle (string): Holds the title of the Track.
            trkLength (string): Holds the length (time) of the Track.

        """

        trkId = input('Enter Position on CD / Album: ').strip()
        trkTitle = input('What is the Track\'s title? ').strip()
        trkLength = input('What is the Track\'s length? ').strip()
        return trkId, trkTitle, trkLength

