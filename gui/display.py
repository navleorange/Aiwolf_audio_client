import PySimpleGUI as sg
import configparser
from PIL import Image #Pillow

class GUI():
    def __init__(self, inifile:configparser.ConfigParser) -> None:
        self.role_text = "role_text"
        self.role_image = "role_image"
        self.hide_button = "hide_button"
        self.comment_title = "comment_title"
        self.comments = "comments"
        self.hide_flag = False
        self.comment_list = []
        self.inifile = inifile
        self.image_path = self.inifile.get("gui","image_path")

        sg.theme("DarkBrown4")
        #TealMono
        #GreenTan

        self.role_background = "#DCDCDC"
        self.role_frame = sg.Frame(title="",
                                   layout=[ [sg.Text(key=self.role_text, text="あなたの役職\n未定",background_color=self.role_background , font=("Arial",20)), sg.Image(key=self.role_image, filename=self.inifile.get("gui","image_path") + "my_role.png")],
                                   [sg.Button(key=self.hide_button, button_text="役職を隠す", pad=((210,0),(0,0)), size=(9,2))]
                                   ],
                            background_color=self.role_background,
                            relief=sg.RELIEF_SUNKEN
                            )
        self.comment_frame = sg.Frame(title="",
                                      layout=[ [sg.Text(key=self.comment_title, text="あなたの発言履歴",font=("Arial",20)) ],
                                       [sg.Multiline(key=self.comments, default_text="", text_color="#FF0000", disabled=True ,size=(45,30), font=("Arial",20), background_color="#C0C0C0")]
                                       ],
                            element_justification="center",
                            relief=sg.RELIEF_SUNKEN
                            )


        self.layout = [
            [self.role_frame, self.comment_frame],
            [sg.Button('Exit', size=(8,2))]
        ]
    
    def open_window(self) -> None:
        self.window = sg.Window("人狼ゲーム",self.layout,size=(1000,500) ,resizable=True, finalize=True, icon=self.image_path + "icon.png")
    
    def update_role(self) -> None:
        self.window[self.role_text].update("あなたの役職\n" + "村人")
    
    def add_comments(self, comment:str) -> None:
        self.comment_list.append(comment)
        self.window[self.comments].update("".join(self.comment_list))
    
    def hide_role(self) -> None:
        # hide

        if not self.hide_flag:
            self.window[self.role_text].update("あなたの役職\n" + "?????????")
            self.window[self.role_image].update(self.inifile.get("gui","image_path") + "rhide.png")

            # prepare display
            self.window[self.hide_button].update(text="役職を表示する")
            self.hide_flag = not self.hide_flag
        else:
            self.window[self.role_text].update("あなたの役職\n" + "村人")
            self.window[self.role_image].update(self.inifile.get("gui","image_path") + "my_role.png")

            # prepare hide
            self.window[self.hide_button].update(text="役職を隠す")
            self.hide_flag = not self.hide_flag

    def read(self):
        return self.window.read()
    
    def close_window(self) -> None:
        self.window.close()

    def resize(self) -> None:
        img = Image.open(self.inifile.get("gui","image_path") + "villager.png")

        (width, height) = (img.width//10, img.height//10)
        
        img_resized = img.resize((width, height))
        img_resized.save(self.inifile.get("gui","image_path") + "my_role.png")


        img = Image.open(self.inifile.get("gui","image_path") + "hide.png")
        
        img_resized = img.resize((width, height))
        img_resized.save(self.inifile.get("gui","image_path") + "rhide.png")