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
    def __init__(self, data ='', flag = -1, num = 0, **kwargs):
        super().__init__(**kwargs)
        if flag == 0:
            self.data = [{'text': data[3*x] + '\n' + data[3*x+1] + '\n' + data[3*x+2], 'size_hint_x': 1} for x in range(num)] 
        if flag == 1:
            self.data = [{'text': data[4*x] + '\n' + data[4*x+1] + '\n' + data[4*x+2] + '\n' + data[4*x+3], 'size_hint_x': 1} for x in range(num)]
            
        print(data[0])
        print(num)
        
class UserDataApp(App):
    def build(self):
        return UserData()
    
    def remove_rem(self):
        print("test")
    
if __name__=="__main__":
    UserDataApp().run()