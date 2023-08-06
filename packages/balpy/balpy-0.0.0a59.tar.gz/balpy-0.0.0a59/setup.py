# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['balpy',
 'balpy.balancerv2cad.scripts',
 'balpy.balancerv2cad.src.balancerv2cad',
 'balpy.balancerv2cad.src.balancerv2cad.logger',
 'balpy.balancerv2cad.tests',
 'balpy.balancerv2cad.tests.unit-test',
 'balpy.enums',
 'balpy.graph']

package_data = \
{'': ['*'],
 'balpy': ['abi/*',
           'balancerv2cad/*',
           'balancerv2cad/notebooks/*',
           'deployments/20210418-authorizer/abi/*',
           'deployments/20210418-authorizer/output/*',
           'deployments/20210418-vault/abi/*',
           'deployments/20210418-vault/output/*',
           'deployments/20210418-weighted-pool/abi/*',
           'deployments/20210418-weighted-pool/output/*',
           'deployments/20210624-stable-pool/abi/*',
           'deployments/20210624-stable-pool/output/*',
           'deployments/20210624-stable-pool/test/*',
           'deployments/20210721-liquidity-bootstrapping-pool/abi/*',
           'deployments/20210721-liquidity-bootstrapping-pool/output/*',
           'deployments/20210721-liquidity-bootstrapping-pool/test/*',
           'deployments/20210727-meta-stable-pool/abi/*',
           'deployments/20210727-meta-stable-pool/output/*',
           'deployments/20210727-meta-stable-pool/test/*',
           'deployments/20210811-ldo-merkle/abi/*',
           'deployments/20210811-ldo-merkle/output/*',
           'deployments/20210811-ldo-merkle/test/*',
           'deployments/20210812-lido-relayer/abi/*',
           'deployments/20210812-lido-relayer/output/*',
           'deployments/20210812-lido-relayer/test/*',
           'deployments/20210812-wsteth-rate-provider/abi/*',
           'deployments/20210812-wsteth-rate-provider/output/*',
           'deployments/20210812-wsteth-rate-provider/test/*',
           'deployments/20210907-investment-pool/abi/*',
           'deployments/20210907-investment-pool/output/*',
           'deployments/20210907-investment-pool/test/*',
           'deployments/20211202-no-protocol-fee-lbp/abi/*',
           'deployments/20211202-no-protocol-fee-lbp/output/*',
           'deployments/20211208-aave-linear-pool/abi/*',
           'deployments/20211208-aave-linear-pool/bytecode/*',
           'deployments/20211208-aave-linear-pool/output/*',
           'deployments/20211208-stable-phantom-pool/abi/*',
           'deployments/20211208-stable-phantom-pool/bytecode/*',
           'deployments/20211208-stable-phantom-pool/output/*',
           'deployments/20220304-erc4626-linear-pool/abi/*',
           'deployments/20220304-erc4626-linear-pool/output/*']}

install_requires = \
['Cython==0.29.24',
 'cytoolz==0.11.2',
 'eth-abi==2.1.1',
 'gql==2.0.0',
 'jstyleson==0.0.2',
 'multicaller==0.0.0a9',
 'requests==2.25.1',
 'web3==5.19.0']

setup_kwargs = {
    'name': 'balpy',
    'version': '0.0.0a59',
    'description': 'Balancer V2 Python API',
    'long_description': None,
    'author': 'Langer',
    'author_email': 'langer@balancer.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
