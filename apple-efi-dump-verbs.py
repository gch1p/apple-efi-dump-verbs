#!/usr/bin/env python3
import argparse
import sys
import os
import struct

def main():
    parser = argparse.ArgumentParser(description="Dump verbs from Apple EFI resource file")
    parser.add_argument("file", nargs=1, help="Path to file")
    parser.add_argument("--decode", action="store_true")

    args = parser.parse_args()

    file = args.file[0]
    if not os.path.isfile(file):
        return "%s does not exists or is not a file" % (file)

    with open(args.file[0], "rb") as f:
        f.seek(16)
        size = struct.unpack("i", f.read(4))[0]

        for i in range(int(size / 8)):
            val = struct.unpack("i", f.read(4))[0]
            print("0x{0:08X}".format(val), end="")
            if (args.decode):
                node_id = (val >> 20) & 0xffff
                verb_id = (val >> 8) & 0xffff
                payload = val & 0xffff
                print(" (0x{0:02x} 0x{1:04x} 0x{2:02x})".format(node_id, verb_id, payload), end="")
            print()

if __name__ == "__main__":
    result = main()
    if result:
        print("error: %s" % result)
        sys.exit(1)
