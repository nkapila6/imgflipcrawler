#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025-05-18 12:06:51 Sunday

@author: Nikhil Kapila
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

def ImgFlipFeeder(keyword:str, nsfw:bool, gifs:bool)->str:
        base_url = 'https://imgflip.com/memesearch?'
        params = dict(q=keyword)
        if nsfw:
            params['nsfw'] = 'on'
        if gifs:
            params['gifs_only'] = 'on'

        url = base_url + urlencode(params)
        return url

def ImgFlipParser(url)->dict:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')
    meme_boxes = soup.find_all('div', class_='mt-box')

    meme_dict = {}
    for box in meme_boxes:
        title = box.find('img')['alt']
        url = box.find('img')['src']
        if url.startswith('//'):
            url = 'https'+url
        url = url.replace('/4/', '/')
        meme_dict[title] = url
    return meme_dict
        

def ImgFlipCrawler(keyword:str, nsfw:bool=False, gifs:bool=False)->dict:
    url = ImgFlipFeeder(keyword, nsfw, gifs)
    memes = ImgFlipParser(url)
    return memes

# It proves simple to avoid using the library and writing my own function, lol
# class ImgFlipFeeder(Feeder):
#     def get_filter(self):
#         search_filter = Filter()

#         # nsfw filter
#         def nsfw(nsfw:bool=False)->str:
#             return 'on' if nsfw else 'off'

#         # gif filter
#         def gifs_only(gif:bool=False)->str:
#             return 'on' if gif else 'off'

#         choices = [True, False]
#         search_filter.add_rule('gifs_only', gifs_only, choices)
#         search_filter.add_rule('nsfw', nsfw, choices)
#         return search_filter

#     def feed(self, keyword, filters=None):
#         # 'https://imgflip.com/memesearch?q={}'
#         base_url = 'https://imgflip.com/memesearch?'
#         # base_url = "https://www.google.com/search?"
#         self.filter = self.get_filter()
#         filter_str = self.filter.apply(filters, sep=",")
#         filter_str = filter_str.split(',')
#         params = dict(q=keyword, gifs_only=filter_str[1], nsfw=filter_str[0])
#         fparams = {k: v for k, v in params.items() if v != 'off'}
#         url = base_url + urlencode(fparams)
#         # Add to queue and log
#         self.out_queue.put(url)
#         self.logger.debug(f"put url to url_queue: {url}")

# class ImgFlipParser(Parser):
#     def parse(self, response):
#         soup = BeautifulSoup(response.content, 'html.parser')
#         # find all meme boxes
#         meme_boxes = soup.find_all('div', class_='mt-box')
#         meme_dict = {}
#         for box in meme_boxes:
#             title = box.find('img')['alt']
#             url = box.find('img')['src']
#             if url.startswith('//'):
#                 url = 'https'+url
#             url = url.replace('/4/', '/')
#             meme_dict[title] = url
#         self.out_queue.put(meme_dict)
#         return meme_dict

# # Placeholder
# class ImgFlipDownloader(ImageDownloader):
#     # def __init__(self, *args, **kwargs):
#     #     super(ImgFlipDownloader, self).__init__(*args, **kwargs)
#     #     # self.results = {}
    
#     def download(self, task, default_ext, timeout=5, max_retry=3, overwrite=False, **kwargs):
#         """Override download to just collect the URL instead of downloading the file"""
#         return None

# class ImgFlipCrawler(Crawler):
#     def __init__(
#         self, feeder_cls=ImgFlipFeeder, parser_cls=ImgFlipParser, downloader_cls=ImgFlipDownloader, *args, **kwargs
#     ):
#         super().__init__(feeder_cls, parser_cls, downloader_cls, *args, **kwargs)

#     def crawl(self, keyword, filters=None):
#         """Start crawling and return parsed results without downloading."""
#         results = {}

        
#         self.signal.reset()
#         self.logger.info("start crawling...")

#         feeder_kwargs = dict(keyword=keyword, filters=filters)
#         self.logger.info("starting %d feeder threads...", self.feeder.thread_num)
#         self.feeder.start(**feeder_kwargs)
#         self.logger.info("starting %d parser threads...", self.parser.thread_num)
#         self.parser.start()

#         # self.logger.info("starting %d downloader threads...", self.downloader.thread_num)
#         # self.downloader.start(**downloader_kwargs)

#         while True:
#             if not self.feeder.is_alive():
#                 self.signal.set(feeder_exited=True)
#             if not self.parser.is_alive():
#                 self.signal.set(parser_exited=True)
#             # if not self.downloader.is_alive():
#             # if self.signal.get('feeder_exited') and self.signal.get('parser_exited'):
#                 break
#             # time.sleep(1)

#         if not self.feeder.in_queue.empty():
#             self.feeder.clear_buffer()
#         if not self.parser.in_queue.empty():
#             self.parser.clear_buffer()
#         # if not self.downloader.in_queue.empty():
#         #     self.downloader.clear_buffer(True)

#         self.logger.info("Crawling task done!")
#         results = self.parser.out_queue.get
#         return results
