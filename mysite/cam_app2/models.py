from tkinter import Image
from django.db import models
from django.shortcuts import render
from django.conf import settings
from django import forms
from PIL import Image

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    StreamFieldPanel,
    PageChooserPanel,
)
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from django.core.files.storage import default_storage

from pathlib import Path

from streams import blocks

import sqlite3, datetime, os, uuid, glob, shutil
#import detect

str_uuid = uuid.uuid4()  # The UUID for image uploading

def reset():
    files_result = glob.glob(str(Path(f'{settings.MEDIA_ROOT}/Result/*.*')), recursive=True)
    files_upload = glob.glob(str(Path(f'{settings.MEDIA_ROOT}/uploadedPics/*.*')), recursive=True)
    files = []
    if len(files_result) != 0:
        files.extend(files_result)
    if len(files_upload) != 0:
        files.extend(files_upload)
    if len(files) != 0:
        for f in files:
            try:
                if (not (f.endswith(".txt"))):
                    os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))
        file_li = [Path(f'{settings.MEDIA_ROOT}/Result/Result.txt'),
                   Path(f'{settings.MEDIA_ROOT}/uploadedPics/img_list.txt'),
                   Path(f'{settings.MEDIA_ROOT}/Result/stats.txt')]
        for p in file_li:
            file = open(Path(p), "r+")
            file.truncate(0)
            file.close()

# Create your models here.
class ImagePage(Page):
    """Image Page."""

    template = "cam_app2/image.html"

    max_count = 2
    

    name_title = models.CharField(max_length=100, blank=True, null=True)
    name_subtitle = RichTextField(features=["bold", "italic"], blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("name_title"),
                FieldPanel("name_subtitle"),

            ],
            heading="Page Options",
        ),
    ]


    def reset_context(self, request):
        context = super().get_context(request)
        context["my_uploaded_file_names"]= []
        context["my_result_file_names"]=[]
        context["my_staticSet_names"]= []
        context["my_lines"]: []
        return context

    def serve(self, request):

        context = self.reset_context(request)
        #reset()
        emptyButtonFlag = False
        if request.POST.get('start')=="":
            print(request.POST.get('start'))
            print("Start selected new2")
            result_dir = r'C:\Users\4yush\Documents\DeepFracture\mysite\cam_app2\Test1\yolov5\runs\detect'
            shutil.rmtree(result_dir)
            os.makedirs(result_dir, exist_ok=True)
            context["my_result_file_names"] = []
            file1 = open(r'C:\Users\4yush\Documents\DeepFracture\mysite\media\uploadedPics\img_list.txt', 'r')
            lines = file1.readlines()
            #this for loop iterates through the whole folder for items, then if the item is a file (and not a directory) it will run the detect script
            for line in lines: #this is the directory that has all the images
                f = line.strip() #this joins the absolute path for the directory with the images, with the image filename, and sets it to the f variable
                path = r'C:\Users\4yush\Documents\DeepFracture\mysite' + f
                print(path)
                #if os.path.isfile(f): #this checks if f is a file, and not a directory
                os.system('python cam_app2\Test1\yolov5\detect.py --source=' + path + ' --weights='+r'C:\Users\4yush\Documents\DeepFracture\mysite\cam_app2\Test1\yolov5\runs\train\exp2\weights\best.pt' + '  --img=416 --conf=0.5 --save-txt')
                print(path)
                
                
                    #the final line runs the detect script. only need to change:
                    # detect script path
                    # source img path that you want to test
                    # weights path. Can choose to use either last.pt or best.pt
                    # can change the other parameters if wanted but i'm not 100% sure what they do
            result_dir = r'C:\Users\4yush\Documents\DeepFracture\mysite\cam_app2\Test1\yolov5\runs\detect'
            for fname in os.listdir(result_dir):
                exp_dir = os.path.join(result_dir, fname)
                print(exp_dir)
                for subfname in os.listdir(exp_dir):
                    result_img_path = os.path.join(exp_dir, subfname)
                    #print(result_img_path)
                    if result_img_path.endswith(".jpg"):
                        print(result_img_path)
                        with open(Path(f'{settings.MEDIA_ROOT}/Result/Result.txt'), 'a') as result_txt:
                            result_txt.write(str(result_img_path))
                            result_txt.write("\n")
                            result_txt.close()
            #file2 = open(r'C:\Users\4yush\Documents\DeepFracture\mysite\media\Result\Result.txt', 'r')
            #lines2 = file2.readlines()
            #for line in lines2:
                #print(line + " hello")
                            context["my_result_file_names"].append(str(f'{str(result_img_path)}'))
                            img = Image.open(result_img_path)
                            img.show()
            return render(request, "cam_app2/image.html", context)

        if (request.FILES and emptyButtonFlag == False):
            print("reached here files")
            reset()
            self.reset_context(request)
            context["my_uploaded_file_names"] = []
            for file_obj in request.FILES.getlist("file_data"):
                uuidStr = uuid.uuid4()
                filename = f"{file_obj.name.split('.')[0]}_{uuidStr}.{file_obj.name.split('.')[-1]}"
                with default_storage.open(Path(f"uploadedPics/{filename}"), 'wb+') as destination:
                    for chunk in file_obj.chunks():
                        destination.write(chunk)
                filename = Path(f"{settings.MEDIA_URL}uploadedPics/{file_obj.name.split('.')[0]}_{uuidStr}.{file_obj.name.split('.')[-1]}")
                with open(Path(f'{settings.MEDIA_ROOT}/uploadedPics/img_list.txt'), 'a') as f:
                    f.write(str(filename))
                    f.write("\n")

                context["my_uploaded_file_names"].append(str(f'{str(filename)}'))
            return render(request, "cam_app2/image.html", context)




        return render(request, "cam_app2/image.html", {'page': self})
