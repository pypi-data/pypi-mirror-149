# Ensure value sets can all be imported


import importlib
from pathlib import Path
from unittest import TestCase
from canvas_workflow_kit import value_set


class SuperValueSetTest(TestCase):

    def test_valuesets(self):
        """
        Test value sets to ensure they compile and can be imported.
        """

        main_path = Path(value_set.__path__[0])

        errors = []

        def test_directory(dir_path):
            for item in dir_path.iterdir():
                if "__pycache__" in str(item):
                    continue

                if item.is_dir():
                    test_directory(item)
                    continue

                if item.suffix == '.py':
                    try:
                        module = importlib.util.spec_from_file_location("canvas_workflow_kit.value_set.v202X", item)
                        module.loader.load_module()
                    except SyntaxError as e:
                        errors.append(f"Syntax error in valueset file: {item} " + str(e))

        test_directory(main_path)
        if errors:
            self.fail('\n'.join(errors))
