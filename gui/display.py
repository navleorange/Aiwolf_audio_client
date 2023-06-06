import PySimpleGUI as sg
import configparser
from PIL import Image #Pillow
from lib import util
from audio import transcription

class GUI():
    def __init__(self, inifile:configparser.ConfigParser) -> None:
        self.role_text = "role_text"
        self.role_image = "role_image"
        self.role_change = "role_change"    # only use test
        self.hide_button = "hide_button"
        self.comment_title = "comment_title"
        self.comments = "comments"
        self.action = "action"
        self.inform_title = "inform_title"
        self.inform = "inform"
        self.hide_flag = False

        self.comment_list = []
        self.inform_list = []

        self.inifile = inifile
        self.image_path = self.inifile.get("gui","image_path")
        self.role_path = self.inifile.get("gui","role_path")
        self.unidentified_path = self.inifile.get("gui","unidentified_path")

        self.width = 130
        self.height = 180

        sg.theme("DarkBrown4")
        #TealMono
        #GreenTan

        anonymous = util.select_unidentified(unidentified_path=self.unidentified_path+"*.png")
        self.resize(image_path=anonymous, save_path=self.unidentified_path + "use.png")
        self.init_icon(image_path=self.image_path+"icon.png", save_path=self.image_path+"icon.ico")


        self.role_background = "#DCDCDC"
        self.inform_background = "#C0C0C0"
        self.text_color = "#FF0000"

        self.role_frame = sg.Frame(title="",
                                   layout=[ [sg.Text(key=self.role_text, text="あなたの役職\n未定",background_color=self.role_background , font=("Arial",20)), sg.Image(key=self.role_image, filename=self.unidentified_path + "use.png", background_color="#D3D3D3")],
                                   [sg.Button(key=self.hide_button, button_text="役職を隠す", pad=((210,0),(0,0)), size=(9,2))],
                                   [sg.Text(key=self.action, text="現在の行動：",font=("Arial",20), background_color=self.role_background)],
                                   ],
                            pad=((80,0),(0,0)),
                            background_color=self.role_background,
                            relief=sg.RELIEF_SUNKEN
                            )
        self.comment_frame = sg.Frame(title="",
                                      layout=[ [sg.Text(key=self.comment_title, text="あなたの発言履歴",font=("Arial",20)) ],
                                       [sg.Multiline(key=self.comments, default_text="", text_color=self.text_color, disabled=True ,size=(40,20), font=("Arial",20), background_color=self.inform_background)]
                                       ],
                            element_justification="center",
                            relief=sg.RELIEF_SUNKEN
                            )
        self.gamemaster_frame = sg.Frame(title="",
                                         layout=[
                                             [sg.Text(key=self.inform_title, text="ゲームマスターからのお知らせ",font=("Arial",20))],
                                             [sg.Multiline(key=self.inform, default_text="",text_color=self.text_color,font=("Arial",20),size=(28,20),background_color=self.inform_background)]
                                         ],
                                         element_justification="center",
                                         relief=sg.RELIEF_SUNKEN
                                    )
        
        self.left_column = sg.Column([
            [self.role_frame],
            [self.gamemaster_frame]
        ])
        self.right_column = sg.Column([
            [self.comment_frame]
        ])

        self.game_column = sg.Column([
            [self.left_column, self.right_column]
        ])
        
        self.layout = [
            [self.game_column]
        ]
    
    def open_window(self) -> None:
        self.window = sg.Window("人狼ゲーム",self.layout,size=(1000,600) ,resizable=True, finalize=True, icon=self.image_path + "icon.ico")
    
    def get_name(self) -> str:
        name = None
        while name == None or name == "":
            name = sg.popup_get_text(message="あなたの名前を入力してください！",title="名前を教えて",font=("Arial",20))

        return name
    
    def get_audio_index(self) -> int:
        message, device_num = transcription.search_device()
        index = None
        while index == None or not index.isdigit() or (int(index) < 0 or device_num <= int(index)):
            index = sg.popup_get_text(message=message, title="オーディオ指定",font=("Arial",20))
        
        return int(index)
    
    def update_role_image(self) -> None:
        anonymous = util.select_unidentified(unidentified_path=self.unidentified_path+"*.png")
        self.resize(image_path=anonymous, save_path=self.unidentified_path + "use.png")
        self.window[self.role_image].update(self.unidentified_path + "use.png")
    
    def update_comments(self, comment:str) -> None:
        self.comment_list.append(comment)
        self.window[self.comments].update("".join(self.comment_list))
    
    def update_inform(self, message:str) -> None:
        self.inform_list.append(message)
        print(self.inform_list)
        self.window[self.inform].update("".join(self.inform_list))
    
    def hide_role(self) -> None:
        # hide

        if not self.hide_flag:
            self.window[self.role_text].update("あなたの役職\n" + "?????????")
            self.window[self.role_image].update(self.image_path + "rhide.png")

            # prepare display
            self.window[self.hide_button].update(text="役職を表示する")
            self.hide_flag = not self.hide_flag
        else:
            self.window[self.role_text].update("あなたの役職\n" + "村人")
            self.window[self.role_image].update(self.image_path + "my_role.png")

            # prepare hide
            self.window[self.hide_button].update(text="役職を隠す")
            self.hide_flag = not self.hide_flag

    def read(self):
        return self.window.read()
    
    def close_window(self) -> None:
        self.window.close()

    def unidentified_resize(self, image_path:str, save_path:str) -> None:
        self.resize(image_path=image_path, save_path=save_path, w=15)

    def resize(self, image_path:str, save_path:str) -> None:
        img = Image.open(image_path)

        # (width, height) = (img.width//10, img.height//10)

        img_resized = img.resize((self.width, self.height))
        img_resized.save(save_path)
    
    def init_icon(self, image_path:str, save_path:str) -> None:
        img = Image.open(image_path)
        img.save(save_path, format="ICO", sizez=[(256,256)])
    
    def finish(self) -> None:
        self.close_window()