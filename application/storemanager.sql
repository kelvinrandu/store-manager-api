-- create table to store users
create table if not exists users (
  id         serial    not null primary key,
  name       varchar   not null,
  email      varchar   not null,
  password   varchar   not null,
  notify     int       default 0,
  created_at timestamp not null default now(),
  updated_at timestamp          default current_timestamp
);

-- create table to handle products
create table if not exists products (
  id         serial    not null primary key,
  name      varchar   not null,
  price       integer      not null,
 quantity       integer      not null,
category     integer     default 0  references categories (id),
  created_by integer   not null references users (id),
  created_at timestamp not null default now(),
  updated_at timestamp          default current_timestamp
);

-- create table to handle categories
create table if not exists categories (
                id         serial    not null primary key,
                name      varchar   not null,
                created_by integer   not null references users (id),
                created_at timestamp not null default now(),
                updated_at timestamp          default current_timestamp
);
-- create table to handle Sales
create table if not exists sales (
                id         serial    not null primary key,
                description      varchar   not null,
                items       integer      not null references products (id),	
		total       integer      not null,
                created_by integer   not null references users (id),
                created_at timestamp not null default now(),
                updated_at timestamp          default current_timestamp
);
-- create table to handle revoked tokens
create table if not exists revoked_tokens (
  id         serial    not null primary key,
  jti     varchar   

);