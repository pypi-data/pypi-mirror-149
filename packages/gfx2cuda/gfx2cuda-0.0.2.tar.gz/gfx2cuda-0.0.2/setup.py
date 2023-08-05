# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gfx2cuda', 'gfx2cuda.dll']

package_data = \
{'': ['*']}

install_requires = \
['comtypes>=1.1.7,<1.2.0', 'numpy>=1.16.5,<1.17.0']

setup_kwargs = {
    'name': 'gfx2cuda',
    'version': '0.0.2',
    'description': 'Fast graphics texture to cuda transfer',
    'long_description': '# Gfx2Cuda - Graphics to CUDA interoperability\n\n_Gfx2Cuda_ is a python implementation of CUDA\'s graphics interopability methods for DirectX, OpenGL, etc.\nThe main usage is for quick transfer of images rendered with for example Godot or Unity to CUDA memory buffers such as \npytoch tensors, without needing to transfer the image to cpu and back to gpu.\n\nFor now only DirectX 11 is supported. This can be useful for implementing CUDA ipc (interprocess-communication) for \nWindows, since that functionality is not available in vanilla CUDA for Windows. \nYou would use a DirectX texture as buffer that can be seen by multiple processes without having to download any gpu data\nto cpu and back.\n\n### Example\n\n**Render to texture and copy to pytorch tensor**\n\n```python\nimport gfx2cuda\nimport torch\n\n# Shape: [height, width, channels]\nshape = [480, 640, 4]\ntensor1 = torch.ones(shape).contiguous().cuda()\ntensor2 = torch.zeros(shape).contiguous().cuda()\n\n# Create copy of a tensor but as a texture\ntex = gfx2cuda.texture(tensor1)\n\nwith tex as ptr:\n    tex.copy_to(tensor2)\n\nprint(tensor2.data)\n# pytorch tensor should now contain a copy of the texture data\n```\n\n**Share texture between process, write on one process and see results in the other**\n\n```python\nfrom multiprocessing import Process\n\nimport gfx2cuda\nimport torch\n\nshape = [4, 4, 4]\n\ndef f(handle):\n    tex = gfx2cuda.open_ipc_texture(handle)\n    # Received and opened the texture\n    print(tex)\n    # >> Texture with format TextureFormat.RGBA32FLOAT (4 x 4)\n    tensor1 = torch.ones(shape).contiguous().cuda()\n    with tex:\n        tex.copy_from(tensor1)\n\nif __name__ == "__main__":\n    tensor = torch.zeros(shape).contiguous().cuda()\n    # Initialize as all zeros\n    tex = gfx2cuda.texture(tensor)\n\n    p = Process(target=f, args=(tex.ipc_handle,))\n    p.start()\n    p.join()\n\n    with tex:\n        tex.copy_to(tensor)\n\n    print(tensor.data)\n    # See all ones\n```\n',
    'author': 'Sven den Hartog',
    'author_email': 'denhartog.sven@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SvenDH/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
