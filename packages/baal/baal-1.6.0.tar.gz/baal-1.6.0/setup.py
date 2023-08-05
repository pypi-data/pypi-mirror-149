# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baal',
 'baal.active',
 'baal.active.dataset',
 'baal.active.heuristics',
 'baal.bayesian',
 'baal.calibration',
 'baal.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=6.2.0',
 'h5py>=3.4.0,<4.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'numpy>=1.21.2,<2.0.0',
 'scikit-learn>=1.0.0,<2.0.0',
 'scipy>=1.7.1,<2.0.0',
 'structlog>=21.1.0,<22.0.0',
 'torch>=1.6.0',
 'tqdm>=4.62.2,<5.0.0']

extras_require = \
{'nlp': ['transformers>=4.10.2,<5.0.0', 'datasets>=1.11.0,<2.0.0'],
 'vision': ['torchvision>=0.7.0']}

setup_kwargs = {
    'name': 'baal',
    'version': '1.6.0',
    'description': 'Library to enable Bayesian active learning in your research or labeling work.',
    'long_description': '<p align="center">\n  <img height=15% width=25% src="https://github.com/ElementAI/baal/blob/master/docs/_static/images/logo-transparent.png?raw=true">\n  <h1 align="center">Bayesian Active Learning (BaaL)\n   <br>\n  <a href="https://circleci.com/gh/ElementAI/baal">\n    <img alt="CircleCI" src="https://circleci.com/gh/ElementAI/baal.svg?style=svg&circle-token=aa12d3134798ff2bf8a49cebe3c855b96a776df1"/>\n  </a>\n  <a href="https://baal.readthedocs.io/en/latest/?badge=latest">\n    <img alt="Documentation Status" src="https://readthedocs.org/projects/baal/badge/?version=latest"/>\n  </a>\n  <a href="https://join.slack.com/t/baal-world/shared_invite/zt-z0izhn4y-Jt6Zu5dZaV2rsAS9sdISfg">\n    <img alt="Slack" src="https://img.shields.io/badge/slack-chat-green.svg?logo=slack"/>\n  </a>\n  <a href="https://github.com/Elementai/baal/blob/master/LICENSE">\n    <img alt="Licence" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"/>\n  </a>\n  </h1>\n</p>\n\n\nBaaL is an active learning library developed at\n[ElementAI](https://www.elementai.com/). This repository contains techniques\nand reusable components to make active learning accessible for all.\n\nRead the documentation at https://baal.readthedocs.io.\n\nOur paper can be read on [arXiv](https://arxiv.org/abs/2006.09916). It includes tips and tricks to make active learning usable in production.\n\nIn this [blog post](https://www.elementai.com/news/2019/element-ai-makes-its-bayesian-active-learning-library-open-source), we present our library.\n\nFor a quick introduction to BaaL and Bayesian active learning, please see these links:\n* [Seminar with Label Studio](https://www.youtube.com/watch?v=HG7imRQN3-k)\n* [User guide](https://baal.readthedocs.io/en/latest/user_guide/index.html)\n* [Bayesian active learning presentation](https://drive.google.com/file/d/13UUDsS1rvqDnXza7L0j4bnqyhOT5TDSt/view?usp=sharing)\n\n\n## Installation and requirements\n\nBaaL requires `Python>=3.6`.\n\nTo install BaaL using pip: `pip install baal`\n\nTo install BaaL from source: `poetry install`\n\nTo use BaaL with [HuggingFace](https://huggingface.co/) Trainers : `pip install baal[nlp]`\n\n## Papers using BaaL\n\n* [Bayesian active learning for production, a systematic study and a reusable library\n](https://arxiv.org/abs/2006.09916) (Atighehchian et al. 2020)\n* [Synbols: Probing Learning Algorithms with Synthetic Datasets\n](https://nips.cc/virtual/2020/public/poster_0169cf885f882efd795951253db5cdfb.html) (Lacoste et al. 2020)\n* [Can Active Learning Preemptively Mitigate Fairness Issues?\n](https://arxiv.org/pdf/2104.06879.pdf) (Branchaud-Charron et al. 2021)\n* [Active learning with MaskAL reduces annotation effort for training Mask R-CNN](https://arxiv.org/abs/2112.06586) (Blok et al. 2021)\n\n\n# What is active learning?\nActive learning is a special case of machine learning in which a learning\nalgorithm is able to interactively query the user (or some other information\nsource) to obtain the desired outputs at new data points\n(to understand the concept in more depth, refer to our [tutorial](https://baal.readthedocs.io/en/latest/)).\n\n## BaaL Framework\n\nAt the moment BaaL supports the following methods to perform active learning.\n\n- Monte-Carlo Dropout (Gal et al. 2015)\n- MCDropConnect (Mobiny et al. 2019)\n- Deep ensembles\n- Semi-supervised learning\n\nIf you want to propose new methods, please submit an issue.\n\n\nThe **Monte-Carlo Dropout** method is a known approximation for Bayesian neural\nnetworks. In this method, the Dropout layer is used both in training and test\ntime. By running the model multiple times whilst randomly dropping weights, we calculate the uncertainty of the prediction using one of the uncertainty measurements in [heuristics.py](baal/active/heuristics/heuristics.py).\n\nThe framework consists of four main parts, as demonstrated in the flowchart below:\n\n- ActiveLearningDataset\n- Heuristics\n- ModelWrapper\n- ActiveLearningLoop\n\n<p align="center">\n  <img src="./docs/literature/images/Baalscheme.svg">\n</p>\n\nTo get started, wrap your dataset in our _[**ActiveLearningDataset**](baal/active/dataset.py)_ class. This will ensure that the dataset is split into\n`training` and `pool` sets. The `pool` set represents the portion of the training set which is yet\nto be labelled.\n\n\nWe provide a lightweight object _[**ModelWrapper**](baal/modelwrapper.py)_ similar to `keras.Model` to make it easier to train and test the model. If your model is not ready for active learning, we provide Modules to prepare them. \n\nFor example, the _[**MCDropoutModule**](baal/bayesian/dropout.py)_ wrapper changes the existing dropout layer\nto be used in both training and inference time and the `ModelWrapper` makes\nthe specifies the number of iterations to run at training and inference.\n\nIn conclusion, your script should be similar to this:\n```python\ndataset = ActiveLearningDataset(your_dataset)\ndataset.label_randomly(INITIAL_POOL)  # label some data\nmodel = MCDropoutModule(your_model)\nmodel = ModelWrapper(model, your_criterion)\nactive_loop = ActiveLearningLoop(dataset,\n                                 get_probabilities=model.predict_on_dataset,\n                                 heuristic=heuristics.BALD(shuffle_prop=0.1),\n                                 query_size=NDATA_TO_LABEL)\nfor al_step in range(N_ALSTEP):\n    model.train_on_dataset(dataset, optimizer, BATCH_SIZE, use_cuda=use_cuda)\n    if not active_loop.step():\n        # We\'re done!\n        break\n```\n\n\nFor a complete experiment, we provide _[experiments/](experiments/)_ to understand how to\nwrite an active training process. Generally, we use the **ActiveLearningLoop**\nprovided at _[src/baal/active/active_loop.py](baal/active/active_loop.py)_.\nThis class provides functionality to get the predictions on the unlabeled pool\nafter each (few) epoch(s) and sort the next set of data items to be labeled\nbased on the calculated uncertainty of the pool.\n\n\n### Re-run our Experiments\n\n```bash\nnvidia-docker build [--target base_baal] -t baal .\nnvidia-docker run --rm baal python3 experiments/vgg_mcdropout_cifar10.py \n```\n\n### Use BaaL for YOUR Experiments\n\nSimply clone the repo, and create your own experiment script similar to the\nexample at [experiments/vgg_experiment.py](experiments/vgg_experiment.py). Make sure to use the four main parts\nof BaaL framework. _Happy running experiments_\n\n### Dev install\n\nSimply build the Dockerfile as below:\n\n```bash\ngit clone git@github.com:ElementAI/baal.git\nnvidia-docker build [--target base_baal] -t baal-dev .\n```\n\nNow you have all the requirements to start contributing to BaaL. _**YEAH!**_\n\n### Contributing!\n\nTo contribute, see [CONTRIBUTING.md](./CONTRIBUTING.md).\n\n\n### Who We Are!\n\n"There is passion, yet peace; serenity, yet emotion; chaos, yet order."\n\nAt ElementAI, the BaaL team tests and implements the most recent papers on uncertainty estimation and active learning.\nThe BaaL team is here to serve you!\n\n- [Parmida Atighehchian](mailto:parmida.atighehchian@servicenow.com)\n- [Frédéric Branchaud-Charron](mailto:frederic.branchaud-charron@servicenow.com)\n- [Jan Freyberg](mailto:jan.freyberg@gmail.com)\n- [Rafael Pardinas](mailto:rafael.pardinas@servicenow.com)\n- [Lorne Schell](mailto:lorne.schell@servicenow.com)\n\n### How to cite\n\nIf you used BaaL in one of your project, we would greatly appreciate if you cite this library using this Bibtex:\n\n```\n@misc{atighehchian2019baal,\n  title={BaaL, a bayesian active learning library},\n  author={Atighehchian, Parmida and Branchaud-Charron, Frederic and Freyberg, Jan and Pardinas, Rafael and Schell, Lorne},\n  year={2019},\n  howpublished={\\url{https://github.com/ElementAI/baal/}},\n}\n```\n\n### Licence\nTo get information on licence of this API please read [LICENCE](./LICENSE)\n',
    'author': 'Parmida Atighehchian',
    'author_email': 'parmida.atighehchian@servicenow.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ElementAI/baal/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
