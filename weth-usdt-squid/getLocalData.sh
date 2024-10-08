#!/bin/sh

# Fetches the data from the DB of the squid running locally

PGPASSWORD="postgres" psql -h localhost -d squid -U postgres -p 23798 -c 'select block, timestamp, price, volume, swaps_count from block_price order by block asc;' --csv -o allPrices.csv
