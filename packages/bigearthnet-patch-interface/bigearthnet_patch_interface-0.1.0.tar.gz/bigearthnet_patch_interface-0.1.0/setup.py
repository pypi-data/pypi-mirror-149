# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigearthnet_patch_interface']

package_data = \
{'': ['*'],
 'bigearthnet_patch_interface': ['tiny_s2/S2A_MSIL2A_20170617T113321_36_85/*']}

install_requires = \
['natsort>=8,<9', 'numpy>=1.21,<2.0', 'pydantic>=1.9,<2.0']

setup_kwargs = {
    'name': 'bigearthnet-patch-interface',
    'version': '0.1.0',
    'description': 'A simple interface class that includes all the relevant information about BigEarthNet patches.',
    'long_description': '# BigEarthNet Patch Interface\n[![Tests](https://img.shields.io/github/workflow/status/kai-tub/bigearthnet_patch_interface/CI?color=dark-green&label=%20Tests)](https://github.com/kai-tub/bigearthnet_patch_interface/actions/workflows/main.yml)\n[![License](https://img.shields.io/pypi/l/bigearthnet_patch_interface?color=dark-green)](https://github.com/kai-tub/bigearthnet_patch_interface/blob/main/LICENSE)\n[![PyPI version](https://badge.fury.io/py/bigearthnet-patch-interface.svg)](https://pypi.org/project/bigearthnet-patch-interface/)\n[![Auto Release](https://img.shields.io/badge/release-auto.svg?colorA=888888&colorB=9B065A&label=auto&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAACzElEQVR4AYXBW2iVBQAA4O+/nLlLO9NM7JSXasko2ASZMaKyhRKEDH2ohxHVWy6EiIiiLOgiZG9CtdgG0VNQoJEXRogVgZYylI1skiKVITPTTtnv3M7+v8UvnG3M+r7APLIRxStn69qzqeBBrMYyBDiL4SD0VeFmRwtrkrI5IjP0F7rjzrSjvbTqwubiLZffySrhRrSghBJa8EBYY0NyLJt8bDBOtzbEY72TldQ1kRm6otana8JK3/kzN/3V/NBPU6HsNnNlZAz/ukOalb0RBJKeQnykd7LiX5Fp/YXuQlfUuhXbg8Di5GL9jbXFq/tLa86PpxPhAPrwCYaiorS8L/uuPJh1hZFbcR8mewrx0d7JShr3F7pNW4vX0GRakKWVk7taDq7uPvFWw8YkMcPVb+vfvfRZ1i7zqFwjtmFouL72y6C/0L0Ie3GvaQXRyYVB3YZNE32/+A/D9bVLcRB3yw3hkRCdaDUtFl6Ykr20aaLvKoqIXUdbMj6GFzAmdxfWx9iIRrkDr1f27cFONGMUo/gRI/jNbIMYxJOoR1cY0OGaVPb5z9mlKbyJP/EsdmIXvsFmM7Ql42nEblX3xI1BbYbTkXCqRnxUbgzPo4T7sQBNeBG7zbAiDI8nWfZDhQWYCG4PFr+HMBQ6l5VPJybeRyJXwsdYJ/cRnlJV0yB4ZlUYtFQIkMZnst8fRrPcKezHCblz2IInMIkPzbbyb9mW42nWInc2xmE0y61AJ06oGsXL5rcOK1UdCbEXiVwNXsEy/6+EbaiVG8eeEAfxvaoSBnCH61uOD7BS1Ul8ESHBKWxCrdyd6EYNKihgEVrwOAbQruoytuBYIFfAc3gVN6iawhjKyNCEpYhVJXgbOzARyaU4hCtYizq5EI1YgiUoIlT1B7ZjByqmRWYbwtdYjoWoN7+LOIQefIqKawLzK6ID69GGpQgwhhEcwGGUzfEPAiPqsCXadFsAAAAASUVORK5CYII=)](https://github.com/intuit/auto)\n<!-- [![Conda Version](https://img.shields.io/conda/vn/conda-forge/bigearthnet-patch-interface?color=dark-green)](https://anaconda.org/conda-forge/bigearthnet-patch-interface) -->\n\n\nA common issue when using a BigEarthNet archive is that the code to load a patch is\n- Slow\n- The necessary libraries to load the data have complex dependencies and cause issues with popular deep-learning libraries\n  - The issue is often caused by a binary mismatch between the underlying `numpy` versions\n- Hard to understand how to access the optimized data\n\nA popular approach is to use the key-value storage [LMDB](https://lmdb.readthedocs.io/en/release/).\nThe patch names are set as a key, and the value is _somehow_ encoded.\nDecoding the values is a common source of bugs when different deep-learning libraries are used.\n\nThe goal of this repository is to alleviate this issue.\nTo support most popular deep-learning libraries, the actual image data will be encoded as `numpy` arrays.\nUsually, these arrays can be loaded without copying the underlying data.\n\nThe provided patch interface will define a Python class containing the 12 bands, encoded as an `np.ndarray`, and may include some metadata.\nThe class allows for fast introspection, validation, and data loading.\n\nIn general, the encoding pipeline is as follows:\n1. To convert the BigEarthNet patches into numpy arrays\n2. Use these arrays to initialize the interface class\n3. Provide any additional metadata information to the interface\n4. Pickle the instance\n5. Store the instance to an LMDB database as a value (usually, the name of the patch is used as the key)\n\nOnly the LMDB database and the interface class are required to load the pre-converted data.\nThis repository only contains the interface to minimize the required dependencies to unpickle the data.\n\nPlease be aware that pickle is **insecure**, and pickled data should **never** be trusted.\nFor a detailed review on `pickle`, see the following post of [synopsys on pickling](https://www.synopsys.com/blogs/software-security/python-pickling/).\nThe primary benefit of pickle is that it comes with Python (requires no heavy dependencies), is blazingly fast, and allows for efficient serialization of various data types.\n\nDo not forget to restrict write access to the pickled files when using them in a shared environment!\n',
    'author': 'Kai Norman Clasen',
    'author_email': 'k.clasen@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai-tub/bigearthnet_patch_interface/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
