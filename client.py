import asyncio
import argparse
import logging
from watersmart import WatersmartClient
from datetime import datetime


PARSER = argparse.ArgumentParser(description="""Download Water meter data""")

PARSER.add_argument(
    "--log-level",
    default=logging.INFO,
    type=lambda x: getattr(logging, x.upper()),
    help="Configure the logging level.",
)
PARSER.add_argument("--url", required=True)
PARSER.add_argument("--email", required=True)
PARSER.add_argument("--password", required=True)

LOCAL_TZ = datetime.now().astimezone().tzinfo


async def main():
    args = PARSER.parse_args()
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=args.log_level, format=log_format)
    wc = WatersmartClient(args.url, args.email, args.password)
    data = await wc.usage()
    # data = [
    #     {
    #             "read_datetime": 1717488000,
    #             "gallons": 67.2,
    #             "flags": None,
    #             "leak_gallons": 0,
    #     }
    # ]
    for datapoint in sorted(data, key=lambda x: x["read_datetime"]):
        # The read datetime is a timestamp in local TZ, not UTC
        ts = (
            datetime.fromtimestamp(datapoint["read_datetime"], tz=None)
            - LOCAL_TZ.utcoffset(None)
        ).replace(tzinfo=LOCAL_TZ)
        print(f"{ts.astimezone()} {datapoint}")


asyncio.run(main())
