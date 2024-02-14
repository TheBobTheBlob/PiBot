import os
from contextlib import asynccontextmanager

import oracledb
from dotenv import load_dotenv

load_dotenv()


DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_URL = os.environ["DB_URL"]


@asynccontextmanager
async def cursor():
    # Setup
    conn = await oracledb.connect_async(user=DB_USERNAME, password=DB_PASSWORD, dsn=DB_URL)
    cursor = conn.cursor()

    yield cursor

    # Teardown
    await conn.commit()
    await conn.close()


async def annouce_creation(id: int) -> bool:
    async with cursor() as cur:
        await cur.execute("SELECT annouce_creation FROM events WHERE guild_id = :id", {"id": id})
        result = await cur.fetchone()

    if result is not None:
        return bool(result[0])
    else:
        return False


async def annoucement_channel(id: int) -> int:
    async with cursor() as cur:
        await cur.execute("SELECT channel_id FROM events WHERE guild_id = :id", {"id": id})
        result = await cur.fetchone()

    return int(result[0])


async def new_event_config(guild_id: int, channel_id: int, role_id: int) -> None:
    async with cursor() as cur:
        await cur.execute(
            "INSERT INTO events (guild_id, channel_id, role_id) VALUES (:guild_id, :channel_id, :role_id)",
            {"guild_id": guild_id, "channel_id": channel_id, "role_id": role_id},
        )


async def create_tables() -> None:
    cmds = {
        "events": [
            "guild_id VARCHAR2(32) PRIMARY KEY NOT NULL",
            "channel_id VARCHAR2(36) NOT NULL",
            "role_id VARCHAR2(36) NULL",
            "annouce_creation CHAR(1) DEFAULT 1 NOT NULL",
            "announce_deletion CHAR(1) DEFAULT 1 NOT NULL",
            "announce_update CHAR(1) DEFAULT 1 NOT NULL",
            "annouce_reminders CHAR(1) DEFAULT 1 NOT NULL",
        ]
    }

    async with cursor() as cur:
        for key, value in cmds.items():
            await cur.execute(f"CREATE TABLE {key} ({', '.join(value)})")

        await cur.execute(
            "INSERT INTO events (guild_id, channel_id, annouce_creation, announce_deletion, announce_update, annouce_reminders) VALUES ('720830635450564641', '1186343403366121574', '1', '1', '1', '1')"
        )


async def drop_tables() -> None:
    async with cursor() as cur:
        await cur.execute("DROP TABLE events")
