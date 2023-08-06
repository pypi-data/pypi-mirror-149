# import time
# import logging
#
# from pytube import YouTube
#
# from.step import Step
# from.step import StepException
#
#
# class DownloadCaptions(Step):
#     def process(self, data, inputs, utils):
#         start = time.time()
#         for yt in data:
#             logging.debug(f'downloading caption for: {yt.id}')
#             if utils.caption_file_exists(yt):
#                 logging.debug('found existing caption file')
#                 continue
#
#             try:
#                 source = YouTube(yt.url)
#                 en_caption = source.captions.get_by_language_code("a.en")
#                 en_caption_convert_to_srt = en_caption.generate_srt_captions()
#
#             except (KeyError, AttributeError):
#                 logging.error(f'Error when downloading caption for: {yt.url}')
#                 continue
#
#             text_file = open(yt.caption_filepath, "w", encoding='utf-8')
#             text_file.write(en_caption_convert_to_srt)
#             text_file.close()
#
#         end = time.time()
#         logging.info(f'took {end - start} seconds to download captions')
#
#         return data

from multiprocessing import Process
import time
import logging

from pytube import YouTube

from.step import Step
# from.step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        processes = []
        start = time.time()

        for i in range(4):
            processes.append(Process(target=self.download_captions, args=(data[i::4], utils)))

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        end = time.time()
        logging.info(f'took {end - start} seconds to download captions')

        return data

    def download_captions(self, data, utils):
        for yt in data:
            logging.debug(f'downloading caption for: {yt.id}')
            if utils.caption_file_exists(yt):
                logging.debug('found existing caption file')
                continue

            try:
                source = YouTube(yt.url)
                en_caption = source.captions.get_by_language_code("a.en")
                en_caption_convert_to_srt = en_caption.generate_srt_captions()

            except (KeyError, AttributeError):
                logging.error(f'Error when downloading caption for: {yt.url}')
                continue

            text_file = open(yt.caption_filepath, "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()

