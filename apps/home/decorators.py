
# csv.py, 用於儲存model_name和對應呼叫的function
model_actions = {}


def register_model_action(models_name):
    def decorator(func):
        model_actions[models_name] = func
        return func
    return decorator
