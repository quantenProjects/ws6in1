#!/bin/env python3

import argparse
import time
import logging

import ws6in1



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", default="WS6in1")
    args = parser.parse_args()

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    keys = None

    driver = ws6in1.ws6in1(args.model)
    for result in driver.genLoopPackets():
        if keys is None:
            keys = list(result.keys())
            print(",".join(keys))
        print(",".join(str(result[k]) for k in keys))
        time.sleep(30)

