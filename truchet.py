from PIL import Image
from argparse import ArgumentParser
from schemes import TruchetScheme, RotateScheme
import sys

def truchet(scheme, output_file, width, height, DEBUG=False):
    output_file = output_file + '.png'

    if DEBUG:
        print(
    f'''DEBUG:
    scheme:         {scheme}
    output_file:    {output_file}
    width:          {width}
    height:         {height}''')
    
    size = scheme.get_size()
    # add one for remainder
    tx = width // size[0] + 1
    ty = height // size[1] + 1
    
    output = Image.new('RGBA', (width, height), 'white')
    i = 0
    for x in range(tx):
        for y in range(ty):
            img = scheme.get_image(i, x, y)
            output.paste(img, (size[0] * x, size[1] * y))
            i = i + 1
        i = i + 1
    
    output.save(output_file)
    print(f'saved to {output_file}')


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

    try:
        tile = Image.open(args.tile)
    except IOError:
        print(f'Unable to open tile file: {tile_file}')
        sys.exit(1)
    
    schemes = [
        TruchetScheme(tile),
        RotateScheme(tile, rotation=90),
        RotateScheme(tile, rotation=180),
        RotateScheme(tile, rotation=270)
    ]
    for i in range(len(schemes)):
        truchet(schemes[i], f'{args.output}_{i}', args.width, args.height)

if __name__ == '__main__':
    main()
