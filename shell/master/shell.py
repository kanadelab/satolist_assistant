# coding: utf-8

import codecs
import os
import shell_settings as settings

class SurfaceData:
	def __init__(self, id = 0, is_append = False):
		self.collision = None
		self.animation = {}
		self.element = None
		self.id = id
		self.is_append = is_append
		self.direct = []

		self.satolist_offset_x = None
		self.satolist_offset_y = None
		self.satolist_expand_x = None
		self.satolist_expand_y = None
		self.satolist_viewer_visible = None
		self.satolist_palette_visible = None
		self.satolist_bind_scope = None
		self.satolist_animation_default = {}

	def AddCollisionArray(self, st_x, st_y, en_x, en_y, id ):
		if self.collision == None:
			self.collision = []

		ret = CollisionData()
		ret.type = "rect"
		ret.id = id
		ret.points = [st_x, st_y, en_x, en_y]
		self.collision.append(ret)
		return self

	def AddCollisionArrayEx(self, id, collision_type, *points):
		if self.collision == None:
			self.collision = []

		ret = CollisionData()
		ret.type = collision_type
		ret.points = points
		ret.id = id
		self.collision.append(ret)
		return self

	def AddElementArray(self, file, x = 0, y = 0, method = "overlay" ):
		if self.element == None:
			self.element = []

		ret = ElementData()
		ret.method = method
		ret.file = file
		ret.x = x
		ret.y = y
		self.element.append(ret)
		return self

	def AddElement(self, id, file, x = 0, y = 0, method = "overlay" ):
		if self.element == None:
			self.element = {}

		ret = ElementData()
		ret.method = method
		ret.file = file
		ret.x = x
		ret.y = y
		self.element[id] = ret
		return self

	def AddAnimation(self, num, interval, arg = None):
		ret = AnimationData()
		ret.interval = interval
		ret.interval_arg = arg
		self.animation[num] = ret
		return ret

	def SetSatolistOffset(self, x, y):
		self.satolist_offset_x = x
		self.satolist_offset_y = y
	
	def SetSatolistExpand(self, x, y):
		self.satolist_expand_x = x
		self.satolist_expand_y = y

	def SetSatolistViewerVisible(self, visible):
		self.satolist_viewer_visible = visible
	
	def SetSatolistPaletteVisible(self, visible):
		self.satolist_palette_visible = visible

	def SetSatolistVisible(self, visible):
		self.satolist_palette_visible = visible
		self.satolist_viewer_visible = visible
	
	def SetSatolistBindScope(self, scope):
		self.satolist_bind_scope = scope

	def SetSatolistAnimationDefault(self, anim_id, pat_id):
		self.satolist_animation_default[anim_id] = pat_id
	

class CollisionData:
	def __init__(self):
		self.id = ""
		self.type = "rect"
		self.points = []

class AnimationPatternData:
	def __init__(self):
		self.method = "overlay"
		self.id = 0
		self.wait = None
		self.x = None
		self.y = None



class AnimationData:
	def __init__(self):
		self.interval = "sometimes"
		self.interval_arg = None
		self.pattern = []
		self.collision = {}

	#overlayとか用、省略時は0
	def AddPattern(self, method, id, wait = 0, x = 0, y = 0):
		pat = AnimationPatternData()
		pat.method = method
		pat.id = id
		pat.wait = wait
		pat.x = x
		pat.y = y
		self.pattern.append(pat)
		return self

	#stopとか用、省略時は出力せず
	def AddPatternEx(self, method, id, wait = None, x = None, y = None):
		pat = AnimationPatternData()
		pat.method = method
		pat.id = id
		pat.wait = wait
		pat.x = x
		pat.y = y
		self.pattern.append(pat)
		return self

	def AddCollision(self, st_x, st_y, en_x, en_y, id):
		col = CollisionData()
		col.type = "rect"
		col.id = id
		col.points = [st_x, st_y, en_x, en_y]
		self.collision.append(col)
		return self
	
	def AddCollisionEx(self, id, collision_type, *points):
		col = CollisionData()
		col.type = collision_type
		col.id = id
		col.points = points
		self.collision.append(col)
		return self

	def AddCollisionExRect(self, id, st_x, st_y, en_x, en_y):
		return self.AddCollisionEx(id, "rect", st_x, st_y, en_x, en_y)

class ElementData:
	def __init__(self ):
		self.method = "overlay"
		self.x = 0
		self.y = 0
		self.file = "surfac0.png"


