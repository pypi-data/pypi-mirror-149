import argparse

from eos import make_fancy_output_dir

from labanotation.process import get_labanotation_results


def main():
    parser = argparse.ArgumentParser(
        description='Convert laban suite csv file to image and labanotations.')
    parser.add_argument('--out', '-o', default='./result', type=str,
                        help='Output directory path.')
    parser.add_argument('--video-path', default=None, type=str,
                        help='Input video path')
    parser.add_argument(
        '-b', '--base-rotation-style',
        type=str, default='every', choices=['every', 'first', 'update'])
    parser.add_argument('csv_filepath', type=str)
    args = parser.parse_args()
    output_path = make_fancy_output_dir(args.out, args)
    get_labanotation_results(args.csv_filepath,
                             output_path,
                             video_path=args.video_path,
                             base_rotation_style=args.base_rotation_style)


if __name__ == '__main__':
    main()
