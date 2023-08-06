# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipyannotator',
 'ipyannotator.custom_input',
 'ipyannotator.custom_widgets',
 'ipyannotator.datasets',
 'ipyannotator.docs',
 'ipyannotator.ipytyping',
 'ipyannotator.services']

package_data = \
{'': ['*']}

install_requires = \
['PyPubSub>=4.0.3,<5.0.0',
 'ipycanvas>=0.10.2,<0.11.0',
 'ipyevents>=0.8.0,<0.9.0',
 'ipykernel>=5.3.4,<6.0.0',
 'ipython>=8.0.1,<9.0.0',
 'ipywidgets>=7.5.1,<8.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'nbdev==1.2.7',
 'pandas>=1.1.2,<2.0.0',
 'pooch>=1.5.2,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'scikit-image>=0.18.3,<0.19.0',
 'tqdm>=4.64.0,<5.0.0',
 'traitlets>=5.1.1,<6.0.0',
 'voila>=0.3.1,<0.4.0']

setup_kwargs = {
    'name': 'ipyannotator',
    'version': '0.8.3',
    'description': 'The infinitely hackable annotation framework',
    'long_description': '# Ipyannotator - the infinitely hackable annotation framework\n\n![CI-Badge](https://github.com/palaimon/ipyannotator/workflows/CI/badge.svg)\n\nIpyannotator is a flexible annotation system. The library contains some pre-defined annotators that can be used out of the box, but it also can be extend and customized according to the users needs.\n\nWe hope this repository helps you to explore how annotation UI\'s can be quickly built using only python code and leveraging many awesome libraries ([ipywidgets](https://github.com/jupyter-widgets/ipywidgets), [voila](https://github.com/voila-dashboards/voila), [ipycanvas](https://github.com/martinRenou/ipycanvas), etc.) from the [jupyter Eco-system](https://jupyter.org/).\n\nAt https://palaimon.io we have used the concepts underlying Ipyannotator internally for various projects and this is our attempt to contribute back to the OSS community some of the benefits we have had using OOS software.\n\n## Please star, fork and open issues!\n\nPlease let us know if you find this repository useful. Your feedback will help us to turn this proof of concept into a comprehensive library.\n\n## Install\n\n`pip install ipyannotator`\n\n**dependencies (should be handled by pip)**\n\n```\npython = "^3.7"\ntraitlets = \'=4.3.3\'\nipycanvas = "^0.5.1"\nipyevents = "^0.8.0"\nipywidgets = "^7.5.1"\n```\n\n## Run ipyannotator as stand-alone web app using voila\n\nUsing `poetry`:\n\ninstall:\n```shell\ncd {project_root}\npoetry install --no-dev\npoetry run pip install voila\n```\nand run simple ipyannotator standalone example:\n```shell \npoetry run voila nbs/09_voila_example.ipynb --enable_nbextensions=True\n```\n  \nSame with `pip`:\n\n```shell\n   cd {project_root}\n   \n   pip install . \n   pip install voila\n   \n   voila nbs/09_voila_example.ipynb --enable_nbextensions=True\n```\n\n## Documentation\n\nThis library has been written in the [literate programming style](https://en.wikipedia.org/wiki/Literate_programming) popularized for\njupyter notebooks by [nbdev](https://www.fast.ai/2019/12/02/nbdev/). Please explore the jupyter notebooks in `nbs/` to learn more about\nthe inner working of ipyannotator.\n\nThe notebooks contains the development dependencies: \n[pytest](https://docs.pytest.org/en/7.1.x/) and [ipytest](https://github.com/chmp/ipytest), \nif you want to run the notebooks remove the tests or install the libraries mentioned.\n\nAlso check out the following notebook for a more high level overview.\n\n- Tutorial demonstrating how ipyannotator can be seamlessly integrated in your data science workflow. `nbs/08_tutorial_road_damage.ipynb`\n- [Recoding of jupytercon 2020](https://www.youtube.com/watch?v=jFAp1s1O8Hg) talk explaining the high level concepts / vision of ipyannotator.\n\n## Jupyter lab trouble shooting\n\nFor clean (re)install make sure to have all the lab extencions active:\n\n`jupyter lab clean` to remove the staging and static directories from the lab \n\n _ipywidgets_:\n \n `jupyter labextension install @jupyter-widgets/jupyterlab-manager`\n \n _ipycanvas_:\n \n `jupyter labextension install @jupyter-widgets/jupyterlab-manager ipycanvas`\n \n _ipyevents_:\n \n `jupyter labextension install @jupyter-widgets/jupyterlab-manager ipyevents`\n \n _nbdime_:\n \n `nbdime extensions --enable [--sys-prefix/--user/--system]`\n \n _viola_:\n \n `jupyter labextension install @jupyter-voila/jupyterlab-preview`\n\n## How to contribute\n\nCheck out `CONTRIBUTING.md` and since ipyannotator is build using nbdev reading\nthe [nbdev tutorial](https://nbdev.fast.ai/tutorial.html) and related docs will be very helpful.\n\n## Additional resources\n\n![jupytercon 2020](https://jupytercon.com/_nuxt/img/5035c8d.svg)\n\n- [jupytercon 2020 talk](https://cfp.jupytercon.com/2020/schedule/presentation/237/ipyannotator-the-infinitely-hackable-annotation-framework/).\n\n##Acknowledgements\n\nThe authors acknowledge the financial support by the Federal Ministry for Digital and Transport of Germany under the program mFUND (project number 19F2160A).\n\n## Copyright\n\nCopyright 2020 onwards, Palaimon GmbH. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this project\'s files except in compliance with the License. A copy of the License is provided in the LICENSE file in this repository.\n\n\n\n<!-- Matomo Image Tracker-->\n<img referrerpolicy="no-referrer-when-downgrade" src="https://matomo.palaimon.io/matomo.php?idsite=4&amp;rec=1" style="border:0" alt="" />\n<!-- End Matomo -->\n',
    'author': 'palaimon.io',
    'author_email': 'oss@mail.palaimon.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/palaimon/ipyannotator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
