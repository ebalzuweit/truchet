import sys
import random
from PIL import Image
from argparse import ArgumentParser

def truchet(img_size, fct, output_file, output_size, DEBUG=False):
    output_file = output_file + '.png'

    if DEBUG:
        print(
    f'''DEBUG:
    scheme:         {scheme}
    output_file:    {output_file}
    width:          {width}
    height:         {height}''')
    
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

def main():
    argparser = ArgumentParser()
    argparser.add_argument('-t', '--tile', help='the tile file to use', type=str, required=True)
    argparser.add_argument('-o', '--output', help='the output file to save', type=str, default='output.png')
    argparser.add_argument('-x', '--width', help='the width of the output', type=int, default=512)
    argparser.add_argument('-y', '--height', help='the height of the output', type=int, default=512)
    args = argparser.parse_args()

    # removed appended .png if present
    if (args.output[-4:] == '.png'):
        args.output = args.output[:-4]

    # open tile image
    try:
        tile = Image.open(args.tile)
    except IOError:
        print(f'Unable to open tile file: {tile_file}')
        sys.exit(1)
    
    # build schemes
    schemes = {
        'standard': lambda i, x, y: tile,
        'random': lambda i, x, y: tile.rotate(90 * random.randrange(0, 3)),
        'windmill': lambda i, x, y: windmill_scheme(tile, i, x, y),
        'rotate90': lambda i, x, y: tile.rotate(90 * i),
        'rotate180': lambda i, x, y: tile.rotate(180 * i),
        'rotate270': lambda i, x, y: tile.rotate(270 * i),
    }

    # run schemes
    for key in schemes.keys():
        truchet(tile.size, schemes[key], f'{args.output}_{key}', (args.width, args.height))

if __name__ == '__main__':
    main()
