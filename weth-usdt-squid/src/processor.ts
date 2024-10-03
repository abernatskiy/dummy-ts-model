import {assertNotNull} from '@subsquid/util-internal'
import {
    BlockHeader,
    DataHandlerContext,
    EvmBatchProcessor,
    EvmBatchProcessorFields,
    Log as _Log,
    Transaction as _Transaction,
} from '@subsquid/evm-processor'
import * as uniswapV3PoolAbi from './abi/uniswapV3Pool'

export const WETH_USDT_POOL_CONTRACT = '0xc7bBeC68d12a0d1830360F8Ec58fA599bA1b0e9b'.toLowerCase()

export const processor = new EvmBatchProcessor()
    .setGateway('https://v2.archive.subsquid.io/network/ethereum-mainnet')
    .setRpcEndpoint({
        url: assertNotNull(process.env.RPC_ETH_HTTP, 'No RPC endpoint supplied'),
        rateLimit: 100
    })
    .setFinalityConfirmation(75)
    .addLog({
        address: [ WETH_USDT_POOL_CONTRACT ],
        topic0: [ uniswapV3PoolAbi.events.Swap.topic ],
        range: {
            from: 16266586
        }
    })
    .setFields({
        block: {
            timestamp: true
        }
    })

export type Fields = EvmBatchProcessorFields<typeof processor>
export type Block = BlockHeader<Fields>
export type Log = _Log<Fields>
export type Transaction = _Transaction<Fields>
export type ProcessorContext<Store> = DataHandlerContext<Store, Fields>
