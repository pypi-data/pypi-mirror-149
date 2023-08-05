from web3 import Web3
from web3._utils.encoding import (
    hexstr_if_str,
    to_bytes,
)


# xrc20 abi.json
xrc20abi = "[{\"constant\":true,\"inputs\":[],\"name\":\"name\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_spender\",\"type\":\"address\"},{\"name\":\"_value\",\"type\":\"uint256\"}],\"name\":\"approve\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"totalSupply\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_from\",\"type\":\"address\"},{\"name\":\"_to\",\"type\":\"address\"},{\"name\":\"_value\",\"type\":\"uint256\"}],\"name\":\"transferFrom\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"decimals\",\"outputs\":[{\"name\":\"\",\"type\":\"uint8\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"_owner\",\"type\":\"address\"}],\"name\":\"balanceOf\",\"outputs\":[{\"name\":\"balance\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"symbol\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_to\",\"type\":\"address\"},{\"name\":\"_value\",\"type\":\"uint256\"}],\"name\":\"transfer\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"_owner\",\"type\":\"address\"},{\"name\":\"_spender\",\"type\":\"address\"}],\"name\":\"allowance\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"fallback\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":true,\"name\":\"owner\",\"type\":\"address\"},{\"indexed\":true,\"name\":\"spender\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"value\",\"type\":\"uint256\"}],\"name\":\"Approval\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":true,\"name\":\"from\",\"type\":\"address\"},{\"indexed\":true,\"name\":\"to\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"value\",\"type\":\"uint256\"}],\"name\":\"Transfer\",\"type\":\"event\"}]"


# This is a class which consists all the methods as per XRC20 standards.

