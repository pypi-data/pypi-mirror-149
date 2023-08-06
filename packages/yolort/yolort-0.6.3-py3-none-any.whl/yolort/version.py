__version__ = '0.6.3'
git_version = '006f3f69f635e03f8e47e10b4a575439a1c0ebec'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
