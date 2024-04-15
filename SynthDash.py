import wx
import threading
import pyaudio
import numpy as np
from Bluetooth_manager.manager import BluetoothManager

class SynthDashboard(wx.Frame):
    """ A GUI dashboard for synthesizer and Bluetooth device management. """
    def __init__(self, parent):
        super().__init__(parent, title="Synthesizer Dashboard", size=(800, 600))
        self.bluetooth_manager = BluetoothManager()
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = None
        self.channels = 2  # Default to stereo audio
        self.init_ui()
        self.Centre()
        self.Show()

    def init_ui(self):
        """ Initialize the user interface components. """
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Audio channel control
        self.channel_ctrl = wx.SpinCtrl(panel, value='2', min=1, max=8)
        vbox.Add(self.channel_ctrl, flag=wx.EXPAND|wx.ALL, border=10)
        self.channel_ctrl.Bind(wx.EVT_SPINCTRL, self.on_channel_change)
        
        # Device list
        self.device_list = wx.ListBox(panel)
        vbox.Add(self.device_list, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)

        # Buttons for scanning and connecting
        btn_panel = wx.Panel(panel)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        scan_btn = wx.Button(btn_panel, label='Scan for Devices')
        scan_btn.Bind(wx.EVT_BUTTON, self.on_scan_devices)
        hbox.Add(scan_btn, flag=wx.RIGHT, border=5)
        
        connect_btn = wx.Button(btn_panel, label='Connect to Device')
        connect_btn.Bind(wx.EVT_BUTTON, self.on_connect_device)
        hbox.Add(connect_btn, flag=wx.RIGHT, border=5)

        stop_stream_btn = wx.Button(btn_panel, label='Stop Streaming')
        stop_stream_btn.Bind(wx.EVT_BUTTON, self.on_stop_streaming)
        hbox.Add(stop_stream_btn, flag=wx.RIGHT, border=5)

        btn_panel.SetSizer(hbox)
        vbox.Add(btn_panel, flag=wx.EXPAND|wx.ALL, border=10)
        
        # Status text
        self.status_text = wx.StaticText(panel, label="Status: Ready")
        vbox.Add(self.status_text, flag=wx.EXPAND|wx.ALL, border=10)
        
        panel.SetSizer(vbox)

    def on_channel_change(self, event):
        """ Handle changes in audio channel configuration. """
        self.channels = self.channel_ctrl.GetValue()

    def on_scan_devices(self, event):
        """ Scan for Bluetooth devices and update the device list. """
        devices = self.bluetooth_manager.discover_devices()
        self.device_list.Set(devices)
        self.update_status("Scanning complete.")

    def on_connect_device(self, event):
        """ Connect to the selected Bluetooth device. """
        selection = self.device_list.GetSelection()
        if selection != wx.NOT_FOUND:
            device_address = self.device_list.GetString(selection)
            threading.Thread(target=self.connect_device, args=(device_address,)).start()

    def connect_device(self, device_address):
        """ Threaded connection to a Bluetooth device. """
        self.update_status(f"Connecting to {device_address}...")
        try:
            self.bluetooth_manager.connect_device(device_address)
            self.update_status("Connected successfully.")
            self.start_streaming_audio(device_address)
        except Exception as e:
            self.update_status(f"Failed to connect: {str(e)}")

    def start_streaming_audio(self, device_address):
        """ Start streaming audio to a Bluetooth device. """
        def callback(in_data, frame_count, time_info, status):
            frequency = 440  # Frequency for A note
            samples = np.sin(2 * np.pi * np.linspace(0, frame_count-1, frame_count) * frequency / 44100)
            data = np.vstack([samples] * self.channels).T.flatten()
            return (data.astype(np.float32).tobytes(), pyaudio.paContinue)

        self.stream = self.pyaudio_instance.open(
            format=pyaudio.paFloat32,
            channels=self.channels,
            rate=44100,
            output=True,
            stream_callback=callback
        )
        self.stream.start_stream()

    def on_stop_streaming(self, event):
        """ Stop any active audio streaming. """
        if self.stream and self.stream.is_active():
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            self.update_status("Streaming stopped.")

    def update_status(self, status):
        """ Update the status label with new information. """
        wx.CallAfter(self.status_text.SetLabel, f"Status: {status}")

if __name__ == "__main__":
    app = wx.App(False)
    frame = SynthDashboard(None)
    app.MainLoop()

