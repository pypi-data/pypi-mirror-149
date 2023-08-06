import sys

def main():
    from threading import Thread
    from .klink import run
    from thonny.web_conn import Webtty

    from flask import Flask,send_from_directory,abort,make_response

    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    sysout = sys.stdout
    app = Flask(__name__)
    sockets = Webtty()
    

    def after_request(resp):
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Private-Network'] = "true"
        return resp

    app.after_request(after_request)
    run(app, sockets, '/hardware')

    appPing = Flask(__name__)
    def ping():
        return '''{"data": {"auto": true}}'''
    appPing.add_url_rule('/ping', 'ping', ping)
    appPing.after_request(after_request)

    wsTh = Thread(target=sockets.listen, )
    wsTh.start()
    
    pingServer = pywsgi.WSGIServer(('0.0.0.0', 55820), appPing)
    print("web server start ... ")
    pingServer.serve_forever()



if __name__ == "__main__":
    main()
    
    


