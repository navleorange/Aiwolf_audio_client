# あんまり良い方法が思い浮かばなかったので、とりあえず...
import pyaudio

format = pyaudio.paInt16

class Role():
	def __init__(self) -> None:
		# init role name
		self.villager = "villager"
		self.seer = "seer"
		self.medium = "medium"	# 前日に吊られた人の役職を知ることができる
		self.guard = "guard"
		self.werewolf = "werewolf"
		self.possessed = "possessed"

		self.role_list = [self.villager,self.seer,self.medium,self.guard,self.werewolf,self.possessed]
		self.role_translate = {self.villager:"村人",self.seer:"占い師",self.medium:"霊能者",self.guard:"狩人",self.werewolf:"人狼",self.possessed:"狂人"}
	
	def translate_ja(self, role:str) -> str:

		if self.role_translate.get(role,None) == None:
			raise ValueError(f"{role} is not exist role")

		return self.role_translate.get(role)

class AgentInfo:
	def __init__(self) -> None:
		self.name = "name"
		self.message = "message"
		self.human_flag = "human_flag"
		self.audio = "audio"

		self._agent_info_format = {self.name:None,self.message:None,self.human_flag:None,self.audio:None}
	
	def get_agent_info_format(self) -> dict:
		return self._agent_info_format.copy()

class GameInfo:
	def __init__(self) -> None:
		self.vote = "vote"
		self.attack = "attack"

		self._gameInfo_format = {self.vote:None,self.attack:None}
	
	def get_gameInfo_format(self) -> dict:
		return self._gameInfo_format.copy()

class Request:
	def __init__(self) -> None:
		self.transcription = "transcription" # request convert audio to text
		self.time_sync = "time_sync"	# request synchronize time
		self.convert_audio = "convert_audio"
		self.talk_end = "talk_end"

		# {key:self variable value:RandomTalkAgent send format}
		self.convert_request = {self.time_sync:"TIME_SYNCHRONIZE", self.transcription:"TRANSCRIPTION", self.convert_audio:"CONVERTAUDIO",self.talk_end:"TALKEND"}

		self._request_format = ""

	def get_request_format(self) -> str:
		return self._request_format
	
	def convert_server_format(self, request:str) -> str:

		if self.convert_request.get(request,None) == None:
			raise ValueError(f"{request} is not exist request")
		
		return self.convert_request.get(request)

class Inform:
	def __init__(self) -> None:
		self.agent_info = "agent_info"
		self.game_info = "game_info"
		self.request = "request"

		# class instance
		self.agent_info_class = AgentInfo()
		self.game_info_class = GameInfo()
		self.request_class = Request()

		self.agent_info_value = None
		self.game_info_value = None
		self.request_value = None

		self._random_inform_format = {self.agent_info:self.agent_info_value,self.game_info:self.game_info_value,self.request:self.request_value}
	
	def get_Inform_format(self) -> dict:
		return self._random_inform_format
	
	def check_agent_info_value(self) -> None:
		if self.agent_info_value == None:
			self.agent_info_value = self.agent_info_class.get_agent_info_format()
	
	def check_request_value(self) -> None:
		if self.request_value == None:
			self.request_value = self.request_class.get_request_format()
	
	def update_basic_info(self, name:str, human_flag:bool) -> None:
		self.check_agent_info_value()
		self.agent_info_value[self.agent_info_class.name] = name
		self.agent_info_value[self.agent_info_class.human_flag] = human_flag
	
	def update_message(self, message:str) -> None:
		self.check_agent_info_value()
		self.agent_info_value[self.agent_info_class.message] = message
	
	def update_audio(self, audio) -> None:
		self.check_agent_info_value()
		self.agent_info_value[self.agent_info_class.audio] = audio
	
	def update_request(self, request:str) -> None:
		self.check_request_value()
		self.request_value = self.request_class.convert_server_format(request=request)
	
	def update_inform_format(self) -> None:
		self._random_inform_format[self.agent_info] = self.agent_info_value
		self._random_inform_format[self.game_info] = self.agent_info_value
		self._random_inform_format[self.request] = self.request_value
	
	def reset_values(self) -> None:
		self.agent_info_value = None
		self.game_info_value = None
		self.request_value = None