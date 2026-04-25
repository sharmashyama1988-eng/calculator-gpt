const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('electronAPI', {
  sendAIRequest: (data) => ipcRenderer.invoke('ai-complete', data),
  onAIStream: (callback) => ipcRenderer.on('ai-stream-data', (event, value) => {
    callback(value);
  }),
  removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel)
});
