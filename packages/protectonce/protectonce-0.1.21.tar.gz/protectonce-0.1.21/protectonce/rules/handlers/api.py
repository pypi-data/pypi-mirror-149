import os


def get_flask_routes(data):
    try:
        if not data:
            return []
        args = data.get('args', [])
        index = data['config']['argsIndex']
        if(len(args) > index):
            paths = [args[index]]
            if(not paths):
                return []
            if("/static/<path:filename>" in paths):  # skipping default path set by flask
                return []
            methods = data['kwargs'].get('methods', None)
            host = os.uname()[1]
            routeData = [{'paths': paths, 'methods': ["GET"]
                          if methods is None else methods, 'host': host}]
            return routeData
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] api.get_flask_routes failed with error {e}')
        return []


def get_flask_params(data):
    try:
        flask_server = data.get('instance', None)
        po_session_id = data.get('result', {}).get('poSessionId', None)
        if(not po_session_id or not flask_server or not hasattr(flask_server, 'jinja_env') or not hasattr(flask_server.jinja_env, 'globals')):
            return {}
        request = flask_server.jinja_env.globals['request']
        return {
            'poSessionId': po_session_id,
            'requestPath': request.url_rule.rule,
            'pathParams': request.view_args
        }
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] api.get_flask_params failed with error : {e}')
        return {}


def get_django_params(data):
    try:
        args = data.get('args', [])
        index = data['config']['argsIndex']
        if(len(args) > index and hasattr(args[index], 'resolver_match') and hasattr(args[index].resolver_match, 'route')):
            return {
                'poSessionId': data.get('result', {}).get('poSessionId', ''),
                'requestPath': args[index].resolver_match.route,
                'pathParams': data.get('kwargs', None)
            }
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] api.get_django_params failed with error : {e}')
    return {}


def get_django_routes(data):
    try:
        host = os.uname()[1]
        if not data:
            return []
        args = data.get('args', [])
        index = data['config']['argsIndex']
        if(len(args) > index + 1):
            path = args[index]
            view = args[index + 1]
            if(not hasattr(view, 'view_class')):
                return [{
                    'paths': [path],
                    'methods': [
                        "GET",
                        "POST",
                        "PUT",
                        "PATCH",
                        "DELETE",
                        "HEAD",
                        "OPTIONS",
                        "TRACE",
                    ],
                    'host': host
                }]
            methods = list(set(dir(view.view_class)) & set(
                view.view_class.http_method_names))
            return [{'paths': [path], 'methods': list(map(lambda method: method.upper(), methods)), 'host': host}]
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] api.get_django_routes failed with error : {e}')
    return []
