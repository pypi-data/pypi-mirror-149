CREATE TYPE order_status AS ENUM ('INITIALIZED', 'DENIED', 'SUBMITTED', 'ACCEPTED', 'REJECTED', 'CANCELED', 'EXPIRED', 'TRIGGERED', 'PENDING_UPDATE', 'PENDING_CANCEL', 'PARTIALLY_FILLED', 'FILLED');
CREATE TYPE order_side AS ENUM ('BUY', 'SELL');
CREATE TYPE order_type AS ENUM ('MARKET', 'LIMIT', 'STOP_MARKET', 'STOP_LIMIT', 'TRAILING_STOP_MARKET', 'TRAILING_STOP_LIMIT');
CREATE TYPE order_time_in_force AS ENUM ('GTC', 'IOC', 'FOK', 'GTD', 'DAY', 'AT_THE_OPEN', 'AT_THE_CLOSE');
CREATE TYPE order_contingency_type AS ENUM ('NONE', 'OTO', 'OCO');
CREATE TYPE order_liquidity_side AS ENUM ('NONE', 'MAKER', 'TAKER');
CREATE TYPE position_side AS ENUM ('FLAT', 'LONG', 'SHORT');

-- pg_enum require explict CAST by default ?
CREATE CAST (varchar AS position_side) WITH INOUT AS ASSIGNMENT;
CREATE CAST (varchar AS order_type) WITH INOUT AS ASSIGNMENT;
CREATE CAST (varchar AS order_side) WITH INOUT AS ASSIGNMENT;
CREATE CAST (varchar AS order_status) WITH INOUT AS ASSIGNMENT;
CREATE CAST (varchar AS order_time_in_force) WITH INOUT AS ASSIGNMENT;
CREATE CAST (varchar AS order_contingency_type ) WITH INOUT AS ASSIGNMENT;
CREATE CAST (varchar AS order_liquidity_side ) WITH INOUT AS ASSIGNMENT;

CREATE TABLE IF NOT EXISTS orders (
	ts_last TIMESTAMPTZ NOT NULL,
	ts_init TIMESTAMPTZ NOT NULL,
	trader_id VARCHAR NOT NULL,
	strategy_id VARCHAR NOT NULL,
	instrument_id VARCHAR NOT NULL,
	client_order_id VARCHAR NOT NULL,
	order_list_id VARCHAR,
	position_id VARCHAR,
	account_id VARCHAR,
	last_trade_id VARCHAR,
        "type" order_type NOT NULL,
        side order_side NOT NULL,
        quantity decimal(32,16) NOT NULL,
        price decimal(32,16),
        time_in_force order_time_in_force NOT NULL,
        is_reduce_only BOOLEAN NOT NULL,
        avg_px decimal(32,16),
        filled_qty decimal(32,16) NOT NULL,
        slippage decimal(32,16) NOT NULL,
        status order_status NOT NULL,
        contingency_type order_contingency_type NOT NULL,
        linked_order_ids VARCHAR,
        parent_order_id VARCHAR,
        tags JSONB,
        expire_time_ns bigint,
        liquidity_side order_liquidity_side NOT NULL,
        is_post_only BOOLEAN NOT NULL,
        display_qty decimal(32,16),
        trigger_price decimal(32,16),
        trigger_type VARCHAR,
        limit_offset VARCHAR,
        trailing_offset VARCHAR,
        offset_type VARCHAR,
	PRIMARY KEY(client_order_id)
);


CREATE TABLE IF NOT EXISTS positions (
        position_id VARCHAR NOT NULL,
        account_id VARCHAR NOT NULL,
        from_order VARCHAR NOT NULL,
        strategy_id VARCHAR NOT NULL,
        instrument_id VARCHAR NOT NULL,
        entry order_side NOT NULL,
        side position_side NOT NULL,
        net_qty decimal(32,16) NOT NULL,
        quantity decimal(32,16) NOT NULL,
        peak_qty decimal(32,16) NOT NULL,
	ts_opened TIMESTAMPTZ NOT NULL,
	ts_closed TIMESTAMPTZ NOT NULL,
	duration_ns bigint NOT NULL,
        avg_px_open decimal(32,16) NOT NULL,
        avg_px_close decimal(32,16),
        quote_currency VARCHAR NOT NULL,
        base_currency VARCHAR NOT NULL,
        cost_currency VARCHAR NOT NULL,
        realized_points decimal(32,16) NOT NULL,
        realized_return VARCHAR NOT NULL,
        realized_pnl VARCHAR NOT NULL,
        commissions VARCHAR NOT NULL,
	PRIMARY KEY(position_id)
);


CREATE INDEX index_orders_ts_init ON orders (ts_init);
CREATE INDEX index_orders_state ON orders (status);

CREATE INDEX index_positions_ts_opend ON positions (ts_opened);
CREATE INDEX index_positions_instrument ON positions (instrument_id);
