# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfn_lsp_extra',
 'cfn_lsp_extra.decode',
 'cfn_lsp_extra.resources',
 'cfn_lsp_extra.scrape']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aiohttp[speedups]>=3.8,<4.0',
 'cfn-lint>=0.59,<0.60',
 'click>=8.0.1',
 'platformdirs==2.5',
 'pydantic==1.8',
 'pygls>=0.11,<0.12',
 'tqdm==4.64',
 'types-PyYAML>=6.0,<7.0']

entry_points = \
{'console_scripts': ['cfn-lsp-extra = cfn_lsp_extra.__main__:main']}

setup_kwargs = {
    'name': 'cfn-lsp-extra',
    'version': '0.1.1',
    'description': 'Cfn Lsp Extra',
    'long_description': '# Cfn Lsp Extra\n\n<!-- [![Python Version](https://img.shields.io/pypi/pyversions/cfn-lsp-extra)][python version] -->\n\nAn experimental cloudformation lsp server built on top of [cfn-lint](https://github.com/aws-cloudformation/cfn-lint) aiming to provide hovering, completion, etc.\n\nhttps://user-images.githubusercontent.com/17688577/166110762-71058f8f-4cb6-44ae-960b-9370a166125a.mp4\n\n## Usage\n\n```bash\npipx install git+https://github.com/LaurenceWarne/cfn-lsp-extra\n```\n\n### Emacs\n\nYou need to install an lsp client like [lsp-mode](https://github.com/emacs-lsp/lsp-mode) and register `cfn-lsp-extra`.  [yaml-mode](https://github.com/yoshiki/yaml-mode) is also highly recommended.\n\n```elisp\n;; After lsp-mode and yaml-mode have been loaded\n(when-let ((exe (executable-find "cfn-lsp-extra")))\n\n  ;; Copied from https://www.emacswiki.org/emacs/CfnLint\n  (define-derived-mode cfn-json-mode js-mode\n    "CFN-JSON"\n    "Simple mode to edit CloudFormation template in JSON format."\n  (setq js-indent-level 2))\n\n  (add-to-list \'magic-mode-alist\n               \'("\\\\({\\n *\\\\)? *[\\"\']AWSTemplateFormatVersion" . cfn-json-mode))\n  (add-to-list \'lsp-language-id-configuration\n               \'(cfn-json-mode . "cloudformation"))\n  (add-hook \'cfn-json-mode-hook #\'lsp)\n  \n  (when (featurep \'yaml-mode)\n    \n    (define-derived-mode cfn-yaml-mode yaml-mode\n      "CFN-YAML"\n      "Simple mode to edit CloudFormation template in YAML format.")\n    (add-to-list \'magic-mode-alist\n                 \'("\\\\(---\\n\\\\)?AWSTemplateFormatVersion:" . cfn-yaml-mode))\n    (add-to-list \'lsp-language-id-configuration\n                 \'(cfn-yaml-mode . "cloudformation"))\n    (add-hook \'cfn-yaml-mode-hook #\'lsp))\n  \n  (lsp-register-client\n   (make-lsp-client :new-connection (lsp-stdio-connection exe)\n                    :activation-fn (lsp-activate-on "cloudformation")\n                    :server-id \'cfn-lsp-extra)))\n```\n\n## Alternatives\n\n### [vscode-cfn-lint](https://github.com/aws-cloudformation/cfn-lint-visual-studio-code)\n\n### [cfn-lint](https://github.com/aws-cloudformation/cfn-lint)\n\nNote this is used by `cfn-lsp-extra` under the hood.\n\n',
    'author': 'Laurence Warne',
    'author_email': 'laurencewarne@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/laurencewarne/cfn-lsp-extra',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
