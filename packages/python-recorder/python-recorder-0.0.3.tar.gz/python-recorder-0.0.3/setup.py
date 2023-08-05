# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recorder', 'recorder.device', 'recorder.listener']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.1.1,<3.0.0',
 'PyInquirer>=1.0.3,<2.0.0',
 'PyYAML>=5.1,<6.0',
 'numpy>=1.22.2,<2.0.0',
 'sounddevice>=0.4.4,<0.5.0',
 'typer[all]>=0.4.0,<0.5.0']

extras_require = \
{'all': ['pyrealsense2>=2.50.0,<3.0.0'],
 'realsense': ['pyrealsense2>=2.50.0,<3.0.0']}

entry_points = \
{'console_scripts': ['recorder = recorder.__main__:main']}

setup_kwargs = {
    'name': 'python-recorder',
    'version': '0.0.3',
    'description': '',
    'long_description': '# python-recorder\n\nDevice independent framework for synchronized recording. Originally designed to\nrecord audio and video from a Realsense camera and several microphones. This\nframework is designed for researchers collecting multimodal datasets. It\nprovides an easy command line application which allows to configure, test and\nuse the available sensors in the host machine. The framework can be divided in\ntwo main features:\n\n## Devices\nThey provide a common interface to initialize, `start` and `stop` a recording,\nwhether is a camera, a microphone or any other sensor. When the recording is\nstopped, device parameters (e.g., `samplerate` in microphones, `framerate` in\ncameras) as well as a `start_timestamp` and an `end_timestamp` are saved\ntogether with the recorded data which allows fine synchronization of data from\nmultiple devices in post-processing.\n\nDevices are configurable through a command line application, which searches for\navailable options in the host machine. At the same time, they are saved in a\n[`yaml` formatted text file](./example-config.yaml). Which allows easy access\nto device exclusive configuration parameters.\n\nMultiple devices compose a [`Recorder` object](./recorder/recorder.py), which\nis responsible for initializing all its devices, setup an output folder for the\nrecordings, and start and stop the recording.\n\nAdding new devices classes is simple, one just needs to extend the [`Device`\nclass](./recorder/device/device.py) and override its abstract methods (`find`,\n`_start`, `_stop` and `show_results`).\n\n## Listeners\nResearchers usually want to synchronize the recording with a specific event, a\ntest or experiment, which can be triggered by a different machine. A `Listener`\nis an interface between a `Recorder` and an external event. At the moment, the\nonly one available is a [`Localhost`\nlistener](./recorder/listener/localhost.py). Which triggers the recording\naccording to `GET` requests through the local network. But additional listeners\ncan be added by extending the [`Listener`\nclass](./recorder/listener/listener.py) and overriding its abstract methods. An\nexample of another listener would be a `ROS` node that subscribes to a specific\ntopic and triggers the recording according to a specific set of messages.\n\nListeners can be setup through the `listen`. This command does not initialize\nthe devices. The listener is responsible of executing `recorder.setup()` as it\nsees fit. In the case of the `localhost` listener, a `GET` request to the\n`/setup` endpoint is necessary before trying to start the recording via the\n`/start` endpoint.\n\n# Setup\nIt is recommended to use a virtual environment in order to isolate the\ninstallation, as it provides a command line interface named `recorder` that can\nconflict with other system packages.\n\n```\npython -m venv venv\n````\n\nActivate the environment on Windows:\n\n```\nvenv\\Scripts\\activate\n```\n\nor on MacOS and Linux:\n\n```\nsource venv/bin/activate\n```\n\nInstall from [Pypi](https://pypi.org/project/python-recorder/). There are\noptional dependencies that define which devices and listeners are available,\ndue to the fact some of these dependencies are not available for all operative\nsystems. Check [extras](#extras) for more information about it.\n```\npip install python-recorder[all]\n```\n\nor install this repository to use the latest development versions.\n```\npip install git+https://github.com/AcousticOdometry/python-recorder.git[all]\n```\n\n## Extras\nExtras can be installed through [the `pip install`\ncommand](https://pip.pypa.io/en/stable/cli/pip_install/#requirement-specifiers)\nby specifying them at the end of the package name:\n\n```\npip install python-recorder[extra_one,extra_two]\n```\n\nThe available extras are defined in [`pyproject.toml`](./pyproject.toml) and\nare described here:\n\n- `realsense`: [Intel\n    Realsense](https://www.intel.com/content/www/us/en/architecture-and-technology/realsense-overview.html)\n    devices depend on [pyrealsense2](https://pypi.org/project/pyrealsense2/).\n- `all`: All the extras defined above.\n\n# Usage\nCheck the usage with the `--help` option:\n```\nrecorder --help\n```\n\n# Workflow\n\nConfigure the devices to be used. One can always modify the configuration\nmanually in the generated `yaml` file.\n```\nrecoder config\n```\n\nTest that the chosen audio devices are working\n```\nrecorder test microphone\n```\n\nRecord an experiment with the configured devices\n```\nrecorder record\n```\n\nListen to `GET` requests through the local network\n```\nrecorder listen localhost\n```\n\n# Contributing\nWe are open to contributions. Please, feel free to open an issue or pull\nrequest with any improvement or bug report. The framework is simple and easily\nextensible, it should fit easily in many projects.\n\n## TODO\n\n- [ ] ROS listener\n- [ ] Complete test suite\n- [ ] Camera device with `OpenCV`\n- [ ] Speedup the configuration file creation with compiled code?',
    'author': 'Andreu Gimenez',
    'author_email': 'esdandreu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
