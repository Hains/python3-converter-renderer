# -*- coding: utf-8 -*-
# by digiteng...05.2020, 07.2020, 
# for channellist,
# <widget source="ServiceEvent" render="xtraNextEvents" nextEvent="1" usedImage="backdrop" position="840,420" size="100,60" zPosition="5" />
# <widget source="ServiceEvent" render="xtraNextEvents" nextEvent="2" usedImage="backdrop" position="940,420" size="100,60" zPosition="5" />
# <widget source="ServiceEvent" render="xtraNextEvents" nextEvent="3" usedImage="backdrop" position="1040,420" size="100,60" zPosition="5" />
# <widget source="ServiceEvent" render="xtraNextEvents" nextEvent="4" usedImage="backdrop" position="1140,420" size="100,60" zPosition="5" />
# ...

from Renderer import Renderer
from enigma import ePixmap, ePicLoad, eTimer, eEPGCache, loadPNG
from Components.AVSwitch import AVSwitch
from Components.Pixmap import Pixmap
from ServiceReference import ServiceReference
from Components.config import config
from Tools.Directories import fileExists
import re


try:
	from Plugins.Extensions.xtraEvent.xtra import xtra
	pathLoc = config.plugins.xtraEvent.loc.value
except:
	pass


class AMB_xtraNextEvents(Renderer):

	def __init__(self):
		Renderer.__init__(self)

		self.pstrNm = ''
		self.evntNm = ''
		
		self.nxEvnt = 0
		self.nxEvntUsed = ""
		self.epgcache = eEPGCache.getInstance()

	def applySkin(self, desktop, parent):
		attribs = self.skinAttributes[:]
		for attrib, value in self.skinAttributes:
			if attrib == 'nextEvent':
				self.nxEvnt = int(value)
			elif attrib == 'usedImage':
				self.nxEvntUsed = value
			
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap
	def changed(self, what):
		try:
			if not self.instance:
				return
			if what[0] == self.CHANGED_CLEAR:
				self.instance.hide()
			if what[0] != self.CHANGED_CLEAR:
				self.delay()


		except:
			pass

	def showEvents(self):
		cevnt = ''
		pstrNm = ''
		try:
			ref = self.source.service
			events = self.epgcache.lookupEvent(['IBDCTM', (ref.toString(), 0, 1, -1)])
			if events:
				cevnt = events[self.nxEvnt][4]
			else:
				self.instance.hide()
				return
		except:
			self.instance.hide()
			return		

		try:
			evntNm = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)|!", "", cevnt).rstrip()
			pstrNm = "{}xtraEvent/{}/{}.jpg".format(pathLoc, self.nxEvntUsed, evntNm)
			if fileExists(pstrNm):	
				size = self.instance.size()
				self.picload = ePicLoad()
				sc = AVSwitch().getFramebufferScale()
				if self.picload:
					self.picload.setPara((size.width(),
					size.height(),
					sc[0],
					sc[1],
					False,
					1,
					'#00000000'))
				result = self.picload.startDecode(pstrNm, 0, 0, False)
				if result == 0:
					ptr = self.picload.getData()
					if ptr != None:
						self.instance.setPixmap(ptr)
						self.instance.show()
				del self.picload
			else:
				self.instance.hide()
				return
		except:
			self.instance.hide()
		
	def delay(self):
		self.timer = eTimer()
		self.timer.callback.append(self.showEvents)
		self.timer.start(500, True)
