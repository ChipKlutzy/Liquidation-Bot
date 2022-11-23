//SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

import "@aavecore/contracts/interfaces/IPoolAddressesProvider.sol";
import "@aavecore/contracts/interfaces/IPool.sol";

contract PoolInit {

    IPoolAddressesProvider immutable ADDRESS_PROVIDER;
    IPool immutable LENDING_POOL;

    constructor(address _provider) {
        ADDRESS_PROVIDER = IPoolAddressesProvider(_provider);
        LENDING_POOL = IPool(ADDRESS_PROVIDER.getPool());
    }
}