from setup import *
from zingmp3 import ZingCrawler

_origin_output_path = os.path.join(os.getcwd(), "Downloads")
_origin_log_path = os.path.join(os.getcwd(), 'log.csv')

def main():
    parser = argparse.ArgumentParser(description='Zingmp3 - A tool crawl data from zingmp3.vn')
    parser.add_argument('url', type=str, help='Url.')

    opts = parser.add_argument_group("Options")
    opts.add_argument('-s', '--save', default=False, action='store_true', help='Save media files', dest='save_media')
    opts.add_argument('-o', '--output', type=str, default=_origin_output_path, help='Download directory to save media files', dest='output_path')
    opts.add_argument('-i', '--info', default=False, action='store_true', help="Save info media.",
                      dest='save_info')
    opts.add_argument('-l', '--lyric', default=False, action='store_true', help='Download media lyric.',
                      dest='down_lyric')
    opts.add_argument("--log", default=_origin_log_path, help="Path to save log file (csv, json, excel supported)",
                      dest="log_path")
    opts.add_argument("--add-index", default=False, action="store_true", help="Add index for crawled media.",
                      dest="add_index")

    args = parser.parse_args()
    ZingCrawler(
        url=args.url,
        output_path=args.output_path,
        save_media=args.save_media,
        save_info=args.save_info,
        down_lyric=args.down_lyric,
        log_path=args.log_path,
        add_index=args.add_index
    )
    to_screen("Everything ..... Done.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write(
            fc + sd + "\n[" + fr + sb + "-" + fc + sd + "] : " + fr + sd + "User Interrupted..\n")
        sys.exit(0)
    except Exception as e:
        print(e)
        to_screen(str(e), status="error")