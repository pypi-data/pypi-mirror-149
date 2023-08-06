# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kogito',
 'kogito.core',
 'kogito.core.processors',
 'kogito.core.processors.models',
 'kogito.models',
 'kogito.models.bart',
 'kogito.models.gpt2',
 'kogito.models.gpt3']

package_data = \
{'': ['*'], 'kogito.core.processors': ['data/*']}

install_requires = \
['git-python==1.0.3',
 'inflect>=5.3.0,<6.0.0',
 'openai',
 'pandas>=1.3.5,<2.0.0',
 'pytorch-lightning>=1.5.10,<2.0.0',
 'rouge-score>=0.0.4,<0.0.5',
 'sacrebleu>=2.0.0,<3.0.0',
 'spacy>=3.2.3,<4.0.0',
 'torch>=1.10.1,<2.0.0',
 'transformers>=4.15.0,<5.0.0',
 'wandb>=0.12.9,<0.13.0']

setup_kwargs = {
    'name': 'kogito',
    'version': '0.2.3',
    'description': 'A Python NLP Commonsense Reasoning library',
    'long_description': '# <span style="background-color:#dce755">k</span>ogito\nA Python NLP Commonsense Reasoning library\n\n## Installation\n\n### Installation with pip\n**kogito** can be installed using pip.\n\n```sh\npip install kogito\n```\n\nIt requires a minimum ``python`` version of ``3.8``.\n\n## Setup\n**kogito** uses [spacy](https://spacy.io) under the hood for various text processing purposes, so, a [spacy](https://spacy.io) language package has to be installed before running the inference module.\n\n```sh\npython -m spacy download en_core_web_sm\n``` \nBy default, ``CommonsenseInference`` module uses ``en_core_web_sm`` to initialize ``spacy`` pipeline, but a different language pipeline can be specified as well.\n\n## Quickstart\n**kogito** provides an easy interface to interact with commonsense reasoning models such as [COMET](https://arxiv.org/abs/2010.05953) to generate inferences from a text input.\nHere is a sample usage of the library where you can initialize an inference module, a custom commonsense reasoning model, and generate a knowledge graph from text on the fly.\n\n```python\nfrom kogito.models.bart.comet import COMETBART\nfrom kogito.inference import CommonsenseInference\n\n# Load pre-trained model from HuggingFace\nmodel = COMETBART.from_pretrained("mismayil/comet-bart-ai2")\n\n# Initialize inference module with a spacy language pipeline\ncsi = CommonsenseInference(language="en_core_web_sm")\n\n# Run inference\ntext = "PersonX becomes a great basketball player"\nkgraph = csi.infer(text, model)\n\n# Save output knowledge graph to JSON file\nkgraph.to_jsonl("kgraph.json")\n```\n\nHere is an excerpt from the result of the above code sample:\n\n```json\n{"head": "PersonX becomes a great basketball player", "relation": "Causes", "tails": [" PersonX practices every day.", " PersonX plays basketball every day", " PersonX practices every day"]}\n{"head": "basketball", "relation": "ObjectUse", "tails": [" play with friends", " play basketball with", " play basketball"]}\n{"head": "player", "relation": "CapableOf", "tails": [" play game", " win game", " play football"]}\n{"head": "great basketball player", "relation": "HasProperty", "tails": [" good at basketball", " good at sports", " very good"]}\n{"head": "become player", "relation": "isAfter", "tails": [" play game", " become coach", " play with"]}\n```\nThis is just one way to generate commonsense inferences and **kogito** offers much more. For complete documentation, check out the [kogito docs](https://kogito.readthedocs.io).\n\n## Development\n\n### Setup\n**kogito** uses [Poetry](https://python-poetry.org/) to manage its dependencies. \n\nInstall poetry from the official repository first:\n```sh\ncurl -sSL https://install.python-poetry.org | python3 -\n```\n\nThen run the following command to install package dependencies:\n```sh\npoetry install\n```\n',
    'author': 'Mete Ismayil',
    'author_email': 'mahammad.ismayilzada@epfl.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mismayil/kogito',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
