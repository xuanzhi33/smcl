import webview

class Api:
    def __init__(self, window) -> None:
        self.window = window
    def test(self):
        print('test')
    def change_title(self, title):
        self.window.title = title

window = webview.create_window('Simple browser', './gui/main.html')
api = Api(window)
webview.start(debug=True)
