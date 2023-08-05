"""Setup script for object_detection with TF2.0."""
from os import path
from setuptools import find_packages
from setuptools import setup
from glob import glob
from typing import List
import shutil


def get_model_zoo_configs() -> List[str]:
    """
    Return a list of configs to include in package for model zoo. Copy over these configs inside
    detectron2/model_zoo.
    """

    # Use absolute paths while symlinking.
    source_configs_dir = path.join(path.dirname(path.realpath(__file__)), "configs")
    destination = path.join(
        path.dirname(path.realpath(__file__)), "detectron2", "model_zoo", "configs"
    )
    # Symlink the config directory inside package to have a cleaner pip install.

    # Remove stale symlink/directory from a previous build.
    if path.exists(source_configs_dir):
        if path.islink(destination):
            path.unlink(destination)
        elif path.isdir(destination):
            shutil.rmtree(destination)

    if not path.exists(destination):
        try:
            path.symlink(source_configs_dir, destination)
        except OSError:
            # Fall back to copying if symlink fails: ex. on Windows.
            shutil.copytree(source_configs_dir, destination)

    config_paths = glob.glob("configs/**/*.yaml", recursive=True) + glob.glob(
        "configs/**/*.py", recursive=True
    )
    return config_paths

# Note: adding apache-beam to required packages causes conflict with
# tf-models-offical requirements. These packages request for incompatible
# oauth2client package.


REQUIRED_PACKAGES = [
    # Required for apache-beam with PY3
    'absl-py>=0.8.1',
    'astor>=0.8.0',
    'Click>=7.0',
    'gast>=0.3.2',
    'google-pasta>=0.1.7',
    'grpcio>=1.24.1',
    'h5py>=2.10.0',
    'requests',
    'itsdangerous>=1.1.0',
    'Jinja2>=2.10.3',
    'Keras-Applications>=1.0.8',
    'Keras-Preprocessing>=1.1.0',
    'Markdown>=3.1.1',
    'MarkupSafe>=1.1.1',
    'numpy>=1.17.2',
    'opencv-python',
    'Pillow>=6.2.0',
    'protobuf>=3.10.0',
    'six>=1.12.0',
    'tensorboard==2.5.0',
    'tensorflow==2.5.0',
    'tensorflow-estimator==2.5.0',
    'termcolor==1.1.0',
    'Werkzeug==0.16.0',
    'wincertstore==0.2',
    'wrapt>=1.11.2',
    'tf_slim',
    'gdown',
    'Cython',
    'PyYAML>=5.3',
    'tqdm>=4.41.0',
    'scipy>=1.4.1',
    'fvcore',
    'cloudpickle',
    'pandas',
    'seaborn',
    'torch>=1.7.0'
    'torchvision>=0.8.1'
]

files = ['*.yaml','detectron2/model_zoo/configs/*']
setup(
    name='alphadetector',
    version='0.0.24',
    author='ravikanur',
    url='https://github.com/ravikanur/ObjectDetection_Webapp',
    description='object detection using yolo, tf2 and detectron2',
    project_urls={
        'Bug Tracker': 'https://github.com/ravikanur/ObjectDetection_Webapp/issues',
    },
    install_requires=REQUIRED_PACKAGES,
    include_package_data=True,
    dependency_links=['https://download.pytorch.org/whl/lts/1.8/torch_lts.html'],
    package_dir={"": 'src'},
    packages=find_packages(where='src'),
    package_data={'detectron2.model_zoo': ['configs/*.yaml', 'configs/COCO-Detection/*yaml',
                                           'configs/COCO-Detection/*py']},
    python_requires='>=3.7',
)
