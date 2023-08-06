### py-shardeum-explorer

A minimal, complete, python API for Shardeum Explorer.

#### Usage

Install the package from [PyPi](https://pypi.org/project/py-shardeum-explorer/)

```bash
pip install py-shardeum-explorer
```

To use it in your code, import the py-shardeum-explorer module:

```python
from shardeumexplorer import ShardeumExplorer

shmexp = ShardeumExplorer("Liberty") // currently it supports the only alphanet
```

- To View Balance of a Specific Address.
It returns the value (in SHM)
```python
shmexp.get_account_balance("0x822429119D53055fB11E69213613851ba28bd888")
```

- To View Balance of a Multiple Address.
It returns a dictionary where the key is an address and its corresponding value is its balance.
```python
shmexp.get_account_balance_multiple(["0x822429119D53055fB11E69213613851ba28bd888","0x73155b7350C500Abd7235d42695F01ff4307a4fa"])
```
- To View Total Accounts Existing in the Network.
```python
shmexp.total_accounts()
```

**Note**: _This package is still nascent and might be broken with continuous updates on the network_. More functionalities will be added to the package soon. Work In Progress. 🚧

#### Found Issues/Bugs?
Report Issues [here](https://github.com/iSumitBanik/py-shardeum-explorer/issues)

