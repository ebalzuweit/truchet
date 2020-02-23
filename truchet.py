import sys, os, random
from PIL import Image
from argparse import ArgumentParser

def truchet(img_size, fct, output_file, output_size):
    output_file = output_file + '.png'

    # add one for remainder
    tx = output_size[0] // img_size[0] + 1
    ty = output_size[1] // img_size[1] + 1
    
    output = Image.new('RGBA', output_size, 'white')
    i = 0
    for y in range(ty):
        for x in range(tx):
            img = fct(i, x, y)
            output.paste(img, (img_size[0] * x, img_size[1] * y))
            i = i + 1
        i = i + 1
    
    output.save(output_file)
    print(f'saved to {output_file}')

def windmill_scheme(tile, i, x, y):
    t = tile
    if x % 2 == 1:
        t = t.rotate(90)
    if y % 2 == 0:
        t = t.rotate(-90)
    if x % 2 == 0 and y % 2 == 1:
        t = t.rotate(180)
    return t

def burst_scheme(tile, i, x, y):
    t = tile.rotate(-90)
    x_rotation = 90 * (x % 4) * (-1 if (y % 2 == 1) else 1)
    y_rotation = -90 * (y % 4)
    t = t.rotate(x_rotation + y_rotation)
    return t

def main():
    argparser = ArgumentParser()
    argparser.add_argument('-t', '--tile_dir', help='tile directory, all .png files will be tiled', type=str, required=True)
    argparser.add_argument('-o', '--output_dir', help='output directory', type=str, default='./output')
    argparser.add_argument('-x', '--width', help='the width of the output images', type=int, default=512)
    argparser.add_argument('-y', '--height', help='the height of the output images', type=int, default=512)
    args = argparser.parse_args()

    if not os.path.isdir(args.tile_dir):
        print(f'Not a valid directory: {args.tile_dir}')
        sys.exit(1)
    if not os.path.isdir(args.output_dir):
        print(f'Not a valid directory: {args.output_dir}')
        sys.exit(1)

    tiles = []
    for (dirpath, dirnames, filenames) in os.walk(args.tile_dir):
        for f in filenames:
            if f[-4:] == '.png':
                tiles.append(f)
        break # only looking at top directory
    
    for tile_file in tiles:
        # open tile image
        try:
            tile = Image.open(os.path.join(args.tile_dir, tile_file))
        except IOError:
            print(f'Unable to open tile file: {tile_file}')
            continue

        # build schemes
        schemes = {
            'standard': lambda i, x, y: tile,
            'random': lambda i, x, y: tile.rotate(90 * random.randrange(0, 3)),
            'windmill': lambda i, x, y: windmill_scheme(tile, i, x, y),
            'burst': lambda i, x, y: burst_scheme(tile, i, x, y),
            'rotate90': lambda i, x, y: tile.rotate(90 * i),
            'rotate180': lambda i, x, y: tile.rotate(180 * i),
            'rotate270': lambda i, x, y: tile.rotate(270 * i),
        }

        # run schemes
        for key in schemes.keys():
            filename = os.path.join(args.output_dir, f'{tile_file[:-4]}_{key}')
            truchet(tile.size, schemes[key], filename, (args.width, args.height))

if __name__ == '__main__':
    main()
