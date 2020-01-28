from kivy.app import App
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_string('''
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

<CustButton@Button+Label>
    color: (0, 0, 0, 1)
    background_color:(1 , 1, 1, 1)
    background_normal: ''
    #on_release: app.remove_rem()
''')

class UserData(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [{'text': "Reminder \nEasy Money", 'size_hint_x': 1} for x in range(20)] 
        
        
class UserDataApp(App):
    def build(self):
        return UserData()
    
    def remove_rem(self):
        print("test")
    
if __name__=="__main__":
    UserDataApp().run()