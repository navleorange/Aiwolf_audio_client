import PySimpleGUI as sg
import configparser
from PIL import Image #Pillow
from lib import util
from audio import transcription

class GUI():
    def __init__(self, inifile:configparser.ConfigParser) -> None:
        # init PySimpleGUI key
        self.role_text = "role_text"
        self.role_image = "role_image"
        self.role_change = "role_change"    # only use test
        self.hide_button = "hide_button"
        self.comment_title = "comment_title"
        self.comments = "comments"
        self.action = "action"
        self.inform_title = "inform_title"
        self.inform = "inform"

        # init use variables
        self.width = 130        # image width
        self.height = 180       # image height
        self.comment_list = []  # user comment list
        self.inform_list = []   # game master inform list
        self.check_flag = False # True: set new message False: not set new message
        self.message = ""       # inform message
        self.role_image_png = None  # role image path
        self.hide_flag = False      # True: hide image False: appear image 

        # load ini file
        self.inifile = inifile
        self.image_path = self.inifile.get("gui","image_path")
        self.role_path = self.inifile.get("gui","role_path") + "{role:s}.png"
        self.role_resize = self.inifile.get("gui","role_path") + "{role:s}_resize.png"
        self.unidentified_path = self.inifile.get("gui","unidentified_path")

        # image path
        self.hide_image = self.image_path+"hide.png"
        self.hide_image_resize = self.image_path + "hide_resize.png"
        self.anonymous_image = self.unidentified_path + "anonymous.png"
        self.icon = self.image_path+"icon.png"
        self.icon_resize = self.image_path+"icon.ico"

        self.anonymous_selected = util.select_unidentified(unidentified_path=self.unidentified_path+"*.png")
        self.resize(image_path=self.anonymous_selected, save_path=self.anonymous_image)
        self.resize(image_path=self.hide_image, save_path=self.hide_image_resize)
        self.role_image_png = self.anonymous_image
        self.init_icon(image_path=self.icon, save_path=self.icon_resize)

        # layout settings
        self.popup_font = ("Arial",20)
        self.role_background = "#DCDCDC"
        self.inform_background = "#C0C0C0"
        self.text_color = "#FF0000"

        sg.theme("DarkBrown4")

        self.role_frame = sg.Frame(title="",
                                   layout=[ [sg.Text(key=self.role_text, text="あなたの役職\n未定",background_color=self.role_background , font=("Arial",20)), sg.Image(key=self.role_image, filename=self.role_image_png, background_color="#D3D3D3")],
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
            name = sg.popup_get_text(message="あなたの名前を入力してください！",title="名前を教えて",font=self.popup_font, icon=self.icon_resize)

        return name
    
    def get_audio_index(self) -> int:
        message, device_num = transcription.search_device()
        index = None
        while index == None or not index.isdigit() or (int(index) < 0 or device_num <= int(index)):
            index = sg.popup_get_text(message=message, title="オーディオ指定",font=self.popup_font, icon=self.icon_resize)
        
        return int(index)

    def check_confirm(self, message:str, image:str = None) -> str:
        self.message = sg.popup_ok(message,title="ゲームの情報", font=self.popup_font, image=image, icon=self.icon_resize)
        self.check_flag = True
        return self.message
    
    def update_role_image(self, role:str) -> None:
        print(type(role))
        print(role)
        print(type(self.role_path))
        print(self.role_path)
        print(type(self.role_resize))
        print(self.role_resize)
        self.resize(image_path=self.role_path.format(role=role), save_path=self.role_resize.format(role=role))
        self.role_image_png = self.role_resize.format(role=role)

        self.window[self.role_image].update(self.role_image_png)
    
    def update_comments(self, comment:str) -> None:
        # update comments history
        self.comment_list.append(comment)
        self.window[self.comments].update("".join(self.comment_list))
    
    def update_inform(self, message:str) -> None:
        # update text from game master
        self.inform_list.append(message)
        self.window[self.inform].update(message)
    
    def hide_role(self) -> None:
        if not self.hide_flag:
            self.window[self.role_text].update("あなたの役職\n" + "?????????")
            self.window[self.role_image].update(self.hide_image_resize)

            # prepare display
            self.window[self.hide_button].update(text="役職を表示する")
            self.hide_flag = not self.hide_flag
        else:
            self.window[self.role_text].update("あなたの役職\n" + "村人")
            self.window[self.role_image].update(self.role_image_png)

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