class XRC20:

    def __init__(self,rpcUrl):
        self.rpcUrl = rpcUrl

    # rpc url connection.

    def web3Connection(self):
        w3 = Web3(Web3.HTTPProvider(self.rpcUrl))
        return w3

    # contract Instance 

    def getContractInstance(self,tokenAddr):
        contractInstance = self.web3Connection().eth.contract(address=tokenAddr, abi=xrc20abi)
        return contractInstance
        
    # Gets the Name of the specified address.
    # Token address is required as argument.

    def name(self,tokenAddr):
        name = self.getContractInstance(tokenAddr).functions.name().call()
        return name

    # # Gets total supply of token.
    # # Token address is required as argument.

    def totalSupply(self,tokenAddr):
        totalSupply = self.getContractInstance(tokenAddr).functions.totalSupply().call()
        totalSupply = self.web3Connection().fromWei(totalSupply, 'ether')
        return totalSupply

    # Gets the Decimal of the specified address.
    # Token address is required as argument.

    def decimal(self,tokenAddr):
        decimal = self.getContractInstance(tokenAddr).functions.decimals().call()
        return decimal

    # Gets the Symbol of the specified address.
    # Token address is required as argument.

    def symbol(self,tokenAddr):
        symbol = self.getContractInstance(tokenAddr).functions.symbol().call()
        return symbol

    # Gets the balance of the specified address.
    # token address, owner address are required as arguments.

    def balanceOf(self,tokenAddr, ownerAddress):
        owner = Web3.toChecksumAddress(ownerAddress)
        balance = self.getContractInstance(tokenAddr).functions.balanceOf(owner).call()
        return self.web3Connection().fromWei(balance, 'ether')

    # This method returns how much allowance spender have from owner.
    # This function required three arguments.
    # owner address, spender address, token address.

    def allowance(self,tokenAddr, ownerAddress, spenderAddress):
        owner = Web3.toChecksumAddress(ownerAddress)
        spender = Web3.toChecksumAddress(spenderAddress)
        Allowance = self.getContractInstance(tokenAddr).functions.allowance(owner, spender).call()
        return self.web3Connection().fromWei(Allowance, 'ether')

    # Transfer XDC for a specified address.
    # This function requires following arguments.
    # private key, recipient address, amount.

    def transferXDC(self, ownerAddress, receiverAddress, ownerPrivateKey, amount):

        owner = Web3.toChecksumAddress(ownerAddress)
        spender = Web3.toChecksumAddress(receiverAddress)
        amount = self.web3Connection().toWei(amount, 'ether')

        nonce = self.web3Connection().eth.getTransactionCount(owner)
        gasPrice = self.web3Connection().eth.gas_price
        estimateGas = self.web3Connection().eth.estimateGas({
            'to': spender,
            'from': owner,
            'value': amount
        })

        tx = {
            'nonce': nonce,
            'to': spender,
            'value': amount,
            'gas': estimateGas,
            'gasPrice': gasPrice,
        }

        signedTx = self.web3Connection().eth.account.signTransaction(tx, ownerPrivateKey)

        txHash = self.web3Connection().eth.sendRawTransaction(signedTx.rawTransaction)
        return self.web3Connection().toHex(txHash)

    # Transfer token for a specified address.
    # This function requires following arguments.
    # ownerAddress, ownerPrivateKey, receiver address, token address, amount.

    def transferToken(self,tokenAddr, ownerAddress, ownerPrivateKey,  receiverAddress, amount):

        owner = Web3.toChecksumAddress(ownerAddress)
        spender = Web3.toChecksumAddress(receiverAddress)

        balance = self.balanceOf(tokenAddr,owner)

        if amount > balance:
            return "amount exceeds balance"

        amount = self.web3Connection().toWei(amount, 'ether')

        Transfer = self.getContractInstance(tokenAddr).functions.transfer(spender, amount)

        hexData = Transfer._encode_transaction_data()

        data = hexstr_if_str(to_bytes, hexData)

        estimateGas = Transfer.estimateGas(
            {
                'from': owner,
            }
        )

        nonce = self.web3Connection().eth.getTransactionCount(owner)
        gasPrice = self.web3Connection().eth.gas_price

        tx = {
            'nonce': nonce,
            'to': tokenAddr,
            'data': data,
            'gas': estimateGas,
            'gasPrice': gasPrice,
        }

        signedTx = self.web3Connection().eth.account.signTransaction(tx, ownerPrivateKey)

        txHash = self.web3Connection().eth.sendRawTransaction(signedTx.rawTransaction)
        return self.web3Connection().toHex(txHash)

    # Approve the passed address to spend the specified amount of tokens on behalf of owner.
    # This function required arguments.
    # ownerAddress, ownerPrivateKey, spenderAddress, tokenAddr, amount.

    def approve(self, tokenAddr, ownerAddress, ownerPrivateKey,  spenderAddress, amount):

        owner = Web3.toChecksumAddress(ownerAddress)
        spender = Web3.toChecksumAddress(spenderAddress)

        balance = self.balanceOf(tokenAddr, owner)
        allowanceAmount = self.allowance(tokenAddr,owner,spender)

        if amount > balance and allowanceAmount > balance:
            return "amount exceeds balance"

        amount = self.web3Connection().toWei(amount, 'ether')

        approveData = self.getContractInstance(tokenAddr).functions.approve(spender, amount)

        hexData = approveData._encode_transaction_data()

        data = hexstr_if_str(to_bytes, hexData)

        estimateGas = approveData.estimateGas()

        nonce = self.web3Connection().eth.getTransactionCount(owner)

        gasPrice = self.web3Connection().eth.gas_price

        tx = {
            'nonce': nonce,
            'to': tokenAddr,
            'data': data,
            'gas': estimateGas,
            'gasPrice': gasPrice,
        }

        signedTx = self.web3Connection().eth.account.signTransaction(tx, ownerPrivateKey)

        txHash = self.web3Connection().eth.sendRawTransaction(signedTx.rawTransaction)
        return self.web3Connection().toHex(txHash)

    # increase the amount of tokens that an owner allowed to a spender.
    # This function required arguments.
    # owner address, ownerPrivateKey, spender address, token address, amount.

    def increaseAllowance(self, tokenAddr, ownerAddress, ownerPrivateKey,  spenderAddress, amount):

        owner = Web3.toChecksumAddress(ownerAddress)
        spender = Web3.toChecksumAddress(spenderAddress)

        balance = self.balanceOf(tokenAddr, owner)

        allowanceAmount = self.allowance(tokenAddr,owner,spender)

        allowanceAmount = self.web3Connection().fromWei(allowanceAmount, 'ether')

        totalAmount = allowanceAmount + amount

        if totalAmount > balance:
            return "amount exceeds balance"

        totalAmount = self.web3Connection().toWei(totalAmount, 'ether')

        Transfer = self.getContractInstance(tokenAddr).functions.approve(spender, totalAmount)

        hexData = Transfer._encode_transaction_data()

        data = hexstr_if_str(to_bytes, hexData)

        estimateGas = Transfer.estimateGas()

        nonce = self.web3Connection().eth.getTransactionCount(owner)
        gasPrice = self.web3Connection().eth.gas_price

        tx = {
            'nonce': nonce,
            'to': tokenAddr,
            'data': data,
            'gas': estimateGas,
            'gasPrice': gasPrice,
        }
        signedTx = self.web3Connection().eth.account.signTransaction(tx, ownerPrivateKey)

        txHash = self.web3Connection().eth.sendRawTransaction(signedTx.rawTransaction)
        return self.web3Connection().toHex(txHash)

    # # decrease the amount of tokens that an owner allowed to a spender.
    # # This function required arguments.
    # # owner address, ownerPrivateKey, spender address, token address, amount.

    def decreaseAllowance(self, tokenAddr, ownerAddress, ownerPrivateKey,  spenderAddress, amount):

        owner = Web3.toChecksumAddress(ownerAddress)
        spender = Web3.toChecksumAddress(spenderAddress)

        allowanceAmount = self.allowance(tokenAddr,owner,spender)
        allowanceAmount = self.web3Connection().fromWei(allowanceAmount, 'ether')

        if allowanceAmount >= amount:
            totalAmount = allowanceAmount - amount
        else:
            totalAmount = amount - allowanceAmount

        totalAmount = self.web3Connection().toWei(totalAmount, 'ether')

        approveData = self.getContractInstance(tokenAddr).functions.approve(spender, totalAmount)

        hexData = approveData._encode_transaction_data()

        data = hexstr_if_str(to_bytes, hexData)

        estimateGas = approveData.estimateGas()

        nonce = self.web3Connection().eth.getTransactionCount(owner)
        gasPrice = self.web3Connection().eth.gas_price

        tx = {
            'nonce': nonce,
            'to': tokenAddr,
            'data': data,
            'gas': estimateGas,
            'gasPrice': gasPrice,
        }
        signedTx = self.web3Connection().eth.account.signTransaction(tx, ownerPrivateKey)

        txHash = self.web3Connection().eth.sendRawTransaction(signedTx.rawTransaction)
        return self.web3Connection().toHex(txHash)

    # # Transfer tokens from one address to another.
    # # This function requires following arguments.
    # # owner address, spenderPrivateKey, spender address, receiver address, token address, amount.

    def transferFrom(self, tokenAddr, ownerAddress,  spenderPrivateKey,  spenderAddress, receiver, amount):

        owner = Web3.toChecksumAddress(ownerAddress)
        receiverAddres = Web3.toChecksumAddress(receiver)
        spender = Web3.toChecksumAddress(spenderAddress)

        allowanceAmount = self.allowance(tokenAddr,owner,spender)
        allowanceAmount = self.web3Connection().fromWei(allowanceAmount, 'ether')

        amount = self.web3Connection().toWei(amount, 'ether')

        if amount > allowanceAmount:
            return "amount exceeds allowance"

        transferData = self.getContractInstance(tokenAddr).functions.transferFrom(
            owner, receiverAddres, amount)

        estimateGas = transferData.estimateGas({
            'from': spender,
        })

        hexData = transferData._encode_transaction_data()

        data = hexstr_if_str(to_bytes, hexData)

        nonce = self.web3Connection().eth.getTransactionCount(spender)
        gasPrice = self.web3Connection().eth.gas_price

        tx = {
            'nonce': nonce,
            'to': tokenAddr,
            'data': data,
            'gas': estimateGas,
            'gasPrice': gasPrice,
        }
        signedTx = self.web3Connection().eth.account.signTransaction(tx, spenderPrivateKey)

        txHash = self.web3Connection().eth.sendRawTransaction(signedTx.rawTransaction)
        return self.web3Connection().toHex(txHash)
