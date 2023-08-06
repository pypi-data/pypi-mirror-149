from multiprocessing import Process
import time
import logging

from pytube import YouTube

from .step import Step
from yt_concate.settings import VIDEOS_DIR


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        processes = []
        start = time.time()

        for i in range(4):
            processes.append(Process(target=self.download_videos, args=(data[i::4], utils)))

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        end = time.time()
        logging.info(f'took {end - start} seconds to download videos')
        return data

    def download_videos(self, data, utils):
        yt_set = set([found.yt for found in data])
        logging.info(f'videos to  download= {len(yt_set)}')

        for yt in yt_set:
            url = yt.url

            if utils.video_file_exists(yt):
                logging.info(f'found existing video file for {url}, skipping')
                continue
            logging.info(f'downloading {url}')
            YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id + '.mp4')
