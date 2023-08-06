import sys
import getopt
import logging

from yt_concate.pipeline.steps.prelight import Preflight
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.read_caption import ReadCaption
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.postlight import Postflight
# from yt_concate.pipeline.steps.step import StepException
from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.utils import Utils


CHANNEL_ID = 'UCKSVUHI9rbbkXhvAXK-2uxA'
short_opts = 'hc:k:l:i:'
long_opts = 'help channel_id= key_word= limit= info='.split()


def main():
    inputs = {
        'channel_id': CHANNEL_ID,
        'key_word': 'incredible',
        'limit': 20,
        'info_level': 'INFO'
    }

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == ("-h", "--help"):
            print_usage()
            sys.exit(0)
        elif opt in ("-c", "--channel_id"):
            inputs['channel_id'] = arg
        elif opt in ("-k", "--key_word"):
            inputs['search_word'] = arg
        elif opt in ("-l", "--limit"):
            inputs['limit'] = int(arg)
        elif opt in ("-i", "--info"):
            inputs['info_level'] = arg

    if inputs['channel_id'] == "" or inputs['key_word'] == "":
        print_usage()
        sys.exit(2)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(message)s')

    file_handler = logging.FileHandler('event.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(inputs['info_level'])
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptions(),
        ReadCaption(),
        Search(),
        DownloadVideos(),
        EditVideo(),
        Postflight(),
    ]

    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()


def print_usage():
    print('python test2.py OPTIONS')
    print('OPTIONS:')
    print('{:>6} {:<20}{}'.format('-c', '--channel_id', 'channel id of the Youtube channel to download'))
    print('{:>6} {:<20}{}'.format('w', '--search_word', 'Search words from subtitles on Youtube channel'))
    print('{:>6} {:<20}{}'.format('l', '--limit', 'Maximum number of clips for merged videos'))
    print('{:>6} {:<20}{}'.format('i', '--info', 'Setting screen display message (ex: DEBUG、INFO、WARNING、ERROR)'))