class ShellData:
	def __init__(self):
		self.surfaces = [] 
		self.direct = []
		self.satolist_offset_x = None
		self.satolist_offset_y = None
		self.satolist_frame_w = None
		self.satolist_frame_h = None
		self.satolist_expand_x = None
		self.satolist_expand_y = None
		self.satolist_viewer_visible = None
		self.satolist_palette_visible = None
		self.auto_extension = ".png"

	def AddSurface(self, id = 0, is_append = False):
		s = SurfaceData(id, is_append)
		self.surfaces.append(s)
		return s

	def SetSatolistOffset(self, x, y):
		self.satolist_offset_x = x
		self.satolist_offset_y = y
	
	def SetSatolistExpand(self, x, y):
		self.satolist_expand_x = x
		self.satolist_expand_y = y

	def SetSatolistFrameSize(self, w, h):
		self.satolist_frame_w = w
		self.satolist_frame_h = h

	def SetSatolistViewerVisible(self, visible):
		self.satolist_viewer_visible = visible
	
	def SetSatolistPaletteVisible(self, visible):
		self.satolist_palette_visible = visible

	def SetSatolistVisible(self, visible):
		self.satolist_palette_visible = visible
		self.satolist_viewer_visible = visible

	def Generate(self, file):
		lines = []
		lines.append("charset,Shift_JIS")

		for d in self.direct:
			lines.append(d)

		if self.satolist_offset_x != None and self.satolist_offset_y != None:
			lines.append("//satolist.palette.offset,%s,%s" % (str(self.satolist_offset_x), str(self.satolist_offset_y)))

		if self.satolist_expand_x != None and self.satolist_expand_y != None:
			lines.append("//satolist.palette.expand,%s,%s" % (str(self.satolist_expand_y), str(self.satolist_expand_y)))

		if self.satolist_frame_w != None and self.satolist_frame_h != None:			
			lines.append("//satolist.palette.frame,%s,%s" % (str(self.satolist_frame_w), str(self.satolist_frame_h)) )

		if self.satolist_viewer_visible != None:
			if self.satolist_viewer_visible:
				lines.append("//satolist.viewer.visible,1")
			else:
				lines.append("//satolist.viewer.visible,0")

		if self.satolist_palette_visible != None:
			if self.satolist_palette_visible:
				lines.append("//satolist.palette.visible,1")
			else:
				lines.append("//satolist.palette.visible,0")

		lines.append("descript")
		lines.append("{")
		lines.append("version,1")
		lines.append("}")

		for s in self.surfaces:
			if s.is_append:
				lines.append("surface.append" + str(s.id))
			else:
				lines.append("surface" + str(s.id))
			lines.append("{")

			#element
			if isinstance(s.element, list):
				count = 0
				for v in s.element:
					lines.append("element%s,%s,%s,%s,%s" % (str(count), str(v.method), str(v.file) + self.auto_extension, str(v.x), str(v.y) ) )
					count = count + 1
			elif isinstance(s.element, dict):
				for k, v in s.element.items():
					lines.append("element%s,%s,%s,%s,%s" % (str(k), str(v.method), str(v.file) + self.auto_extension, str(v.x), str(v.y) ) )
			
			#animation
			for k, v in s.animation.items():
				if v.interval_arg == None:
					lines.append("animation%s.interval,%s" % (str(k), str(v.interval) ) )
				else:
					lines.append("animation%s.interval,%s,%s" % (str(k), str(v.interval), str(v.interval_arg)))

				count = 0
				for p in v.pattern:
					l = "animation%s.pattern%s,%s,%s" % (str(k), str(count), str(p.method), str(p.id))
					if(p.wait != None):
						l = l + (",%s" % (str(p.wait)))
					if(p.x != None):
						l = l + (",%s" % (str(p.x)))
					if(p.y != None):
						l = l + (",%s" % (str(p.y)))
					lines.append(l)
					count = count + 1

			#collision
			if isinstance(s.collision, list) and s.collision != None:
				count = 0
				for c in s.collision:
					lines.append("collisionex%s,%s,%s,%s" % (str(count), str(c.id), str(c.type), ",".join([str(pt) for pt in c.points ])))
					count = count + 1
			elif isinstance(s.collision, dict) and s.collision != None:
				for k, c in s.collision.items():
					lines.append("collisionex%s,%s,%s,%s" % (str(k), str(c.id), str(c.type), ",".join([str(pt) for pt in c.points ]) ))

			#satolist
			if s.satolist_offset_x != None and s.satolist_offset_y != None:
				lines.append("//satolist.palette.offset,%s,%s" % (str(s.satolist_offset_x), str(s.satolist_offset_y)))

			if s.satolist_expand_x != None and s.satolist_expand_y != None:
				lines.append("//satolist.palette.expand,%s,%s" % (str(s.satolist_expand_y), str(s.satolist_expand_y)))

			if s.satolist_bind_scope != None:
				lines.append("//satolist.scope,%s" % (str(s.satolist_bind_scope)) )

			if s.satolist_viewer_visible != None:
				if s.satolist_viewer_visible:
					lines.append("//satolist.viewer.visible,1")
				else:
					lines.append("//satolist.viewer.visible,0")

			if s.satolist_palette_visible != None:
				if s.satolist_palette_visible:
					lines.append("//satolist.palette.visible,1")
				else:
					lines.append("//satolist.palette.visible,0")

			for k, v in s.satolist_animation_default.items():
				lines.append("//satolist.surface.default,%s,%s" %( str(k), str(v)) )

			#direct
			for d in s.direct:
				lines.append(d)


			lines.append("}")


		f = codecs.open(file, "w", "shift_jis")
		for l in lines:
			f.write(l + '\r\n')




