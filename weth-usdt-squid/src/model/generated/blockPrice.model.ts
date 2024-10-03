import {Entity as Entity_, Column as Column_, PrimaryColumn as PrimaryColumn_, IntColumn as IntColumn_, Index as Index_, FloatColumn as FloatColumn_} from "@subsquid/typeorm-store"

@Entity_()
export class BlockPrice {
    constructor(props?: Partial<BlockPrice>) {
        Object.assign(this, props)
    }

    @PrimaryColumn_()
    id!: string

    @Index_()
    @IntColumn_({nullable: false})
    block!: number

    @Index_()
    @IntColumn_({nullable: false})
    timestamp!: number

    @FloatColumn_({nullable: false})
    price!: number

    @FloatColumn_({nullable: false})
    volume!: number

    @IntColumn_({nullable: false})
    swapsCount!: number
}
