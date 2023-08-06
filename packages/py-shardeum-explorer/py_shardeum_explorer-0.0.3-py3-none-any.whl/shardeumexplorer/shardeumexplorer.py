import requests

class ShardeumExplorer:
  def __init__(self,network):
    """ __init__ method for the class ShardeumExplorer.

    Args:
        network (string): The name of the network. 
    """
    self.decimal_places = 18
    if(network.lower() == "liberty"):
      self.block_explorer_url = "http://explorer.liberty10.shardeum.org"
  
  def get_account_balance(self,address):
    """ This function returns the balance for a specific account (in SHM).

    Args:
        address (string): The address of the account.

    Returns:
        balance_in_decimal (float): The balance (in decimal format) for the input address.
    """
    get_account_balance_endpoint = f"/api/account?address={address.lower()}"
    URL = self.block_explorer_url + get_account_balance_endpoint
    response = requests.get(URL)
    balance_in_hex = response.json()['accounts'][0]['account']['balance']
    balance_in_decimal = int(balance_in_hex,16)/(10**self.decimal_places)
    return balance_in_decimal
    
  def get_account_balance_multiple(self,address_list):
    """ This function returns the balance for a list of address(es) and returns n

    Args:
        address_list (list): List of addresses.

    Returns:
        multiple_balance_dict (dict): Output in format {"address":"balance", ...}
    """
    multiple_balance_dict  = dict()
    for address in address_list:
      multiple_balance_dict[address] = self.get_account_balance(address)
    
    return multiple_balance_dict

  def total_accounts(self):
    """ This function returns the total number of accounts in the network.

    Returns:
        total_accounts_count (int): Total number of accounts in the network.
    """
    fetch_accounts_endpoint = f"/api/account?count=1"
    URL = self.block_explorer_url + fetch_accounts_endpoint
    response = requests.get(URL)
    total_accounts_count = response.json()['totalAccounts']
    return total_accounts_count