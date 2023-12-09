import os
try:
    import torch
    _is_torch_available = True
except ImportError:
    _is_torch_available = False

if _is_torch_available:
    from .assets import SOCKET_INSTRUCTIONS
    from .inference import GenLMInferenceWrapper
    from .prompt import PromptTemplater
    import torch
    _torch_version = torch.__version__
    if _torch_version < "1.10.0":
        print (
            "GenLM-Inference-Wrapper requires PyTorch>=1.10.0. The currently installed PyTorch version is {} installed at {}.".format(
                _torch_version, os.path.dirname(torch.__file__)
            )
        )
else:
    print (
        "GenLM-Inference-Wrapper requires PyTorch>=1.10. PyTorch must be installed separately. See https://pytorch.org/get-started/locally/ for installation instructions."
    )