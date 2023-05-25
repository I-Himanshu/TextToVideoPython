from importlib.resources import path
import pyttsx3
import pixabay.core
from moviepy import *
from moviepy.editor import *
from keybert import KeyBERT
import random
import os
import time
px = pixabay.core("20484832-b73e12f8e2c1f4f9b0ae74bac")
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def text_to_audio(text):
    time.sleep(1)
    audio_file = f"./audio/{text[0:10]}--{len(text)}.mp3"
    print("Converting text to audio...")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 135)
    engine.setProperty('volume', 1)
    engine.save_to_file(f"<pitch middle='-100'>{text}.</pitch>", audio_file)
    engine.runAndWait()
    return AudioFileClip(audio_file)


def get_keywords_from_text(text):
    print("Getting keywords from text...")
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(text)
    random.shuffle(keywords)
    return keywords


def keywords_to_images(keywords):
    IMAGES = []
    for keyword in keywords:
        print("Getting images for keyword: {}".format(keyword))
        images = px.query(keyword)
        images = [images[i] for i in range(min(20,len(images)))]
        random.shuffle(images)
        print("{} images found".format(len(images)))
        for i in range(0, min(3,len(images))):
            path = "./images/"+keyword+str(i)+".jpg"
            images[i].download(path, "largeImage")
            IMAGES.append(path)
    return IMAGES


def images_to_video(images,seconds):
    clips = []
    # random.shuffle(images)
    for image in images:
        clips.append(ImageClip(image).set_duration(seconds/max(random.randint(2,5),len(images))))
    clips = [clip.resize((480,360)) for clip in clips]
    clips = [clip.resize(lambda t: 1+0.2*t) for clip in clips]
    clip = concatenate_videoclips(clips=clips,method='compose')
    return clip


def merge_audio_video(audio,video):
    final = video.set_audio(audio)
    return final


def get_corner_video(video_file,duration):
    FinalVideo = VideoFileClip(video_file,target_resolution=(100,100)).subclip(0,10).set_pos(("right","bottom"))
    while FinalVideo.duration < duration:
        FinalVideo = concatenate_videoclips([FinalVideo,FinalVideo])
    return FinalVideo.subclip(0,duration).without_audio().set_pos(("right","bottom"))


def add_corner_video(video1,video2):
    return CompositeVideoClip([video2,video1])


def merge_all_clips(clips):
    return concatenate_videoclips(clips=clips)