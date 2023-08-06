#!/usr/bin/env python3

import argparse
from bioblu.ds_manage import image_cutting

if __name__ == "__main__":
    p = argparse.ArgumentParser()

    p.add_argument('-s', '--img-source', dest='fdir')
    p.add_argument('-th', '--horz_tile_count', default=3, dest='horz_n', type=int)
    p.add_argument('-tv', '--vert_tile_count', default=2, dest='vert_n', type=int)
    p.add_argument('-a', '--altitude_m', dest='altitude', type=int)
    p.add_argument('-l', '--location', default='no_location', dest='location', type=str)
    p.add_argument('--save-tiles', dest='save_tiles', action='store_true', default=True)
    p.add_argument('--save-csv', dest='save_csv', action='store_true', default=True)
    p.add_argument('-o', '--output-dir', dest='target_dir', default=None)

    args = p.parse_args()

    image_cutting.create_tiles(img_dir=args.fdir,
                               horizontal_tile_count=args.horz_n,
                               vertical_tile_count=args.vert_n,
                               altitude_m=args.altitude,
                               save_tiles_csv=args.save_csv,
                               save_tile_images=args.save_tiles,
                               target_dir=args.target_dir)

# Example:
# python3 create_tiles.py -s /home/user/img_dir -th 3 -tv 2 -a 5 --save-tiles --save-csv --location "testbeach"