# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinytorchtest']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'tinytorchtest',
    'version': '0.7.1',
    'description': 'A tiny test suite for pytorch based machine learning models.',
    'long_description': '# Tiny Torchtest\n\nA Tiny Test Suite for pytorch based Machine Learning models, inspired by\n[mltest](https://github.com/Thenerdstation/mltest/blob/master/mltest/mltest.py).\nChase Roberts lists out 4 basic tests in his [medium\npost](https://medium.com/@keeper6928/mltest-automatically-test-neural-network-models-in-one-function-call-eb6f1fa5019d)\nabout mltest. torchtest is mostly a pytorch port of mltest(which was\nwritten for tensorflow).\n\n--- \n\nForked from [BrainPugh](https://github.com/BrianPugh/torchtest) who\nforked the repo from\n[suriyadeepan](https://github.com/suriyadeepan/torchtest).\n\nNotable changes:\n\n-   Support for models to have multiple positional arguments.\n\n-   Support for unsupervised learning.\n\n-   Fewer requirements (due to streamlining testing).\n\n-   More comprehensive changes.\n\n-   This repository is still active. I\'ve created an\n    [issue](https://github.com/suriyadeepan/torchtest/issues/6) to\n    double check but it looks like the original maintainer is no longer\n    actioning pull requests.\n\n---\n\n# Installation\n\n``` bash\npip install --upgrade torchtest\n```\n\n# Tests\n\n``` python\n# imports for examples\nimport torch\nimport torch.nn as nn\nimport torch.nn.functional as F\nfrom torch.autograd import Variable\n```\n\n## Variables Change\n\n``` python\nfrom torchtest import assert_vars_change\n\ninputs = Variable(torch.randn(20, 20))\ntargets = Variable(torch.randint(0, 2, (20,))).long()\nbatch = [inputs, targets]\nmodel = nn.Linear(20, 2)\n\n# what are the variables?\nprint(\'Our list of parameters\', [ np[0] for np in model.named_parameters() ])\n\n# do they change after a training step?\n#  let\'s run a train step and see\nassert_vars_change(\n    model=model,\n    loss_fn=F.cross_entropy,\n    optim=torch.optim.Adam(model.parameters()),\n    batch=batch)\n```\n\n``` python\n""" FAILURE """\n# let\'s try to break this, so the test fails\nparams_to_train = [ np[1] for np in model.named_parameters() if np[0] is not \'bias\' ]\n# run test now\nassert_vars_change(\n    model=model,\n    loss_fn=F.cross_entropy,\n    optim=torch.optim.Adam(params_to_train),\n    batch=batch)\n\n# YES! bias did not change\n```\n\n## Variables Don\'t Change\n\n``` python\nfrom torchtest import assert_vars_same\n\n# What if bias is not supposed to change, by design?\n#  test to see if bias remains the same after training\nassert_vars_same(\n    model=model,\n    loss_fn=F.cross_entropy,\n    optim=torch.optim.Adam(params_to_train),\n    batch=batch,\n    params=[(\'bias\', model.bias)]\n    )\n# it does? good. let\'s move on\n```\n\n## Output Range\n\n``` python\nfrom torchtest import test_suite\n\n# NOTE : bias is fixed (not trainable)\noptim = torch.optim.Adam(params_to_train)\nloss_fn=F.cross_entropy\n\ntest_suite(model, loss_fn, optim, batch,\n    output_range=(-2, 2),\n    test_output_range=True\n    )\n\n# seems to work\n```\n\n``` python\n""" FAILURE """\n#  let\'s tweak the model to fail the test\nmodel.bias = nn.Parameter(2 + torch.randn(2, ))\n\ntest_suite(\n    model,\n    loss_fn, optim, batch,\n    output_range=(-1, 1),\n    test_output_range=True\n    )\n\n# as expected, it fails; yay!\n```\n\n## NaN Tensors\n\n``` python\n""" FAILURE """\nmodel.bias = nn.Parameter(float(\'NaN\') * torch.randn(2, ))\n\ntest_suite(\n    model,\n    loss_fn, optim, batch,\n    test_nan_vals=True\n    )\n```\n\n## Inf Tensors\n\n``` python\n""" FAILURE """\nmodel.bias = nn.Parameter(float(\'Inf\') * torch.randn(2, ))\n\ntest_suite(\n    model,\n    loss_fn, optim, batch,\n    test_inf_vals=True\n    )\n```\n\n# Debugging\n\n``` bash\ntorchtest\\torchtest.py", line 151, in _var_change_helper\nassert not torch.equal(p0, p1)\nRuntimeError: Expected object of backend CPU but got backend CUDA for argument #2 \'other\'\n```\n\nWhen you are making use of a GPU, you should explicitly specify\n`device=cuda:0`. By default `device` is set to `cpu`. See [issue\n#1](https://github.com/suriyadeepan/torchtest/issues/1) for more\ninformation.\n\n``` python\ntest_suite(\n    model,  # a model moved to GPU\n    loss_fn, optim, batch,\n    test_inf_vals=True,\n    device=\'cuda:0\'\n    )\n```\n\n# Citation\n\n``` tex\n@misc{Ram2019,\n  author = {Suriyadeepan Ramamoorthy},\n  title = {torchtest},\n  year = {2019},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/suriyadeepan/torchtest}},\n  commit = {42ba442e54e5117de80f761a796fba3589f9b223}\n}\n```\n',
    'author': 'Alex',
    'author_email': 'adrysdale@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abdrysdale/tinytorchtest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
