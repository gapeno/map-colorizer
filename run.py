import json
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.io import shapereader
from random import randrange
import argparse
import numpy as np

states_dict = {
    'Acre': 'AC',
    'Alagoas': 'AL',
    'Amapá': 'AP',
    'Amazonas': 'AM',
    'Bahia': 'BA',
    'Ceará': 'CE',
    'Distrito Federal': 'DF',
    'Espírito Santo': 'ES',
    'Goiás': 'GO',
    'Maranhão': 'MA',
    'Mato Grosso': 'MT',
    'Mato Grosso do Sul': 'MS',
    'Minas Gerais': 'MG',
    'Pará': 'PA',
    'Paraíba': 'PB',
    'Paraná': 'PR',
    'Pernambuco': 'PE',
    'Piauí': 'PI',
    'Rio de Janeiro': 'RJ',
    'Rio Grande do Norte': 'RN',
    'Rio Grande do Sul': 'RS',
    'Rondônia': 'RO',
    'Roraima': 'RR',
    'Santa Catarina': 'SC',
    'São Paulo': 'SP',
    'Sergipe': 'SE',
    'Tocantins': 'TO'
}


def get_random_color(args):
    val_max = 101
    val_min = 0
    val_rand = randrange(val_min, val_max)
    color_map = plt.get_cmap(args.cmap)
    norm = plt.Normalize(vmin=val_min, vmax=val_max)
    return color_map(norm(np.array([val_rand])))[0]


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

    for record, state in zip(shp.records(), shp.geometries()):
        name = record.attributes['name']
        if name in states_dict:
            if args.random_colors:
                face_color = get_random_color(args)
            ax.add_geometries([state], ccrs.PlateCarree(),
                              facecolor=face_color, edgecolor='black')
    plt.show()


def define_args():
    parser = argparse.ArgumentParser(description='Configure the map-colorizer tool.')
    # json
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', nargs=1, type=argparse.FileType('r'),
                        help='JSON file mapping states to a value')
    group.add_argument('-r', '--random-colors', action='store_true',
                        help='Uses random colors.')
    parser.add_argument('-c', '--cmap', default='gist_rainbow',
                        help='PyPlot Color map name. Check color maps in https://tinyurl.com/td7vpdx.')
    parser.add_argument('--hide-outline', action='store_true',
                        help='Hide the map outline.')
    return parser.parse_args()


def start():
    args = define_args()
    print(args)
    draw_map(args)


start()
