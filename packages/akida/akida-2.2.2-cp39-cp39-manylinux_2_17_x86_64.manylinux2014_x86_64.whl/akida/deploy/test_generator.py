import os
from pathlib import Path

from .application_generator import ApplicationGenerator
from .array_to_cpp import array_to_cpp


def _test_file_from_template(test_name, tpl_path, dest_path, filename):
    src_path = os.path.join(tpl_path, filename)
    dst_path = os.path.join(dest_path, test_name, filename)
    with open(src_path, 'r') as src, open(dst_path, 'w') as dst:
        for line in src:
            # Substitute pattern by filename
            dst.write(line.replace("TEST_NAME", test_name))


class TestGenerator(ApplicationGenerator):

    def program(self):
        model = self.model()
        device = self.device()
        if model is not None and device is not None:
            model.map(device, hw_only=True)
            return model.sequences[0].program
        return None

    def model(self):
        """The test Model

        Must be provided by each test application.
        """
        return None

    def device(self):
        """The test Device

        Must be provided by each test application.
        """
        return None

    def inputs(self):
        """The test inputs

        Must be provided by each test application.
        """
        return None

    def outputs(self):
        """The test outputs

        Must be provided by each test application.
        """
        return None

    def generate(self, test_name, dest_path):
        """Generate test application files

        It first calls the default parent generator.

        It then:
        - generate test program input files,
        - generate test program output files,
        - copies test.cpp file from the package resources.
        """
        super().generate(test_name, dest_path)
        inputs = self.inputs()
        outputs = self.outputs()
        dest_dir = os.path.join(dest_path, test_name)
        # Generate source arrays
        if inputs is not None:
            array_to_cpp(dest_dir, inputs, "inputs")
        if outputs is not None:
            array_to_cpp(dest_dir, outputs, "outputs")
        if self.program() is not None:
            tpl_path = os.path.join(Path(__file__).parent, "app_templates")
            # Write test files
            _test_file_from_template(test_name, tpl_path, dest_path, "test.h")
            _test_file_from_template(test_name, tpl_path, dest_path, "test.cpp")
