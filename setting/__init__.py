def get_setting(debug):
    if debug:
        return {
            "url_prefix": "http://127.0.0.1:5000" 
        }
    else:
        return {
            "url_prefix": "https:/XXXXXXXXX.a.run.app"
        }