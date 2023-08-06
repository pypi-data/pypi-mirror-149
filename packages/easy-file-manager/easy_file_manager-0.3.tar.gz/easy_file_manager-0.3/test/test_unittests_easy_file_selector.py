import unittest

from easy_file_manager.easy_file_manager import EasyFileSelect


class TestStringMethod(unittest.TestCase):

    def test_001_instantiate_easy_file_select(self):
        '''
            Test instantiating a member of the class EasyFileSelect
        '''

        # Instantiate instance
        instance = EasyFileSelect(debug=True)

    def test_002_select_files(self):
        '''
            Test letting user pick files
        '''

        # Instantiate instance
        instance = EasyFileSelect(debug=True)
        # Let user select files in the file selector
        instance.file_selection(title='DEBUG: Unitest',
                                button_labels=['Choose file', 'Remove file', 'Open selection', 'Scroll to top'],
                                preload=list())


if __name__ == '__main__':
    unittest.main()
