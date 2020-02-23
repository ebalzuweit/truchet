import sys
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
    for x in range(tx):
        for y in range(ty):
            img = fct(i, x, y)
            output.paste(img, (img_size[0] * x, img_size[1] * y))
            i = i + 1
        i = i + 1
    
    output.save(output_file)
    print(f'saved to {output_file}')


def main():
    argparser = ArgumentParser()
    argparser.add_argument('-t', '--tile', nargs='+', help='the tile file(s) to use', type=str, required=True)
    argparser.add_argument('-o', '--output', help='the output file to save', type=str, default='output.png')
    argparser.add_argument('-x', '--width', help='the width of the output', type=int, default=512)
    argparser.add_argument('-y', '--height', help='the height of the output', type=int, default=512)
    args = argparser.parse_args()

    # removed appended .png if present
    if (args.output[-4:] == '.png'):
        args.output = args.output[:-4]

    tiles = []
    try:
        for t in args.tile:
            tile = Image.open(t)
            tiles.append(tile)
    except IOError:
        print(f'Unable to open tile file: {tile_file}')
        sys.exit(1)
    
    schemes = [
        lambda i, x, y: tiles[i % len(tiles)],
        lambda i, x, y: tiles[i % len(tiles)].rotate(90 * i),
        lambda i, x, y: tiles[i % len(tiles)].rotate(180 * i),
        lambda i, x, y: tiles[i % len(tiles)].rotate(270 * i)
    ]
    for i in range(len(schemes)):
        truchet(tiles[0].size, schemes[i], f'{args.output}_{i}', (args.width, args.height))

if __name__ == '__main__':
    main()
