"""Download Watersmart meter data"""

import asyncio
import argparse
import logging
from watersmart import (
    WatersmartClient,
    WatersmartClientAuthenticationError,
    WatersmartClientCommunicationError,
    WatersmartClientError,
)


PARSER = argparse.ArgumentParser(description=__doc__)

PARSER.add_argument(
    "--log-level",
    default=logging.INFO,
    type=lambda x: getattr(logging, x.upper()),
    help="Configure the logging level.",
)
PARSER.add_argument("--url", required=True)
PARSER.add_argument("--email", required=True)
PARSER.add_argument("--password", required=True)


async def main():
    args = PARSER.parse_args()
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=args.log_level, format=log_format)
    wc = WatersmartClient(url=args.url, email=args.email, password=args.password)
    try:
        data = await wc.usage()
        for datapoint in sorted(data, key=lambda x: x["read_datetime"]):
            parts = [
                f"{datapoint['local_datetime']}",
                f"usage: {datapoint['gallons']:8}gal",
                f"leak: {datapoint['leak_gallons']:8}gal",
                f"flags: {datapoint['flags']}",
            ]
            print(" | ".join(parts))
    except WatersmartClientAuthenticationError:
        logging.exception("Login failure")
    except WatersmartClientCommunicationError:
        logging.exception("Communications error")
    except WatersmartClientError:
        logging.exception("Unknown error")


def start():
    asyncio.run(main())


if __name__ == "__main__":
    start()
