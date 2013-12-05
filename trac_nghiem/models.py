#coding: utf-8

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#bảng câu hỏi
class question(models.Model):
    id_user = models.ForeignKey(User)
    id_question = models.AutoField(primary_key=True,auto_created=True,blank=False,verbose_name="Mã câu hỏi")
    content = models.CharField(max_length=2000,blank=False,verbose_name="Nội dung câu hỏi")
    lession  = models.SmallIntegerField(blank=False,verbose_name="mức độ")
    def __unicode__(self):
        return u'%s' %(self.content)

#bảng đáp án cho mỗi câu hỏi
class answer(models.Model):
    id_answer = models.AutoField(primary_key=True, blank=False,verbose_name="Mã câu trả lời")
    id_question = models.ForeignKey(question)
    content = models.CharField(max_length=1000,blank=False,verbose_name="Câu trả lời")
    is_answer = models.BooleanField()

    def __unicode__(self):
        return u'%s' %(self.content)
class answered(models.Model):
    id_user=models.ForeignKey(User)
    answered = models.IntegerField(verbose_name="câu hỏi đã trả lời")
    lession = models.SmallIntegerField(verbose_name="bài học")
#bảng kết quả
class result(models.Model):
    id_user = models.ForeignKey(User)
    lession = models.SmallIntegerField(verbose_name="tên bài học", default=0)
    last_question = models.IntegerField(verbose_name="câu hỏi gần đây nhất",default=0)
    scores = models.IntegerField(verbose_name="tổng điểm",default=0)
    correct_answers = models.IntegerField(verbose_name="số câu trả lời đúng",default=0)
    wrong_answers = models.IntegerField(verbose_name="số câu trả lời sai",default=0)
    total_answers = models.IntegerField(verbose_name="tổng số câu trả lời",default=0)
    rate = models.CharField(verbose_name="xếp loại",default="kém",max_length=20)
    last_time = models.DateTimeField(verbose_name="lần làm bài cuối",primary_key=False)

    def __unicode__(self):
        return self.last_time

#bảng lưu thông tin người dùng
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    c = (
        ('Nam','Nam'),
        (('Nữ').decode('utf8'),('Nữ').decode('utf8')),
        (('Khác').decode('utf8'),('Khác').decode('utf8'))
    )
    sex = models.CharField(max_length=10,choices=c,default=('Khác').decode('utf8'))
    birthday = models.DateField()
    name = models.CharField(max_length=100,default=None)
    def __unicode__(self):
        return self.user.username
