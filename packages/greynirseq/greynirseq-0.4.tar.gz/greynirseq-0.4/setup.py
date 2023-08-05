# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['greynirseq',
 'greynirseq.cli',
 'greynirseq.ner',
 'greynirseq.nicenlp',
 'greynirseq.nicenlp.criterions',
 'greynirseq.nicenlp.data',
 'greynirseq.nicenlp.examples.constituency_parsing',
 'greynirseq.nicenlp.examples.ner',
 'greynirseq.nicenlp.models',
 'greynirseq.nicenlp.tasks',
 'greynirseq.nicenlp.utils',
 'greynirseq.nicenlp.utils.constituency',
 'greynirseq.nicenlp.utils.label_schema',
 'greynirseq.serve',
 'greynirseq.utils',
 'greynirseq.utils.bpe',
 'greynirseq.utils.preprocessing',
 'greynirseq.utils.qa',
 'greynirseq.utils.tests']

package_data = \
{'': ['*'],
 'greynirseq.ner': ['testdata/*'],
 'greynirseq.nicenlp': ['examples/pos/*', 'examples/translation/*']}

install_requires = \
['editdistance>=0.6.0,<0.7.0',
 'fairseq>=0.10.0,<0.11.0',
 'langid>=1.1.6,<2.0.0',
 'nltk>=3.5,<4.0',
 'pyjarowinkler>=1.8,<2.0',
 'reynir>=3.5.0,<4.0.0',
 'scipy>=1.5,<2.0',
 'sentencepiece>=0.1.96,<0.2.0',
 'spacy>=2,<3',
 'transformers>=4.3.2,<5.0.0']

entry_points = \
{'console_scripts': ['greynirseq = greynirseq.cli.greynirseq_main:main']}

setup_kwargs = {
    'name': 'greynirseq',
    'version': '0.4',
    'description': 'Natural language processing for Icelandic',
    'long_description': '[![superlinter](https://github.com/mideind/greynirseq/actions/workflows/superlinter.yml/badge.svg)]() [![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)\n\n---\n\n<img src="assets/greynir-logo-large.png" alt="Greynir" width="200" height="200" align="right" style="margin-left:20px; margin-bottom: 20px;">\n\n# GreynirSeq\n\nGreynirSeq is a natural language parsing toolkit for Icelandic focused on sequence modeling with neural networks. It is under active development and is in its early stages.\n\nThe modeling part (nicenlp) of GreynirSeq is built on top of the excellent [fairseq](https://github.com/pytorch/fairseq) from Facebook (which is built on top of pytorch).\n\nGreynirSeq is licensed under the GNU AFFERO GPLv3 license unless otherwise stated at the top of a file.\n\n**What\'s new?**\n* An Icelandic RoBERTa model, **IceBERT** finetuned for NER and POS tagging.\n* Icelandic - English translation.\n\n**What\'s on the horizon?**\n* More fine tuning tasks for Icelandic, constituency parsing and grammatical error detection\n\n---\n\nBe aware that usage of the CLI or otherwise downloading model files will result in downloading of **gigabytes** of data.\nSimply installing `greynirseq` will not download any models, they are automatically downloaded on-demand.\n\n## Installation\nIn a suitable virtual environment\n``` bash\n# From PyPI\n$ pip install greynirseq\n# or from git main branch\n$ pip install git+https://github.com/mideind/greynirseq@main\n```\n\n## Features\n\n### TL;DR give me the CLI\n\nThe `greynirseq` CLI interface can be used to run pretrained models for various tasks. Run `pip install greynirseq && greynirseq -h` to see what options are available.\n\n#### POS\nInput is accepted from file containing a single [tokenized](https://github.com/mideind/Tokenizer) sentence per line, or from stdin.\n\n``` bash\n$ echo "Systurnar Guðrún og Monique átu einar um jólin á McDonalds ." | greynirseq pos --input -\n\nnvfng nven-s c n---s sfg3fþ lvfnsf af nhfog af n----s pl\n```\n\n#### NER\nInput is accepted from file containing a single [tokenized](https://github.com/mideind/Tokenizer) sentence per line, or from stdin.\n\n``` bash\n$ echo "Systurnar Guðrún og Monique átu einar um jólin á McDonalds ." | greynirseq ner --input -\n\nO B-Person O B-Person O O O O O B-Organization O\n```\n\n#### Translation\nInput is accepted from file containing a single **untokenized** sentence per line, or from stdin.\n\n``` bash\n# For en->is translation\n$ echo "This is an awesome test that shows how to use a pretrained translation model." | greynirseq translate --source-lang en --target-lang is\n\nÞetta er æðislegt próf sem sýnir hvernig nota má forprófað þýðingarlíkan.\n\n# For is->en translation\n$ echo "Þetta er æðislegt próf sem sýnir hvernig nota má forprófað þýðingarlíkan." | greynirseq translate --source-lang is --target-lang en\n\nThis is an awesome test that shows how a pre-tested translation model can be used.\n```\n\n### Neural Icelandic Language Processing - NIceNLP\n\nIceBERT is an Icelandic BERT-based (RoBERTa) language model that is suitable for fine tuning on downstream tasks.\n\nThe following fine tuning tasks are available both through the `greynirseq` CLI and for loading programmatically.\n\n1. [POS tagging](https://github.com/mideind/GreynirSeq/blob/main/src/greynirseq/nicenlp/examples/pos/README.md)\n1. [NER tagging](https://github.com/mideind/GreynirSeq/blob/main/src/greynirseq/nicenlp/examples/ner/README.md)\n\nThere are also a some translation models available. They are Transformer models trained from scratch or finetuned based on mBART25.\n\n1. [Translation](https://github.com/mideind/GreynirSeq/blob/main/src/greynirseq/nicenlp/examples/translation/README.md)\n\n## Development\nTo install GreynirSeq in development mode we recommend using poetry as shown below\n\n```bash\npip install poetry && poetry install\n```\n\n### Linting\n\nAll code is checked with [Super-Linter](https://github.com/github/super-linter) in a *GitHub Action*, we recommend running it locally before pushing\n\n```bash\n./run_linter.sh\n```\n\n### Type annotation\n\nType annotation will soon be checked with mypy and should be included.\n\n',
    'author': 'Miðeind ehf',
    'author_email': 'tauganet@mideind.is',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mideind/GreynirSeq',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
