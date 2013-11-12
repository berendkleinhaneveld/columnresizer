"""
ColumnResizer

Python port of the C++ code.
For use with PySide.
Only supports grid layouts.

Copyright 2011 Aurelien Gateau <agateau@kde.org>
License: LGPL v2.1 or later (see COPYING)

:Authors:
	Berend Klein Haneveld
"""
from PySide.QtGui import QGridLayout
from PySide.QtCore import QObject
from PySide.QtCore import QEvent
from PySide.QtCore import QTimer
from PySide.QtCore import Slot


class ColumnResizer(QObject):
	def __init__(self):
		super(ColumnResizer, self).__init__()

		self._widgets = []
		self._gridColumnInfoList = []
		self._updateTimer = QTimer(self)
		self._updateTimer.setSingleShot(True)
		self._updateTimer.setInterval(0)
		self._updateTimer.timeout.connect(self._updateWidth)

	# Public methods

	def addWidgetsFromLayout(self, layout, column):
		"""
		:type layout: QGridLayout
		:type column: int
		"""
		assert column >= 0
		if isinstance(layout, QGridLayout):
			self._addWidgetsFromGridLayout(layout, column)
		else:
			print "ColumnResizerResizer does not support layouts of type:", type(layout)

	def eventFilter(self, obj, event):
		"""
		Overrides QObject.eventFilter()
		"""
		if event.type() == QEvent.Resize:
			self._scheduleWidthUpdate()
		return False

	# Private methods

	@Slot()
	def _updateWidth(self):
		width = 0
		for widget in self._widgets:
			width = max(widget.sizeHint().width(), width)
		for info in self._gridColumnInfoList:
			info[0].setColumnMinimumWidth(info[1], width)

	def _addWidget(self, widget):
		self._widgets.append(widget)
		widget.installEventFilter(self)
		self._scheduleWidthUpdate()

	def _addWidgetsFromGridLayout(self, layout, column):
		for row in range(layout.rowCount()):
			item = layout.itemAtPosition(row, column)
			if not item:
				continue
			widget = item.widget()
			if not widget:
				continue
			self._addWidget(widget)
		self._gridColumnInfoList.append([layout, column])

	def _scheduleWidthUpdate(self):
		self._updateTimer.start()
