# from functools import wraps
# from django.contrib.auth import logout
# from django.shortcuts import redirect
#
#
# def check_session_id(view_func):
#     @wraps(view_func)
#     def wrapped_view(request, *args, **kwargs):
#         session_key = request.session.session_key
#         print('aaaa')
#         print(session_key)
#         print(request.session.get('session_key'))
#         if session_key != request.session.get('session_key'):
#             print('out')
#             # 不相符，執行相應的措施，例如強制登出
#             logout(request)
#             return redirect('login')
#
#         return view_func(request, *args, **kwargs)
#
#     return wrapped_view
