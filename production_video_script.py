from manimlib.imports import *
from itertools import zip_longest
import spacy
nlp = spacy.load("en_core_web_sm")
topic_pos=["NN","NNP","NNPS","NNS","VB","VBP","VBZ","MD"]
from datetime import datetime
import pickle
import textwrap
import numpy as np
import os
import re
from urllib.parse import quote as url_quote
from builtins import ValueError
from google_images_download import google_images_download
image_response = google_images_download.googleimagesdownload()

wrapper_100 = textwrap.TextWrapper(width=100,
    break_long_words=False,
    break_on_hyphens=False,
    fix_sentence_endings=True)
wrapper_50 = textwrap.TextWrapper(width=50,
    break_long_words=False,
    break_on_hyphens=False,
    fix_sentence_endings=True)
wrapper_200 = textwrap.TextWrapper(width=200,
    break_long_words=False,
    break_on_hyphens=False,
    fix_sentence_endings=True)
wrapper_300 = textwrap.TextWrapper(width=300,
    break_long_words=False,
    break_on_hyphens=False,
    fix_sentence_endings=True)
todays_date=datetime.today().strftime('%Y-%m-%d')

non_alphanumeric = re.compile('[^0-9a-zA-Z\s\,\.\']')

month,date =todays_date.split("-")[1:]

def arrange_incidents_by_year(incidents):
  count=0
  for x in incidents:
    try:
      incidents[count]["numeric_year"]=int(x['year'])
      int(x['year'])
    except ValueError:
      year_list=x['year'].split()
      if "BC" in year_list:
        year_list.remove("BC")
        incidents[count]["numeric_year"]=int(year_list[0])*-1
      elif "AD" in year_list:
        year_list.remove("AD")
        incidents[count]["numeric_year"]=int(year_list[0])
    count+=1
  newlist = sorted(incidents, key=lambda k: k['numeric_year'])
  return newlist

def grouper(iterable, n, fillvalue=None):
    '''
    Collect data into fixed-length chunks or blocks
    grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    
    '''
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def replace_special_chars_to_tex(text):
  positions=[m.start() for m in non_alphanumeric.finditer(text)]
  new_text=list(text)
  for x in positions:
    new_text[x]='\\'+text[x]
  return ''.join(new_text)

def get_google_search_topics(text):
  doc=nlp(text)
  lemmas = [{"lemma":token.lemma_.strip(),"tag":token.tag_} for token in doc if not token.is_stop]
  topics= [word["lemma"] for word in lemmas if word["tag"] in topic_pos]
  return topics[:5]

def get_google_images(topic,index,limit=9):
  topic=" ".join(
      [
          url_quote(
              text
          ) for text in (
              topic.encode('utf-8')
          ).split()
      ]
  )
  arguments = {
      "keywords"         : topic,
      "limit"            : limit,
      "print_urls"       : False,
      "type"             : 'photo',
      "image_directory"  : str(index),
      "silent_mode"      : True
  }
  image_response.download(arguments)

def breakdown_sentences(text):
  doc=nlp(text.decode("utf-8"))
  return [str(sents) for sents in doc.sents]

def get_time_to_read(text):
  words=text.strip().split(" ")
  return max(((len(words)/3)+1),3.5)

with open("/gdrive/My Drive/try_daily_digest/2016-"+month+"-"+date+".pkl","rb") as file:
  all_incident=arrange_incidents_by_year(pickle.load(file))
  
count=0
for _ in all_incident:
  all_incident[count]['index']=count
  count+=1

data_set=[[inc["description"].encode("utf-8"),inc["summary"].encode("utf-8")] for inc in all_incident]
data_set=[[incidents[0],incidents[1]] for incidents in data_set]
data_set=[{"title":incidents[0],"text":incidents[1]} for incidents in data_set]
text_clip_data=[breakdown_sentences(incident["text"]) for incident in data_set]

year,title_texts=[incident["year"] for incident in all_incident],[incident["description"] for incident in all_incident]

