import argparse
import asyncio

from database import oracle

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=["create", "drop"])
args = parser.parse_args()


async def main():
    match args.action:
        case "create":
            await oracle.create_tables()
        case "drop":
            await oracle.drop_tables()


if __name__ == "__main__":
    asyncio.run(main())
