# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytorch_ie',
 'pytorch_ie.core',
 'pytorch_ie.data',
 'pytorch_ie.data.datamodules',
 'pytorch_ie.data.datasets',
 'pytorch_ie.data.datasets.hf_datasets',
 'pytorch_ie.models',
 'pytorch_ie.models.genre',
 'pytorch_ie.models.modules',
 'pytorch_ie.taskmodules',
 'pytorch_ie.utils']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=2.1.0,<3.0.0',
 'huggingface-hub>=0.5.1,<0.6.0',
 'pytorch-lightning>=1.6.1,<2.0.0',
 'torchmetrics>=0.8.0,<0.9.0',
 'transformers>=4.18.0,<5.0.0']

setup_kwargs = {
    'name': 'pytorch-ie',
    'version': '0.6.1',
    'description': 'State-of-the-art Information Extraction in PyTorch',
    'long_description': 'PyTorch-IE: State-of-the-art Information Extraction in PyTorch\n==============================================================\n\n.. badges-begin\n\n| |Status| |Python Version| |License| |Read the Docs|\n| |Tests| |Codecov| |pre-commit| |Black| |Contributor Covenant|\n\n.. |Status| image:: https://badgen.net/badge/status/alpha/d8624d\n   :target: https://badgen.net/badge/status/alpha/d8624d\n   :alt: Project Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/pytorch-ie\n   :target: https://github.com/christophalt/pytorch-ie\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/github/license/christophalt/pytorch-ie\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/pytorch-ie/latest.svg?label=Read%20the%20Docs\n   :target: https://pytorch-ie.readthedocs.io/\n   :alt: Read the documentation at https://pytorch-ie.readthedocs.io/\n.. |Tests| image:: https://github.com/christophalt/pytorch-ie/workflows/Tests/badge.svg\n   :target: https://github.com/christophalt/pytorch-ie/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/christophalt/pytorch-ie/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/christophalt/pytorch-ie\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n.. |Contributor Covenant| image:: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg\n   :target: https://github.com/christophalt/pytorch-ie/blob/main/CODE_OF_CONDUCT.rst\n   :alt: Contributor Covenant\n\n.. badges-end\n\n-----\n\n🚀️ Quickstart\n---------------\n\n.. code:: console\n\n    $ pip install pytorch-ie\n\n\n⚡️ Examples\n------------\n**Note:** Setting ``num_workers=0`` in the pipeline is only necessary when running an example in an\ninteractive python session. The reason is that multiprocessing doesn\'t play well with the interactive python\ninterpreter, see `here <https://docs.python.org/3/library/multiprocessing.html#using-a-pool-of-workers>`_\nfor details.\n\nSpan-classification-based Named Entity Recognition\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n.. code:: python\n\n    from dataclasses import dataclass\n\n    from pytorch_ie.annotations import LabeledSpan\n    from pytorch_ie.auto import AutoPipeline\n    from pytorch_ie.core import AnnotationList, annotation_field\n    from pytorch_ie.documents import TextDocument\n\n    @dataclass\n    class ExampleDocument(TextDocument):\n        entities: AnnotationList[LabeledSpan] = annotation_field(target="text")\n\n    document = ExampleDocument(\n        "“Making a super tasty alt-chicken wing is only half of it,” said Po Bronson, general partner at SOSV and managing director of IndieBio."\n    )\n\n    # see below for the long version\n    ner_pipeline = AutoPipeline.from_pretrained("pie/example-ner-spanclf-conll03", device=-1, num_workers=0)\n\n    ner_pipeline(document, predict_field="entities")\n\n    for entity in document.entities.predictions:\n        print(f"{entity} -> {entity.label}")\n\n    # Result:\n    # IndieBio -> ORG\n    # Po Bronson -> PER\n    # SOSV -> ORG\n\nTo create the same pipeline as above without `AutoPipeline`:\n\n.. code:: python\n\n    from pytorch_ie.auto import AutoTaskModule, AutoModel\n    from pytorch_ie.pipeline import Pipeline\n\n    model_name_or_path = "pie/example-ner-spanclf-conll03"\n    ner_taskmodule = AutoTaskModule.from_pretrained(model_name_or_path)\n    ner_model = AutoModel.from_pretrained(model_name_or_path)\n    ner_pipeline = Pipeline(model=ner_model, taskmodule=ner_taskmodule, device=-1, num_workers=0)\n\nOr, without `Auto` classes at all:\n\n.. code:: python\n\n    from pytorch_ie.pipeline import Pipeline\n    from pytorch_ie.models import TransformerSpanClassificationModel\n    from pytorch_ie.taskmodules import TransformerSpanClassificationTaskModule\n\n    model_name_or_path = "pie/example-ner-spanclf-conll03"\n    ner_taskmodule = TransformerSpanClassificationTaskModule.from_pretrained(model_name_or_path)\n    ner_model = TransformerSpanClassificationModel.from_pretrained(model_name_or_path)\n    ner_pipeline = Pipeline(model=ner_model, taskmodule=ner_taskmodule, device=-1, num_workers=0)\n\n\nText-classification-based Relation Extraction\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n.. code:: python\n\n    from dataclasses import dataclass\n\n    from pytorch_ie.annotations import BinaryRelation, LabeledSpan\n    from pytorch_ie.auto import AutoPipeline\n    from pytorch_ie.core import AnnotationList, annotation_field\n    from pytorch_ie.documents import TextDocument\n\n\n    @dataclass\n    class ExampleDocument(TextDocument):\n        entities: AnnotationList[LabeledSpan] = annotation_field(target="text")\n        relations: AnnotationList[BinaryRelation] = annotation_field(target="entities")\n\n    document = ExampleDocument(\n        "“Making a super tasty alt-chicken wing is only half of it,” said Po Bronson, general partner at SOSV and managing director of IndieBio."\n    )\n\n    re_pipeline = AutoPipeline.from_pretrained("pie/example-re-textclf-tacred", device=-1, num_workers=0)\n\n    for start, end, label in [(65, 75, "PER"), (96, 100, "ORG"), (126, 134, "ORG")]:\n        document.entities.append(LabeledSpan(start=start, end=end, label=label))\n\n    re_pipeline(document, predict_field="relations", batch_size=2)\n\n    for relation in document.relations.predictions:\n        print(f"({relation.head} -> {relation.tail}) -> {relation.label}")\n\n    # Result:\n    # (Po Bronson -> SOSV) -> per:employee_of\n    # (Po Bronson -> IndieBio) -> per:employee_of\n    # (SOSV -> Po Bronson) -> org:top_members/employees\n    # (IndieBio -> Po Bronson) -> org:top_members/employees\n\n..\n  github-only\n\n✨📚✨ `Read the full documentation`__\n\n__ https://pytorch-ie.readthedocs.io/\n\nDevelopment Setup\n-----------------\n\n🏅 Acknowledgements\n---------------------\n\n- This package is based on the `sourcery-ai/python-best-practices-cookiecutter`_ and `cjolowicz/cookiecutter-hypermodern-python`_ project templates.\n\n.. _sourcery-ai/python-best-practices-cookiecutter: https://github.com/sourcery-ai/python-best-practices-cookiecutter\n.. _cjolowicz/cookiecutter-hypermodern-python: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n\n\n📃 Citation\n-------------\n\nIf you want to cite the framework feel free to use this:\n\n.. code:: bibtex\n\n    @misc{alt2022pytorchie,\n    author={Christoph Alt, Arne Binder},\n    title = {PyTorch-IE: State-of-the-art Information Extraction in PyTorch},\n    year = {2022},\n    publisher = {GitHub},\n    journal = {GitHub repository},\n    howpublished = {\\url{https://github.com/ChristophAlt/pytorch-ie}}\n    }\n',
    'author': 'Christoph Alt',
    'author_email': 'christoph.alt@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/christophalt/pytorch-ie',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
