import {TypeormDatabase} from '@subsquid/typeorm-store'
import {BlockPrice} from './model'
import {WETH_USDT_POOL_CONTRACT, processor} from './processor'
import * as uniswapV3PoolAbi from './abi/uniswapV3Pool'

processor.run(new TypeormDatabase({supportHotBlocks: true}), async (ctx) => {
    const blockPriceRecs: BlockPrice[] = []
    for (let block of ctx.blocks) {
        let cumulativePrice = 0
        let swapsCount = 0
        let volumeUsdt = 0
        for (let log of block.logs) {
            if (log.address === WETH_USDT_POOL_CONTRACT && log.topics[0] === uniswapV3PoolAbi.events.Swap.topic) {
                const { sqrtPriceX96, amount1 } = uniswapV3PoolAbi.events.Swap.decode(log)
                cumulativePrice += Number(sqrtPriceX96 * sqrtPriceX96 * 1_000_000_000_000_000n / 6277101735386680763835789423207666416102355444464034512896n) / 1000
                swapsCount += 1
                volumeUsdt += Math.abs(Number(amount1) / 1e6)
            }
        }
        if (cumulativePrice > 0) {
            blockPriceRecs.push(new BlockPrice({
                id: `${block.header.height}`,
                block: block.header.height,
                timestamp: block.header.timestamp / 1000,
                price: cumulativePrice / swapsCount,
                volume: volumeUsdt,
                swapsCount
            }))
        }
    }
    await ctx.store.insert(blockPriceRecs)
})