def align_text_100(text):
  corrected_text=''
  for sentence in wrapper_100.wrap(text):
    corrected_text+=' '.join(sentence.split())+'\n'
  return corrected_text

def reshape_text_data(data):
  broken_down_sentences=[]
  for incident_texts in data:
    sentences=[]
    for incident_text in incident_texts:
      brokendown_sents=wrapper_200.wrap(incident_text)
      break_down_counts = len(brokendown_sents)
      if break_down_counts > 2:
        for sentence in wrapper_300.wrap(incident_text):
          sentences.append(sentence)
      else:
        for sentence in wrapper_300.wrap(incident_text):
          sentences.append(sentence)
    broken_down_sentences.append(sentences)
  return broken_down_sentences

text_clip_data=reshape_text_data(text_clip_data)

title_texts = [wrapper_50.wrap(x) for x in title_texts]

IMAGE_SCREEN_DIMENSION=1920/1080

def resize_image(image):
  width_array=image.get_right()-image.get_left()
  width=width_array[0]
  height_array=image.get_top()-image.get_bottom()
  height=height_array[1]
  r_image=float(width/height)

  if r_image > IMAGE_SCREEN_DIMENSION or r_image == IMAGE_SCREEN_DIMENSION:
	r_s=FRAME_WIDTH/width
	image_width=width*r_s
	image_height=height*r_s

  else:
	r_s=FRAME_HEIGHT/height
	image_width=width*r_s
	image_height=height*r_s

  image.set_height(image_height)

  image.set_width(image_width)
  return image








class final_video(Scene):
  '''
  complete video
  '''
  CONFIG={
      "include_sound": True,
      "camera_config":{
          "background_color": WHITE,
          "background_opacity":0.4,
      }
  }
  def construct(self):
  self.intro_video()
  self.content_video()
  self.outro()
  
  
  def intro_video(self):
    self.add_sound("/gdrive/My Drive/lil daufe/audios/intro audio.mp3")
    intro_pics=["/gdrive/My Drive/lil daufe/intro_pics/"+img for img in sorted(os.listdir("/gdrive/My Drive/lil daufe/intro_pics"))]
    for pic in intro_pics[:4]:
      self.intro_anim(pic,0.4)
    for pic in intro_pics[4:14]:
      self.intro_anim(pic,0.2)
    TITLE_TEXT=r'''
      HISTORY IN MINUTES
    '''
    TITLE=TextMobject(
        TITLE_TEXT,
        fill_color=BLACK,
        stroke_color=WHITE,
        stroke_width=2,
        stroke_opacity=1
    ).scale(2.2)
    temp_background=resize_image(ImageMobject(intro_pics[14]))
    self.add(temp_background)
    self.play(FadeIn(TITLE),run_time=0.4)
    self.add_foreground_mobject(TITLE)
    self.remove(temp_background)
    for pic in intro_pics[14:]:
      self.intro_anim(pic,0.2)
    end_pic=resize_image(ImageMobject(intro_pics[-1]))
    self.play(FadeOut(end_pic),FadeOut(TITLE))
    
  def intro_anim(self,pic,time):
    img=ImageMobject(pic)
    image=resize_image(img)
    self.add(image)
    self.wait(time)
    self.remove(image)
	
  def content_video(self):
    self.add_sound("/gdrive/My Drive/lil daufe/audios/birth_of_a_hero.mp3")
    self.IMAGE_SCREEN_DIMENSION=1920/1080
    for incident in all_incident:
      text=incident["description"]
      index=incident["index"]
      get_google_images(' '.join(get_google_search_topics(text)),index)
    images_directory=[]
    for directory in range(len(text_clip_data)):
      images_directory.append(sorted(["/content/downloads/"+str(directory)+"/"+img for img in os.listdir("/content/downloads/"+str(directory))]))
    for title,current_year,images,texts in zip(title_texts,year,images_directory,text_clip_data):
      self.image_slideshow(images[0],title,current_year)
    os.system('rm -rf downloads')
  def image_slideshow(self,image,text,current_year):
    image_clip=ImageMobject(image)
    image_clip=resize_image(image_clip)
    image_clip.add_updater(lambda g,dt:g.scale(1.0003))
    self.add(image_clip)
    self.animate_data(text,current_year)
    self.remove(image_clip)

  def animate_data(self,text,current_year):
    year_text=TextMobject("year: "+current_year,fill_color=BLACK)
    year_text.add_background_rectangle(color=WHITE,stroke_width=10,stroke_opacity=0.75)
    width=np.array([year_text.get_width(),0,0])
    year_text.move_to(0.8*TOP-(width/2)+LEFT_SIDE+(0.2*LEFT))
    self.play(year_text.shift,width+RIGHT,rate_func=linear,run_time=0.25)
    self.text_clips_animation(text)
    self.play(year_text.shift,-1*(width+RIGHT),rate_func=linear,run_time=0.25)
    self.remove(year_text)

  def text_clips_animation(self,texts):
    for x,y in grouper(texts,2,""):
      self.text_animation(x,y)

  def text_animation(self,upper_text,lower_text):
    upper_text_mobject   =   self.get_text_mobject(upper_text)
    lower_text_mobject   =   self.get_text_mobject(lower_text)
    lower_text_mobject.next_to(upper_text_mobject,DOWN)
    informations = Group(upper_text_mobject,lower_text_mobject)
    informations.add_background_rectangle(color=WHITE,stroke_opacity=0.75)
    height_by_two=informations.get_height()/2
    height_adjustment=np.array([0,height_by_two+0.1,0])
    width=np.array([informations.get_width(),0,0])
    informations.move_to(0.8*BOTTOM+height_adjustment-(width/2)+LEFT_SIDE+(0.2*LEFT))