def Element(file, x = 0, y = 0, method = "overlay"):
	ret = ElementData()
	ret.method = method
	ret.file = file
	ret.x = x
	ret.y = y
	return ret

def Animation(interval, arg = None):
	ret = AnimationData()
	ret.interval = interval
	ret.interval_arg = arg
	return ret

def Collision(st_x, st_y, en_x, en_y, id ):
	ret = CollisionData()
	ret.type = "rect"
	ret.id = id
	ret.points = [st_x, st_y, en_x, en_y]
	return ret

def CollisionEx(id, collision_type, *points):
	ret = CollisionData()
	ret.type = collision_type
	ret.points = points
	ret.id = id
	return ret


#ここからメイン。これより上は切り離してもつかえるつもりで
if __name__ == "__main__":
	shell = ShellData()
	shell.SetSatolistOffset(130, 130)
	shell.SetSatolistVisible(False)

	#定数
	EYE_NORMAL = 10000				#通常
	EYE_CLOSE = 10001				#閉じ
	EYE_BIG = 10002					#見開き
	EYE_BIG_ST = 10003				#見開き強
	EYE_SMALL = 10004				#閉じかけ
	EYE_SMILE = 10005				#笑み	
	EYE_SUP = 10006					#驚愕
	EYE_ZITO = 10007				#ジト目
	EYE_LIGHT = 10008				#発光

	MAYU_NORMAL = 20000				#通常
	MAYU_ANG = 20001				#怒り
	MAYU_TR = 20002					#困り	
	MAYU_TRUP = 20003				#困り上
	MAYU_UPHIGH = 20004				#上強
	MAYU_UPLOW = 20005				#上弱

	MOUTH_NORMAL = 30000			#通常
	MOUTH_AKIRE = 30001				#呆れ
	MOUTH_CLOSE = 30002				#閉じ
	MOUTH_CLOSEMUSUBI = 30003		#閉じ結び
	MOUTH_CLOSESMALL = 30004		#閉じ小
	MOUTH_CRAMP = 30005				#引きつり
	MOUTH_E = 30006					#え
	MOUTH_OPENBIG = 30007			#開強
	MOUTH_OPENSMALL = 30008			#開弱
	MOUTH_OPENSMALL2 = 30009		#開微
	MOUTH_SMILE = 30010				#笑み
	MOUTH_SMILEBITTER = 30011		#苦笑
	MOUTH_SMILELOW = 30012			#笑み弱
	MOUTH_SUP = 30013				#驚き
	MOUTH_OPEN = 30014
	MOUTH_OPENLOW = 30015

	OTHER_CHEEK1 = 40000			#頬染1
	OTHER_CHEEK2 = 40001			#頬染2
	OTHER_EAR_FOX = 40002			#きつねみみ
	OTHER_EAR_CAT = 40003			#ねこみみ
	OTHER_EAR_RABBIT = 40004		#うさぎみみ
	OTHER_TAIL_FOX = 40005			#きつねしっぽ
	OTHER_SATOLIST = 40006


	def AddBaseEye(s, id, file):
		surface = s.AddSurface(id)
		if os.path.isfile(settings.EYE_DIR + "/" + file + ".png"):
			surface.AddElementArray(settings.EYE_DIR + "/" + file)
		else:
			surface.AddElementArray("eye/" + file)
		#surface.AddElementArray("eye_l/" + file)

	def AddBaseMayu(s, id, file):
		surface = s.AddSurface(id)
		if os.path.isfile(settings.MAYU_DIR + "/" + file + ".png"):
			surface.AddElementArray(settings.MAYU_DIR + "/" + file)
		else:
			surface.AddElementArray("mayu/" + file)

	def AddBaseMouth(s, id, file):
		surface = s.AddSurface(id)
		surface.AddElementArray("mouth/" + file)

	def AddBaseOther(s, id, file):
		surface = s.AddSurface(id)
		surface.AddElementArray("other/" + file)

	def AddSingleLayerAnimation(surface, id, image):
		animation = surface.AddAnimation(id, "runonce")
		animation.AddPattern("overlay", image)
		surface.SetSatolistAnimationDefault(id, 0)


	#ダミー
	surface = shell.AddSurface(10)
	surface.AddElementArray("dummy")

	#素材系
	eye_template = (
		(EYE_NORMAL, "normal"),
		(EYE_CLOSE, "close"),
		(EYE_BIG, "big"),
		(EYE_BIG_ST, "big_st"),
		(EYE_SMALL, "small"),
		(EYE_SMILE, "smile"),
		(EYE_SUP, "sup"),
		(EYE_ZITO, "zito"),
		(EYE_LIGHT, "normal_light")
	)

	mayu_template = (
		(MAYU_NORMAL, "normal"),
		(MAYU_ANG, "ang"),
		(MAYU_TR, "tr"),
		(MAYU_TRUP, "tr_up"),
		(MAYU_UPHIGH, "up_high"),
		(MAYU_UPLOW, "up_low")
	)

	mouth_template = (
		(MOUTH_NORMAL, "normal"),
		(MOUTH_AKIRE, "akire"),
		(MOUTH_CLOSE, "close"),
		(MOUTH_CLOSEMUSUBI, "close_musubi"),
		(MOUTH_CLOSESMALL, "close_small"),
		(MOUTH_CRAMP, "cramp"),
		(MOUTH_E, "e"),
		(MOUTH_OPENBIG, "open_big"),
		(MOUTH_OPENSMALL, "open_small"),
		(MOUTH_OPENSMALL2, "open_small2"),
		(MOUTH_SMILE, "smile"),
		(MOUTH_SMILEBITTER, "smile_bitter"),
		(MOUTH_SMILELOW, "smile_low"),
		(MOUTH_SUP, "sup"),
		(MOUTH_OPEN, "open"),
		(MOUTH_OPENLOW, "openlow")
	)

	#うれしそうに話す、があると良いのかも？
	lipsync_normal = (MOUTH_NORMAL, MOUTH_OPEN)
	lipsync_low = (MOUTH_CLOSESMALL, MOUTH_OPENLOW)
	lipsync_big = (MOUTH_NORMAL, MOUTH_OPENBIG)
	#lipsync_big = (MOUTH_OPENBIG, MOUTH_OPENBIG)


	def AddBrink(surface, eye_open = EYE_NORMAL, eye_half1 = EYE_SMALL, eye_half2 = EYE_SMALL, eye_close = EYE_CLOSE):
		animation = surface.AddAnimation(100, "runonce")
		animation.AddPattern("overlay", eye_open, 0, 0)

		animation = surface.AddAnimation(101, "sometimes")
		animation.AddPatternEx("stop", 100)
		animation.AddPattern("overlay", eye_open, 0)
		animation.AddPattern("overlay", eye_half1, 50)
		animation.AddPattern("overlay", eye_close, 50)
		animation.AddPattern("overlay", eye_half1, 50)
		animation.AddPattern("overlay", eye_open, 50)

		surface.SetSatolistAnimationDefault(100, 0)

	def AddLipSync(surface, mouth_close = MOUTH_NORMAL, mouth_open = MOUTH_OPENLOW):
		animation = surface.AddAnimation(200, "runonce")
		animation.AddPattern("overlay", mouth_close)
		
		animation = surface.AddAnimation(201, "bind+talk", 1)
		animation.AddPatternEx("stop", 200)
		animation.AddPattern("overlay", mouth_close, 0)
		animation.AddPattern("overlay", mouth_open, 100)
		animation.AddPattern("overlay", mouth_close, 100)

		animation = surface.AddAnimation(202, "bind")
		animation.AddPatternEx("stop", 200)
		animation.AddPattern("overlay", mouth_open)

		animation = surface.AddAnimation(203, "bind")
		animation.AddPatternEx("stop", 200)
		animation.AddPattern("overlay", mouth_close)

		surface.SetSatolistAnimationDefault(200, 0)

	def AddLipSyncSet(surface, surface_set):
		AddLipSync(surface, surface_set[0], surface_set[1])
	
	def AddMayu(surface, mayu_id = MAYU_NORMAL):
		AddSingleLayerAnimation(surface, 300, mayu_id)

	def AddEye(surface, eye_id):
		AddSingleLayerAnimation(surface, 100, eye_id)

	def AddMouth(surface, mouth_id):
		AddSingleLayerAnimation(surface, 200, mouth_id)

	def AddCheek(surface, cheek_level):
		if cheek_level == 1:
			AddSingleLayerAnimation(surface, 80, OTHER_CHEEK1)
		elif cheek_level == 2:
			AddSingleLayerAnimation(surface, 80, OTHER_CHEEK2)


	#各ベース表情追加
	for i in eye_template:
		AddBaseEye(shell, i[0], i[1])
	for i in mayu_template:
		AddBaseMayu(shell, i[0], i[1])
	for i in mouth_template:
		AddBaseMouth(shell, i[0], i[1])
	
	AddBaseOther(shell, OTHER_CHEEK1, "cheek1")
	AddBaseOther(shell, OTHER_CHEEK2, "cheek2")
	AddBaseOther(shell, OTHER_TAIL_FOX, "fox_tail")

	#立ち絵
	s = shell.AddSurface("0-27, !10")
	s.AddElement(0, "body/body1")
	#きつねみみもたしておく
	s.AddElement(1, "other/ear_fox")
	#めがね
	#s.AddElement(2, "other/glasses")
	#しっぽはinterpolate合成で一番うしろにみえるようにする
	s.AddElement(3, "other/satolist")
	anim = s.AddAnimation(400, "runonce")
	anim.AddPattern("interpolate", OTHER_TAIL_FOX )

	#コリジョン
	s.AddCollisionArrayEx("bust", "rect", 119,247,224,315)
	s.AddCollisionArrayEx("head", "rect", 119,97,237,138)
	s.AddCollisionArrayEx("leg", "rect", 127,482,239,599)

	#きせかえの追加

	#頬1
	bind = s.AddAnimation(410, "never")
	bind.AddPattern("overlay", OTHER_CHEEK1)
	bind.AddPatternEx("stop", 420)

	#頬2
	bind = s.AddAnimation(420, "never")
	bind.AddPattern("overlay", OTHER_CHEEK2)
	bind.AddPatternEx("stop", 410)
	

	#通常
	s = shell.AddSurface("0")
	AddBrink(s, EYE_NORMAL)
	AddLipSyncSet(s, lipsync_normal)
	AddMayu(s, MAYU_NORMAL)
	#AddCheek(s, 1)

	#1,1
	s = shell.AddSurface("1")
	AddBrink(s, EYE_NORMAL)
	if settings.SHELL_MODE == settings.MODE_EX1:
		AddLipSync(s, MOUTH_E)
	else:
		AddLipSync(s, MOUTH_NORMAL, MOUTH_SUP)
	AddMayu(s, MAYU_UPLOW)

	#1,2
	s = shell.AddSurface("2")
	AddEye(s, EYE_SUP)
	AddLipSync(s, MOUTH_NORMAL, MOUTH_OPENBIG)
	AddMayu(s, MAYU_UPHIGH)

	#1,3
	s = shell.AddSurface("3")
	AddBrink(s, EYE_ZITO)
	AddLipSync(s, MOUTH_E)
	AddMayu(s, MAYU_TR)

	#1,5
	s = shell.AddSurface("4")
	AddEye(s, EYE_SMILE)
	#AddLipSync(s, MOUTH_NORMAL, MOUTH_SMILE)
	AddLipSync(s, MOUTH_NORMAL, MOUTH_OPEN)
	AddMayu(s, MAYU_UPHIGH)

	#1,6
	s = shell.AddSurface("5")
	AddEye(s, EYE_CLOSE)
	AddLipSync(s, MOUTH_NORMAL, MOUTH_SMILELOW)
	AddMayu(s, MAYU_NORMAL)

	#1,7
	s = shell.AddSurface("6")
	AddBrink(s)
	AddLipSync(s, MOUTH_CLOSESMALL, MOUTH_OPENSMALL)
	AddMayu(s, MAYU_ANG)

	#2,1
	s = shell.AddSurface("7")
	AddBrink(s)
	AddLipSync(s, MOUTH_NORMAL, MOUTH_SMILEBITTER)
	AddMayu(s, MAYU_TR)

	#2,2
	s = shell.AddSurface("8")
	AddBrink(s)
	AddLipSync(s, MOUTH_NORMAL, MOUTH_E)
	AddMayu(s, MAYU_ANG)

	#2,3
	s = shell.AddSurface("9")
	AddBrink(s)
	AddLipSync(s, MOUTH_CLOSE, MOUTH_OPENBIG)
	AddMayu(s)

	#2,4
	s = shell.AddSurface("11")
	AddBrink(s)
	AddLipSync(s, MOUTH_CLOSESMALL, MOUTH_OPENSMALL)
	AddMayu(s, MAYU_TR)

	#2,5
	s = shell.AddSurface("12")
	AddBrink(s)
	AddMouth(s, MOUTH_AKIRE)
	AddMayu(s,MAYU_UPLOW)

	#2,6
	s = shell.AddSurface("13")
	AddEye(s, EYE_CLOSE)
	AddLipSyncSet(s, lipsync_big)
	AddMayu(s, MAYU_TR)

	#2,7
	s = shell.AddSurface("14")
	AddEye(s, EYE_SMILE)
	AddLipSync(s)
	AddMayu(s, MAYU_TRUP)

	#3,1
	s = shell.AddSurface("15")
	AddEye(s, EYE_CLOSE)
	AddLipSync(s)
	AddMayu(s)

	#3,2
	s = shell.AddSurface("16")
	AddBrink(s, EYE_ZITO, EYE_SMALL)
	AddLipSync(s, MOUTH_CLOSESMALL, MOUTH_OPENSMALL)
	AddMayu(s, MAYU_ANG)

	#3,3
	s = shell.AddSurface("17")
	AddBrink(s, EYE_ZITO, EYE_SMALL)
	AddLipSync(s, MOUTH_NORMAL, MOUTH_CRAMP)
	AddMayu(s, MAYU_TR)

	#3,4
	s = shell.AddSurface("18")
	AddBrink(s, EYE_ZITO, EYE_SMALL)
	AddLipSync(s, MOUTH_CLOSESMALL, MOUTH_E)
	AddMayu(s, MAYU_ANG)

	#3,5
	s = shell.AddSurface("19")
	AddBrink(s, EYE_ZITO, EYE_SMALL)
	AddLipSync(s, MOUTH_CLOSESMALL, MOUTH_OPENSMALL2)
	AddMayu(s)

	#3,6
	s = shell.AddSurface("20")
	AddBrink(s)
	AddLipSync(s, MOUTH_NORMAL, MOUTH_OPENBIG)
	AddMayu(s, MAYU_ANG)

	#3,7
	s = shell.AddSurface("21")
	AddEye(s, EYE_CLOSE)
	AddLipSync(s, MOUTH_NORMAL, MOUTH_SMILELOW)
	AddMayu(s, MAYU_TR)

	#4,5
	#s = shell.AddSurface("22")
	#AddEye

	#4,6
	s = shell.AddSurface("23")
	AddEye(s, EYE_SUP)
	AddMouth(s, MOUTH_SUP)
	AddMayu(s, MAYU_ANG)

	#4,7
	s = shell.AddSurface("24")
	AddEye(s, EYE_SUP)
	AddLipSync(s, MOUTH_NORMAL, MOUTH_SUP)
	AddMayu(s, MAYU_ANG)

	#5,2
	s = shell.AddSurface("25")
	AddBrink(s)
	AddMouth(s, MOUTH_CLOSEMUSUBI)
	AddMayu(s, MAYU_TR)

	#5,4

	#5,6
	s = shell.AddSurface("26")
	AddBrink(s, EYE_ZITO, EYE_SMALL)
	AddLipSync(s)
	AddMayu(s,MAYU_TR)


	#通常
	s = shell.AddSurface("27")
	AddEye(s, EYE_LIGHT)
	AddLipSyncSet(s, lipsync_normal)
	AddMayu(s, MAYU_NORMAL)
	#AddCheek(s, 1)




	surface = shell.AddSurface("0-27,!10")
	surface.SetSatolistVisible(True)
	

	shell.Generate("surfaces.txt")
	exit(0)
