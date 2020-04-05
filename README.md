usage: run.py [-h] (-f FILE | -r) [-c CMAP] [--hide-outline]

Configure the map-colorizer tool.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  JSON file mapping states to a value
  -r, --random-colors   Uses random colors.
  -c CMAP, --cmap CMAP  PyPlot Color map name. Check color maps in
                        https://tinyurl.com/td7vpdx.
  --hide-outline        Hide the map outline.

NOTE: It currently only works with Brazillian map.