#     informations.shift()
    time=get_time_to_read(upper_text+" "+lower_text)
    self.play(informations.shift,width+(0.4*RIGHT),rate_func=linear,run_time=0.4)
    self.wait(time-0.5)
    self.play(informations.shift,-1*(width+0.4*RIGHT),rate_func=linear,run_time=0.4)
    self.remove(informations)

  def get_text_mobject(self,txt):
    try:
      text_clip=TextMobject(txt,fill_color=BLACK).scale(0.7)
    except:
      txt=replace_special_chars_to_tex(txt)
      text_clip=TextMobject(txt,fill_color=BLACK).scale(0.7)
    return text_clip

  def outro(self):
    self.add_sound("/gdrive/My Drive/lil daufe/audios/outro.mp3")
    outro_pics=["/gdrive/My Drive/lil daufe/outro_pics/"+img for img in sorted(os.listdir("/gdrive/My Drive/lil daufe/outro_pics"))]
    raw_outro_image=ImageMobject(outro_pics[0])
    resized_outro_image=resize_image(raw_outro_image).shift(11*RIGHT)
    self.wait()
    self.play(resized_outro_image.shift,15*LEFT)
    like_object=ImageMobject(outro_pics[2]).shift(2*RIGHT+3*UP)
    lil_dafue_text="Lil Dafue"
    lil_dafue_object=TextMobject(lil_dafue_text,fill_color=BLACK).scale(2.8)
    lil_dafue=lil_dafue_object.next_to(like_object,DOWN)
    lil_dafue=lil_dafue.shift(0.5*RIGHT)
    lcs=ImageMobject(outro_pics[1]).scale(1.3).shift(9*RIGHT+1.5*DOWN)

    self.play(FadeIn(like_object))
    self.play(FadeIn(lil_dafue))
    self.wait(2)
    self.play(lcs.shift,7*LEFT)

    lil_dafue_text="Lil Dafue"
    lil_dafue_object=TextMobject(lil_dafue_text,fill_color=BLACK).scale(2.8)
    lil_dafue=lil_dafue_object.next_to(like_object,DOWN)
    lil_dafue=lil_dafue.shift(0.5*RIGHT)
    self.play(FadeIn(lil_dafue))

  
  
