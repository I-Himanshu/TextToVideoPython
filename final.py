import os
from textwrap import TextWrapper
from tools import text_to_audio,get_keywords_from_text,keywords_to_images, images_to_video, merge_audio_video, get_corner_video, add_corner_video, merge_all_clips

ARTICLE = """Artificial intelligence is a next-gen intelligence incorporated into the machines that can respond according to the different situations. AI is considered comparable to the natural intelligence of human beings and artificially intelligent machines perform various functions such as learning, reasoning and solving problems. Specifically, artificial intelligence refers to the simulation of the human brain and reasoning which particularly solves and plan things according to the surrounding scenario. Artificial intelligence is one of the most innovative developments in the realm of technology and according to experts, Artificial intelligence will form the basis of our future generation.
Artificial intelligence is deemed to provide various benefits in different domains such as healthcare, banks, information technology, businesses and much more. Artificial intelligence has a noteworthy application in the healthcare realm wherein machines will operate on people for different checkups without human intervention. With the use of complex algorithms, Artificial intelligence can provide data-driven solutions to the doctors which in turn help them to make better decisions about the patient’s health.
Artificial intelligence has a great function in business performance in which chatbots offer immediate response to the queries and provide 24/7 support to the customers. This ultimately saves the time and effort required to carry out a successful business.
Nowadays, you use Google Maps, Uber cabs, and many other applications that automatically detect your issues and answers to your queries in no time- all thanks to artificial intelligence. The maps usually instruct you to take a different route as the one you are going to follow might have huge traffic congestion, all this is possible with the help of AI machines.
Artificial intelligence has greatly influenced various other fields related to manufacturing, education, finance, gaming, art, government and much more. AI has the potential to execute tasks related to speech recognition, face recognition, translating different languages, decision-making etc. Therefore, it is the future of technology as it can solve highly complex problems and delivers you the result within no time."""

texts = ARTICLE.split(".")[:3]
ALL_CLIPS = []
for i,text in enumerate(texts):
    if len(text) < 5:
        continue
    text = text.strip()
    print(f"{i}:"*10)
    print("Processing text: {}".format(text))
    keywords = get_keywords_from_text(text)
    # keywords = keywords if len(keywords) < 3 else keywords[:3]
    keywords = [keyword for keyword,chances in keywords if chances > 0.4]
    audio = text_to_audio(text)
    audio_duration = audio.duration
    print("Audio duration: ", audio_duration)
    # keywords = keywords if len(keywords) < int(audio.duration) else keywords[:int(audio_duration/2)]
    print("Keywords: ", keywords)
    images = keywords_to_images(keywords)
    print("Images: ", images)
    video = images_to_video(images,audio_duration)
    video = merge_audio_video(audio,video)
    corner_video = get_corner_video("video.mp4",video.duration)
    OUTPUT = add_corner_video(corner_video,video)
    ALL_CLIPS.append(OUTPUT)
    for image in images:
        try:
            os.remove(image)
        except:
            print("Error while deleting image: ", image)
merge_all_clips(ALL_CLIPS).write_videofile(ARTICLE[:10]+".mp4",fps=24)