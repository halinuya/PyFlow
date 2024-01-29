## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from qtpy.QtWidgets import QWidget
from qtpy.QtWidgets import QHBoxLayout
from qtpy.QtWidgets import QMenu

from PyFlow.Core.Common import *


UI_INPUT_WIDGET_PINS_FACTORIES = {}


class IInputWidget(object):
    def __init__(self,parent= None):
        super(IInputWidget, self).__init__()

    def widgetVariant(self):
        return "DefaultWidget"

    def getWidget(self):
        raise NotImplementedError("getWidget of IInputWidget is not implemented")

    def setWidget(self, widget):
        raise NotImplementedError("setWidget of IInputWidget is not implemented")

    def blockWidgetSignals(self, bLock=False):
        raise NotImplementedError(
            "blockWidgetSignals of IInputWidget is not implemented"
        )


class InputWidgetRaw(QWidget, IInputWidget):
    """
    This type of widget can be used as a base class for complex ui generated by designer
    """

    def __init__(self, parent=None, dataSetCallback=None, defaultValue=None, **kwargs):
        super(InputWidgetRaw, self).__init__(parent=parent)
        self._defaultValue = defaultValue
        # function with signature void(object)
        # this will set data to pin
        self.dataSetCallback = dataSetCallback
        self._widget = None
        self._menu = QMenu()
        self.actionReset = self._menu.addAction("ResetValue")
        self.actionReset.triggered.connect(self.onResetValue)

    def setWidgetValueNoSignals(self, pin):
        self.blockWidgetSignals(True)
        self.setWidgetValue(pin.currentData())
        self.blockWidgetSignals(False)

    def setWidget(self, widget):
        self._widget = widget

    def getWidget(self):
        assert self._widget is not None
        return self._widget

    def onResetValue(self):
        self.setWidgetValue(self._defaultValue)

    def setWidgetValue(self, value):
        """to widget"""
        pass

    def widgetValueUpdated(self, value):
        """from widget"""
        pass

    def contextMenuEvent(self, event):
        self._menu.exec_(event.globalPos())


class InputWidgetSingle(InputWidgetRaw):
    """
    This type of widget is used for a simple widgets like buttons, checkboxes etc.
    It consists of horizontal layout widget itself and reset button.
    """

    def __init__(self, parent=None, dataSetCallback=None, defaultValue=None, **kwargs):
        super(InputWidgetSingle, self).__init__(
            parent=parent,
            dataSetCallback=dataSetCallback,
            defaultValue=defaultValue,
            **kwargs,
        )
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self._index = 0
        self._widget = None
        self.senderPin = None

    def getWidget(self):
        return InputWidgetRaw.getWidget(self)

    def setWidget(self, widget):
        InputWidgetRaw.setWidget(self, widget)
        self.horizontalLayout.insertWidget(self._index, self.getWidget())


def REGISTER_UI_INPUT_WIDGET_PIN_FACTORY(packageName, factory):
    if packageName not in UI_INPUT_WIDGET_PINS_FACTORIES:
        UI_INPUT_WIDGET_PINS_FACTORIES[packageName] = factory


def createInputWidget(
    dataType,
    dataSetter,
    defaultValue=None,
    widgetVariant=DEFAULT_WIDGET_VARIANT,
    **kwargs,
):
    pinInputWidget = None
    for packageName, factory in UI_INPUT_WIDGET_PINS_FACTORIES.items():
        pinInputWidget = factory(
            dataType, dataSetter, defaultValue, widgetVariant, **kwargs
        )
        if pinInputWidget is not None:
            return pinInputWidget
    return pinInputWidget
