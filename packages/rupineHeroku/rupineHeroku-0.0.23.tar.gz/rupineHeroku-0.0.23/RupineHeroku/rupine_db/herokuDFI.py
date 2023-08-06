from RupineHeroku.rupine_db import herokuDbAccess
from psycopg2 import sql

def postDFIOracle(connection, schema, data):

    query = sql.SQL("INSERT INTO {}.dfi_oracle (id,key,is_live,block_number,block_median_timestamp,block_timestamp,active_price,next_price) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING;").format(sql.Identifier(schema))
    params = (
        data['id'],
        data['key'],
        data['is_live'],
        data['block_number'],
        data['block_median_timestamp'],
        data['block_timestamp'],
        data['active_price'],
        data['next_price']
    )
    result = herokuDbAccess.insertDataIntoDatabase(query, params, connection)    
    return result

def getOraclePrice(connection, schema, tokenSymbol:str,timestamp=None,blockNumber=None):
    tokenSymbolQuery = tokenSymbol.upper() + '-USD'
    if timestamp is None and blockNumber is None:
        return None
    elif timestamp is not None:
        query = sql.SQL("SELECT d.id, d.key, d.is_live, d.block_number, d.block_median_timestamp, d.block_timestamp, d.active_price, d.next_price, d.created_at, d.modified_at FROM {0}.dfi_oracle d \
            RIGHT JOIN (SELECT key,MIN(block_timestamp) as min_block_timestamp FROM {0}.dfi_oracle \
            WHERE 1=1 AND block_timestamp >= %s AND key = %s GROUP BY key) cond \
            ON d.key = cond.key AND d.block_timestamp = cond.min_block_timestamp").format(sql.Identifier(schema))
        params = [timestamp,tokenSymbolQuery]
    else:
        query = sql.SQL("SELECT d.id, d.key, d.is_live, d.block_number, d.block_median_timestamp, d.block_timestamp, d.active_price, d.next_price, d.created_at, d.modified_at FROM {0}.dfi_oracle d \
            RIGHT JOIN (SELECT key,MIN(block_timestamp) as min_block_timestamp FROM {0}.dfi_oracle \
            WHERE 1=1 AND block_number >= %s AND key = %s GROUP BY key) cond \
            ON d.key = cond.key AND d.block_timestamp = cond.min_block_timestamp").format(sql.Identifier(schema))
        params = [blockNumber,tokenSymbolQuery]
    
    result = herokuDbAccess.insertDataIntoDatabase(query, params, connection)    
    return result

def getlatestOracleBlock(connection, schema, tokenSymbol:str):
    tokenSymbolQuery = tokenSymbol + '-USD'
    query = sql.SQL("SELECT MAX(d.block_number) as max_block_number FROM {0}.dfi_oracle d \
        WHERE 1=1 AND key = %s ").format(sql.Identifier(schema),tokenSymbol.upper())
    params = [tokenSymbolQuery]
   
    
    result = herokuDbAccess.insertDataIntoDatabase(query, params, connection)    
    return result
