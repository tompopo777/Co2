# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib.auth.models import User
from django.utils import timezone

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import LoginForm, SignUpForm

from django.contrib.auth import login
from django.contrib.sessions.models import Session
from ..home.models import Profile


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            try:
                now_user = Profile.objects.get(user_id=User.objects.get(username=username).id)

                if now_user.locked_until is not None and now_user.locked_until > timezone.now():
                    now_user.failed_login_attempts = 0
                    time_remaining = now_user.locked_until - timezone.now()
                    msg = f'登入失敗過多次，請稍後{int(time_remaining.total_seconds())}秒後再嘗試!'
                    return render(request, "accounts/login.html", {"form": form, "msg": msg})

                # 登入成功
                if user is not None:
                    pre_key = now_user.session_key
                    if pre_key is not None:
                        try:
                            pre_user = Session.objects.get(session_key=pre_key)
                            pre_user.delete()
                        except:
                            pass
                    now_user.failed_login_attempts = 0
                    now_user.save()
                    login(request, user)
                    return redirect("/")
                else:
                    now_user.failed_login_attempts += 1
                    login_limit = 3
                    if now_user.failed_login_attempts >= login_limit:
                        now_user.locked_until = timezone.now() + timezone.timedelta(minutes=15)
                        now_user.failed_login_attempts = 0
                        now_user.save()
                        msg = '登入失敗過多次，請稍後10分鐘後再嘗試!'
                    else:
                        now_user.save()
                        count = now_user.failed_login_attempts
                        msg = f'帳號或密碼輸入錯誤，請重新輸入(剩餘次數: {login_limit - count})!'
            except User.DoesNotExist:
                msg = '帳號或密碼輸入錯誤，請重新輸入!'
        # else:
        #     msg = '5679'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'Account created successfully.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
