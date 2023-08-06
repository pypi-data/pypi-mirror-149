# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plotly_resampler',
 'plotly_resampler.aggregation',
 'plotly_resampler.figure_resampler']

package_data = \
{'': ['*']}

install_requires = \
['dash>=2.2.0,<3.0.0',
 'jupyter-dash>=0.4.2',
 'lttbc==0.2.0',
 'orjson>=3.6.8,<4.0.0',
 'pandas>=1.3.5,<2.0.0',
 'plotly>=5.6.0,<6.0.0',
 'trace-updater>=0.0.8']

setup_kwargs = {
    'name': 'plotly-resampler',
    'version': '0.6.0',
    'description': 'Visualizing large time series with plotly',
    'long_description': '<p align="center">\n    <a href="#readme">\n        <img alt="Plotly-Resampler logo" src="https://raw.githubusercontent.com/predict-idlab/plotly-resampler/main/docs/sphinx/_static/logo.svg" width=65%>\n    </a>\n</p>\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/plotly-resampler.svg)](https://pypi.org/project/plotly-resampler/)\n[![support-version](https://img.shields.io/pypi/pyversions/plotly-resampler)](https://img.shields.io/pypi/pyversions/plotly-resampler)\n[![codecov](https://img.shields.io/codecov/c/github/predict-idlab/plotly-resampler?logo=codecov)](https://codecov.io/gh/predict-idlab/plotly-resampler)\n[![Code quality](https://img.shields.io/lgtm/grade/python/github/predict-idlab/plotly-resampler?label=code%20quality&logo=lgtm)](https://lgtm.com/projects/g/predict-idlab/plotly-resampler/context:python)\n[![Downloads](https://pepy.tech/badge/plotly-resampler)](https://pepy.tech/project/plotly-resampler)\n[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?)](http://makeapullrequest.com)\n[![Documentation](https://github.com/predict-idlab/plotly-resampler/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/predict-idlab/plotly-resampler/actions/workflows/deploy-docs.yml)\n[![Testing](https://github.com/predict-idlab/plotly-resampler/actions/workflows/test.yml/badge.svg)](https://github.com/predict-idlab/plotly-resampler/actions/workflows/test.yml)\n\n\n<!-- [![Downloads](https://pepy.tech/badge/plotly-resampler)](https://pepy.tech/project/plotly-resampler) -->\n\n> `plotly_resampler`: visualize large sequential data by **adding resampling functionality to Plotly figures**\n\n[Plotly](https://github.com/plotly/plotly.py) is an awesome interactive visualization library, however it can get pretty slow when a lot of data points are visualized (100 000+ datapoints). This library solves this by downsampling (aggregating) the data respective to the view and then plotting the aggregated points. When you interact with the plot (panning, zooming, ...), callbacks are used to aggregate data and update the figure. \n\n<p align="center">\n    <a href="#readme">\n        <img alt="example demo" src="https://github.com/predict-idlab/plotly-resampler/blob/main/docs/sphinx/_static/basic_example.gif" width=95%>\n    </a>\n</p>\n\nIn [this Plotly-Resampler demo](https://github.com/predict-idlab/plotly-resampler/blob/main/examples/basic_example.ipynb) over `110,000,000` data points are visualized! \n\n<!-- These dynamic aggregation callbacks are realized with: -->\n<!-- * [Dash](https://github.com/plotly/dash) when a `go.Figure` object is wrapped with dynamic aggregation functionality, see example ⬆️. -->\n<!-- * The [FigureWidget.layout.on_change](https://plotly.com/python-api-reference/generated/plotly.html?highlight=on_change#plotly.basedatatypes.BasePlotlyType.on_change) method, when a `go.FigureWidget` is used within a `.ipynb` environment. -->\n\n<!-- #### Useful links -->\n\n<!-- - [Documentation]() work in progress 🚧  -->\n<!-- - [Example notebooks](https://github.com/predict-idlab/plotly-resampler/tree/main/examples/) -->\n\n### Installation\n\n| [**pip**](https://pypi.org/project/plotly_resampler/) | `pip install plotly-resampler` | \n| ---| ----|\n<!-- | [**conda**](https://anaconda.org/conda-forge/plotly_resampler/) | `conda install -c conda-forge plotly_resampler` | -->\n\n\n## Usage\n\nTo **add dynamic resampling** to your plotly Figure\n* using a web application with *Dash* callbacks, you should;\n  1. wrap the plotly Figure with `FigureResampler`\n  2. call `.show_dash()` on the Figure\n* within a *jupyter* environment and *without creating a web application*, you should:\n  1. wrap the plotly Figure with `FigureWidgetResampler`\n  2. output the `FigureWidgetResampler` instance in a cell\n\n> **Note**:  \n> Any plotly Figure can be wrapped with `FigureResampler` and `FigureWidgetResampler`! 🎉  \n> But, (obviously) only the scatter traces will be resampled.\n\n> **Tip** 💡:  \n> For significant faster initial loading of the Figure, we advise to wrap the constructor of the plotly Figure and add the trace data as `hf_x` and `hf_y`\n\n### Minimal example\n\n```python\nimport plotly.graph_objects as go; import numpy as np\nfrom plotly_resampler import FigureResampler, FigureWidgetResampler\n\nx = np.arange(1_000_000)\nnoisy_sin = (3 + np.sin(x / 200) + np.random.randn(len(x)) / 10) * x / 1_000\n\n# OPTION 1 - FigureResampler: dynamic aggregation via a Dash web-app\nfig = FigureResampler(go.Figure())\nfig.add_trace(go.Scattergl(name=\'noisy sine\', showlegend=True), hf_x=x, hf_y=noisy_sin)\n\nfig.show_dash(mode=\'inline\')\n```\n\n#### FigureWidgetResampler: dynamic aggregation via `FigureWidget.layout.on_change`\n```python\n... \n# OPTION 2 - FigureWidgetResampler: dynamic aggregation via `FigureWidget.layout.on_change`\nfig = FigureWidgetResampler(go.Figure())\nfig.add_trace(go.Scattergl(name=\'noisy sine\', showlegend=True), hf_x=x, hf_y=noisy_sin)\n\nfig\n```\n\n### Features\n\n* **Convenient** to use:\n  * just add either\n    * `FigureResampler` decorator around a plotly Figure and call `.show_dash()`\n    * `FigureWidgetResampler` decorator around a plotly Figure and output the instance in a cell\n  * allows all other plotly figure construction flexibility to be used!\n* **Environment-independent** \n  * can be used in Jupyter, vscode-notebooks, Pycharm-notebooks, Google Colab, and even as application (on a server)\n* Interface for **various aggregation algorithms**:\n  * ability to develop or select your preferred sequence aggregation method\n\n\n### Important considerations & tips\n\n* When running the code on a server, you should forward the port of the `FigureResampler.show_dash()` method to your local machine.<br>\n  **Note** that you can add dynamic aggregation to plotly figures with the `FigureWidgetResampler` wrapper without needing to forward a port!\n* In general, when using downsampling one should be aware of (possible) [aliasing](https://en.wikipedia.org/wiki/Aliasing) effects.  \n  The <b><a style="color:orange">[R]</a></b> in the legend indicates when the corresponding trace is being resampled (and thus possibly distorted) or not. Additionally, the `~<range>` suffix represent the mean aggregation bin size in terms of the sequence index.\n\n## Future work 🔨\n\n* Support `.add_traces()` (currently only `.add_trace` is supported)\n\n<br>\n\n---\n\n<p align="center">\n👤 <i>Jonas Van Der Donckt, Jeroen Van Der Donckt, Emiel Deprost</i>\n</p>\n',
    'author': 'Jonas Van Der Donckt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/predict-idlab/plotly-resampler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
