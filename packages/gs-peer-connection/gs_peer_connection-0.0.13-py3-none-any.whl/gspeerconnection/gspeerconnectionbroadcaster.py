import ast
import json
import logging
import platform
from threading import Thread
from time import sleep
import socketio
from aiortc import RTCPeerConnection, RTCRtpSender, RTCConfiguration, RTCIceServer
from aiortc.contrib.media import MediaPlayer, MediaRelay
import picamera

from gspeerconnection.pitrack import PiH264Relay, PiH264CameraOutput

video_trackList = list()


class BroadcastThread(Thread):
    def __init__(self, cameraoutput):
        super(BroadcastThread, self).__init__()
        self.cameraoutput = cameraoutput

    def run(self):

        while True:
            buf = self.cameraoutput.nal_queue.get()
            if buf:
                for track in video_trackList:
                    track.write(buf)


class GSPeerConnectionBroadcaster:

    def getPiH264Relay(self):
        video_track = PiH264Relay(30)
        video_trackList.append(video_track)
        return video_track

    def force_codec(self, pc, sender, forced_codec):
        kind = forced_codec.split("/")[0]
        codecs = RTCRtpSender.getCapabilities(kind).codecs
        transceiver = next(t for t in pc.getTransceivers() if t.sender == sender)
        transceiver.setCodecPreferences(
            [codec for codec in codecs if codec.mimeType == forced_codec]
        )

    @classmethod
    async def create(cls, gsdbs):
        self = GSPeerConnectionBroadcaster()

        with picamera.PiCamera() as camera:
            self.gsdbs = gsdbs
            camera.resolution = (self.gsdbs.credentials["hres"], self.gsdbs.credentials["vres"])
            camera.framerate = self.gsdbs.credentials["framerate"]
            sleep(1)  # camera warm-up time
            target_bitrate = camera.resolution[0] * \
                             camera.resolution[1] * \
                             camera.framerate * 0.150

            cameraOutput = PiH264CameraOutput()
            broadcast_thread = BroadcastThread(cameraOutput)
            camera.start_recording(
                cameraOutput,
                format="h264",
                profile="constrained",
                bitrate=int(target_bitrate),
                inline_headers=True,
                sei=False,
            )
            broadcast_thread.start()
            self.sio = socketio.AsyncClient()
            self.peerConnections = {}
            self._logger = logging.getLogger(__name__)
            self.webcam = None
            self.relay = None

            @self.sio.event
            async def connect():
                self._logger.info('connection established')

            @self.sio.event
            async def answer(id, description):
                if type(description) == str:
                    description = ast.literal_eval(description)
                desc = type('new_dict', (object,), description)
                await self.peerConnections[id].setRemoteDescription(desc)

            @self.sio.event
            async def watcher(id):
                pc = RTCPeerConnection(configuration=RTCConfiguration([
                    RTCIceServer("stun:stun.l.google:19302"),
                    RTCIceServer(self.gsdbs.credentials["turnserver"],
                                 self.gsdbs.credentials["turnuser"],
                                 self.gsdbs.credentials["turnpw"]),
                ]))

                self.peerConnections[id] = pc

                video = self.getPiH264Relay()

                @pc.on("iceconnectionstatechange")
                async def on_iceconnectionstatechange():
                    # self._logger.info("ICE connection state is %s", pc.iceConnectionState)
                    if pc.iceConnectionState == "failed":
                        video_trackList.remove(video)
                        await pc.close()
                        self.peerConnections.pop(id, None)

                transceiver = pc.addTransceiver("video")
                capabilities = RTCRtpSender.getCapabilities("video")
                preferences = list(filter(lambda x: x.name == "H264", capabilities.codecs))
                preferences += list(filter(lambda x: x.name == "rtx", capabilities.codecs))
                transceiver.setCodecPreferences(preferences)

                for t in pc.getTransceivers():
                    if t.kind == "video":
                        pc.addTrack(video)

                await pc.setLocalDescription(await pc.createOffer())
                await self.sio.emit("offer", {"id": id,
                                              "message": json.dumps(
                                                  {"type": pc.localDescription.type,
                                                   "sdp": pc.localDescription.sdp})})

            @self.sio.event
            async def disconnectPeer(id):
                if id in self.peerConnections:
                    await self.peerConnections[id].close()
                    self.peerConnections.pop(id, None)

            @self.sio.event
            async def disconnect():
                self._logger.info('disconnected from server')

            connectURL = ""

            if "localhost" in self.gsdbs.credentials["signalserver"]:
                connectURL = f'{self.gsdbs.credentials["signalserver"]}:{str(self.gsdbs.credentials["signalport"])}'
            else:
                connectURL = self.gsdbs.credentials["signalserver"]

            await self.sio.connect(
                f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}{self.gsdbs.credentials["cnode"]}')
            await self.sio.wait()
