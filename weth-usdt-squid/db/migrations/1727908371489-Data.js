module.exports = class Data1727908371489 {
    name = 'Data1727908371489'

    async up(db) {
        await db.query(`CREATE TABLE "block_price" ("id" character varying NOT NULL, "block" integer NOT NULL, "timestamp" integer NOT NULL, "price" numeric NOT NULL, "volume" numeric NOT NULL, "swaps_count" integer NOT NULL, CONSTRAINT "PK_6c8d531346d63b1c0118b84b587" PRIMARY KEY ("id"))`)
        await db.query(`CREATE INDEX "IDX_8e46501d9096748080fd2beafe" ON "block_price" ("block") `)
        await db.query(`CREATE INDEX "IDX_67d0de47e885ff96f85a15c93e" ON "block_price" ("timestamp") `)
    }

    async down(db) {
        await db.query(`DROP TABLE "block_price"`)
        await db.query(`DROP INDEX "public"."IDX_8e46501d9096748080fd2beafe"`)
        await db.query(`DROP INDEX "public"."IDX_67d0de47e885ff96f85a15c93e"`)
    }
}
