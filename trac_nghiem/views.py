# Create your views here.
#coding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from trac_nghiem.models import question
from trac_nghiem.models import answer
from trac_nghiem.models import answered
from trac_nghiem.models import result
from trac_nghiem.models import UserProfile
from trac_nghiem.form import UserForm,UserProfileForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import datetime
import random
from django.template import RequestContext

# global variables
current_id_question = -1
current_lession = 1
def home(request):
    if (request.user.is_authenticated()==True):
        return render_to_response('base.html',{'page':"home.html",'right_main':'right_main_for_home_page.html','login':'loggedin.html','user':request.user},context_instance=RequestContext(request))
    else:
        return render_to_response('base.html',{'page':"home.html",'right_main':'right_main_for_home_page.html','login':'login.html'},context_instance=RequestContext(request))
def add(request):
    if request.user.is_authenticated():
        c = {'page':"create_question.html",'login':'loggedin.html'}
        return render_to_response('base.html',c,context_instance=RequestContext(request))
    else:
        return HttpResponse("<html><font size=30>Bạn chưa đăng nhập</html>")

def register(request):
    return render_to_response('base.html',{'page':"register.html"})

def auth_view(request):
    username= request.POST.get('email','')
    password= request.POST.get('password','')
    user = auth.authenticate(username=username,password=password)
    if (user is not None):
        if user.is_active:
            auth.login(request,user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/account/invalid')
    else:
        return HttpResponse("Invalid login")

def loggedin(request):
    return render_to_response('loggedin.html',{'user':request.user.username})
def invalid_login(request):
    return render_to_response('invalid_login.html')
def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')
def register_user(request):
    c = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            return HttpResponseRedirect('/account/register_success')
        else:
            return render_to_response('error.html')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response('register.html',{'user_form':user_form, 'profile_form':profile_form,'registered':registered},c)
def register_success(request):
    return render_to_response('register_success.html')

def createQuestion(request):
    '''ghi cau hoi vao trong co so du lieu'''

    #lấy thông tin cần thiết từ form
    print request.method
    if request.method=="POST":
        content = request.POST.get('content')  #lấy nội dung câu hỏi
        if (content):
            li=[]                                   # biến lưu danh sách các câu trả lời
            i = 1

            # lấy ra các câu trả lời từ form
            dap_an = "answer_" + str(i)
            while (request.POST.get(dap_an)):
                    i = i + 1
                    li.append(request.POST.get(dap_an))
                    dap_an = "answer_" + str(i)

            # lấy ra đáp án đúng và các thông tin khác
            dap_an_dung = request.POST.get('is_answer')
            if (dap_an_dung):
                les = request.POST.get('lession')
                giai_thich = request.POST.get('giai_thich')

                #tạo các bản ghi
                q = question(content=content,lession=les) #tạo ra bản ghi question
                q.id_user = request.user
                q.save()                                    #lưu bản ghi
                j = 0       #j là biến chạy
                s = str(1)  #s là biến string để xác định đáp án đúng
                while (j < i-1):
                    if (dap_an_dung == s): # nếu là đáp án đúng thì thực hiện lệnh if
                        ans = answer(content = li[j], is_answer=True)
                        ans.id_question = q
                        ans.save()
                    else:                   # nếu là đáp án sai thì thực hiện lệnh else
                        ans = answer(content = li[j], is_answer=False)
                        ans.id_question = q
                        ans.save()
                    j = j + 1
                    s=str(j+1)
                return render_to_response('temp.html',{'cau_hoi':content,'dap_an':dap_an_dung,'cau_tra_loi':li})
            else:
                return HttpResponse("Câu hỏi không hợp lệ")
        else:
            return HttpResponse("Câu hỏi không hợp lệ")
    return HttpResponse("Câu hỏi không hợp lệ")
def lession(request, lession):
    """lấy câu hỏi phụ thuộc vào lession"""
    if request.user.is_authenticated():
        #đếm số lượng câu hỏi
        if question.objects.count() != 0:
            so_luong_cau_hoi = question.objects.count()
            if (answered.objects.filter(id_user=request.user,lession=lession).count() == question.objects.filter(lession=lession).count() and question.objects.filter(lession=lession).count()!=0):
                    return HttpResponse("Chúc mừng,<br> Bạn đã trả lời hết câu hỏi của phần này")
            elif question.objects.filter(lession=lession).count() == 0:
                return HttpResponse('Phần này chưa có câu hỏi')
            #lấy câu hỏi random phù hợp với lession cho đến khi tìm được câu hỏi phù hợp
            while True:
                ran = random.randrange(1,so_luong_cau_hoi+1)
                cau_hoi = question.objects.get(id_question= ran)
                if (cau_hoi.lession == int(lession)):
                    if not answered.objects.filter(id_user=request.user,answered=ran):
                        tra_loi = answer.objects.filter(id_question=cau_hoi)
                        # các biến toàn cục lưu mã câu hỏi và lession hiện tại
                        global current_id_question
                        global current_lession
                        current_id_question= cau_hoi.id_question
                        current_lession = cau_hoi.lession
                        c = {'page':"home.html",'login':'loggedin.html','user':request.user,'cau_hoi':cau_hoi.content,'danh_sach_dap_an':tra_loi,'right_main':'question.html','current_url':request.get_full_path()}
                        return render_to_response('base.html',c,RequestContext(request))

        else:
            return HttpResponse("Chưa có câu hỏi,<br> hãy đặt câu hỏi giúp chúng tôi!")
    else:
        return HttpResponse("Bạn cần phải đăng nhập để xem nội dung")
def reload_lesssion(request, lession):
    """lấy câu hỏi phụ thuộc vào lession"""
    if request.user.is_authenticated():
        #đếm số lượng câu hỏi
        if question.objects.count() != 0:
            so_luong_cau_hoi = question.objects.count()
            if (answered.objects.filter(id_user=request.user,lession=lession).count() == question.objects.filter(lession=lession).count() and question.objects.filter(lession=lession).count()!=0):
                    return HttpResponse("Chúc mừng,<br> Bạn đã trả lời hết câu hỏi của phần này")
            elif question.objects.filter(lession=lession).count() == 0:
                return HttpResponse('Phần này chưa có câu hỏi')
            #lấy câu hỏi random phù hợp với lession cho đến khi tìm được câu hỏi phù hợp
            while True:
                ran = random.randrange(1,so_luong_cau_hoi+1)
                cau_hoi = question.objects.get(id_question= ran)
                if (cau_hoi.lession == int(lession)):
                    if not answered.objects.filter(id_user=request.user,answered=ran):
                        tra_loi = answer.objects.filter(id_question=cau_hoi)
                        # các biến toàn cục lưu mã câu hỏi và lession hiện tại
                        global current_id_question
                        global current_lession
                        current_id_question= cau_hoi.id_question
                        current_lession = cau_hoi.lession
                        c = {'cau_hoi':cau_hoi.content,'danh_sach_dap_an':tra_loi,'current_url':request.get_full_path()}
                        return render_to_response('reload_question.html',c,RequestContext(request))

        else:
            return HttpResponse("Chưa có câu hỏi,<br> hãy đặt câu hỏi giúp chúng tôi!")
    else:
        return HttpResponse("Bạn cần phải đăng nhập để xem nội dung")
@csrf_exempt
def check_answer(request):
    response = render_to_response("failure.html",{'current_lession':current_lession},RequestContext(request))
    print "in check"
    print 'dap an %s ' %request.POST
    if request.method == "POST":
        if request.POST.get('dap_an'):
            id_answer = request.POST.get('dap_an')
            obj = answer.objects.get(id_answer=id_answer)
            #kiểm tra đã trả lời câu hỏi này hay chưa?

            if (answered.objects.filter(id_user=request.user,answered=obj.id_question.id_question)):
                return HttpResponse("answered")
            else:
                #tạo cở sở dữ liệu các câu hỏi đã trả lời
                ans = answered(id_user=request.user,answered=obj.id_question.id_question,lession=obj.id_question.lession)
                ans.save()
                #kiểm tra xem có đã có đối tượng result ở trong bảng chưa?
                #Nếu có rồi thì thực hiện qua phương thức get
                #Nếu chưa có thì tạo đói tượng mới
                if result.objects.filter(id_user=request.user,lession=obj.id_question.lession):
                    r = result.objects.get(id_user=request.user,lession=obj.id_question.lession)
                else:
                    r = result(id_user=request.user,lession=obj.id_question.lession)
                r.last_question = obj.id_question.id_question
                r.total_answers = r.total_answers + 1
                r.last_time = datetime.datetime.now()
                if(obj.is_answer==True):
                    r.scores = r.scores + 10
                    r.correct_answers = r.correct_answers + 1
                    response = render_to_response("congratulation.html",{'current_lession':current_lession},RequestContext(request))
                else:
                    r.wrong_answers = r.wrong_answers + 1
                    if ((r.scores - 3)< 0):
                        r.scores = 0
                    else:
                        r.scores = r.scores - 3
                #xếp hạng người dùng
                if (r.scores >= 100):
                    r.rate = "thành thạo"
                elif r.scores <= 100 and r.scores >=80:
                    r.rate = "khá"
                elif r.scores <80 and r.scores>=60:
                    r.rate = "đạt"
                elif r.scores < 60 and r.scores >=30:
                    r.rate = "cần cải thiện"
                else:
                    r.rate = "mới thực hành"
                r.save()
        else:
            return HttpResponse("Bạn chưa chọn câu trả lời")
    return response
def ignore_question(request):
    if request.method == "GET" and request.user.is_authenticated():
        obj = question.objects.get(id_question=current_id_question)
        if (answered.objects.filter(id_user=request.user,answered=obj.id_question)):
                return HttpResponse("ignored")
        else:
            if question.objects.filter(id_question=current_id_question):
                ans = answered(id_user=request.user,answered=obj.id_question,lession=obj.lession)
                ans.save()
                return render_to_response('ignore_question.html',{'current_lession':current_lession},RequestContext(request))
    return HttpResponse("Nothing happens")
def statistic(request):
    # hàm thống kê thành tích người dùng

    if request.user.is_authenticated():
        r = result.objects.filter(id_user=request.user).order_by('lession')
        return render_to_response('statistic.html',{'result':r,'login':'loggedin.html','user':request.user,})
    else:
        return HttpResponse("Bạn chưa đăng nhập")
def changePassword(request):
    edited = False
    if request.user.is_authenticated():
        if request.method == "POST":
            u = request.user
            print u.id
            p1 = request.POST.get('password1')
            p2 = request.POST.get('password2')
            if (p1 == p2):
                u.set_password(request.POST.get('password1'))
                u.save()
                auth.logout(request)
                edited = True
                return render_to_response("doimatkhau_thanhcong.html")
            else:
                return HttpResponse("mật khẩu không hợp lệ")
        else:
            return render_to_response('paswordChange.html',RequestContext(request))
    else:
        return HttpResponse("Bạn chưa đăng nhập")
def profile (request):
    if request.user.is_authenticated():
        p = UserProfile.objects.get(user=request.user)
        u = request.user
        return render_to_response('profile.html',{'profile':p,'login':'loggedin.html','user':request.user})
    else:
        return HttpResponse("bạn chưa đăng nhập")