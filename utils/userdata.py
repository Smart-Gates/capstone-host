from kivy.app import App
from kivy.uix.recycleview import RecycleView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

Builder.load_string('''
<RemoveItem>:
    Button:
        text: "Delete Item"
        size_hint: 0.375, 0.2
        pos_hint: {"x":0.1, "y":0.1}
        
    Button:
        id: cancel
        text: "Cancel"
        size_hint: 0.375, 0.2
        pos_hint: {"x":0.525, "y":0.1}

<UserData>:
    canvas.before:
        Color:
            rgba:(1,1,1, 1)
        Rectangle:
            size: self.size
            pos: self.pos
    pos_hint: {'right': 1}
    id: main_win
    viewclass: 'CustButton'
    RecycleBoxLayout:
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'

<CustButton>
    color: (0, 0, 0, 1)
    background_color:(1 , 1, 1, 1)
    background_normal: ''
    on_release: root.remove_rem()
''')

class RemoveItem(FloatLayout):
    pass

class CustButton(Button, Label):
    def remove_rem(self):
        show = RemoveItem()
        popWin = Popup(title = "Delete Item", content = show, size_hint = (0.5, 0.5))
        show.ids.cancel.on_release = popWin.dismiss
        popWin.open()

class UserData(RecycleView):
    def __init__(self, data ='', flag = -1, num = 0, **kwargs):
        super().__init__(**kwargs)
        if flag == 0:
            self.data = [{'text': data[5*x+1] + '\n' + data[5*x+2] + '\n' + data[5*x+3], 'size_hint_x': 1} for x in range(num)] 
        if flag == 1:
            self.data = [{'text': data[7*x+1] + '\n' + data[7*x+2] + '\n' + data[7*x+3] + '\n' + data[7*x+4], 'size_hint_x': 1} for x in range(num)]
            
class UserDataApp(App):
    def build(self):
        return UserData()
    
if __name__=="__main__":
    UserDataApp().run()