from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
from UM.Application import Application
import LayerView
class LayerViewProxy(QObject):
    def __init__(self, parent = None):
        super().__init__(parent)
        self._current_layer = 0
        self._controller = Application.getInstance().getController()
        self._controller.activeViewChanged.connect(self._onActiveViewChanged)
        self._onActiveViewChanged()
    
    currentLayerChanged = pyqtSignal()
    maxLayersChanged = pyqtSignal()
    
    @pyqtProperty(int, notify = maxLayersChanged)
    def numLayers(self):
        active_view = self._controller.getActiveView()
        #print("num max layers " , active_view.getMaxLayers())
        return active_view.getMaxLayers()
        #return 100
    
    @pyqtProperty(int, notify = currentLayerChanged)
    def currentLayer(self):
        active_view = self._controller.getActiveView()
        if type(active_view) == LayerView.LayerView.LayerView:
            return active_view.getCurrentLayer()
    
    @pyqtSlot(int)
    def setCurrentLayer(self, layer_num):
        active_view = self._controller.getActiveView()
        if type(active_view) == LayerView.LayerView.LayerView:
            active_view.setLayer(layer_num)
            
    def _onLayerChanged(self):
        self.currentLayerChanged.emit()
        
    def _onMaxLayersChanged(self):
        self.maxLayersChanged.emit()
        
    def _onActiveViewChanged(self):
        active_view = self._controller.getActiveView()
        if type(active_view) == LayerView.LayerView.LayerView:
            active_view.currentLayerNumChanged.connect(self._onLayerChanged)
            active_view.maxLayersChanged.connect(self._onMaxLayersChanged)