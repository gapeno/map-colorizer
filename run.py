import argparse
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import json

from cartopy.io import shapereader
from random import randrange


def get_mapped_color(args, val_min, val_max, val):
    color_map = plt.get_cmap(args.cmap)
    norm = plt.Normalize(vmin=val_min, vmax=val_max)
    return color_map(norm(np.array([val])))[0]


def get_random_color(args):
    return get_mapped_color(args, val_min, val_max, randrange(val_min, val_max))


def draw_map(args):
    kw = dict(resolution='50m', category='cultural',
              name='admin_1_states_provinces')

    states_shp = shapereader.natural_earth(**kw)
    shp = shapereader.Reader(states_shp)

    subplot_kw = dict(projection=ccrs.PlateCarree())

    fig, ax = plt.subplots(figsize=(8, 6),
                           subplot_kw=subplot_kw)
    ax.set_extent([-82, -32, -38, 10])

    ax.background_patch.set_visible(False)
    ax.outline_patch.set_visible(not(args.hide_outline))

    values = args.data.values()
    min_val = min(values)
    max_val = max(values)

    for record, state in zip(shp.records(), shp.geometries()):
        name = record.attributes['name']
        if name in args.data:
            if args.random_colors:
                face_color = get_random_color(args)
            else:
                face_color = get_mapped_color(args, min_val, max_val, args.data[name])
            ax.add_geometries([state], ccrs.PlateCarree(),
                              facecolor=face_color, edgecolor='black')
    plt.show()


def define_args():
    parser = argparse.ArgumentParser(description='Configure the map-colorizer tool.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help='JSON file mapping states to a value')
    group.add_argument('-r', '--random-colors', action='store_true', help='Uses random colors.')
    parser.add_argument('-c', '--cmap', default='gist_rainbow',
                        help='PyPlot Color map name. Check color maps in https://tinyurl.com/td7vpdx.')
    parser.add_argument('--hide-outline', action='store_true',
                        help='Hide the map outline.')
    return parser.parse_args()


def start():
    args = define_args()
    with open(args.file) as f:
        args.data = json.load(f)
    draw_map(args)


start()
