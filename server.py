import asyncio
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

# ✅ Correct import path
from pipecat.transports.smallwebrtc.request_handler import (
    SmallWebRTCPatchRequest,
    SmallWebRTCRequest,
    SmallWebRTCRequestHandler,
)
from pipecat.transports.smallwebrtc.connection import SmallWebRTCConnection
from pipecat.transports.smallwebrtc.transport import SmallWebRTCTransport
from pipecat.transports.base_transport import TransportParams
from pipecat.runner.types import SmallWebRTCRunnerArguments

from main import run_bot

load_dotenv()

small_webrtc_handler = SmallWebRTCRequestHandler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/offer")
async def offer(request: SmallWebRTCRequest, background_tasks: BackgroundTasks):
    async def webrtc_connection_callback(connection: SmallWebRTCConnection):
        transport = SmallWebRTCTransport(
            webrtc_connection=connection,
            params=TransportParams(
                audio_in_enabled=True,
                audio_out_enabled=True,
                video_out_enabled=True,
                video_out_is_live=True,
                video_out_width=512,
                video_out_height=512,
            ),
        )
        runner_args = SmallWebRTCRunnerArguments(
            webrtc_connection=connection,
        )
        # Running the bot in a background task so the callback returns immediately
        # and the SDP answer can be sent back to the client.
        asyncio.create_task(run_bot(transport, runner_args))

    background_tasks.add_task(lambda: None)

    answer = await small_webrtc_handler.handle_web_request(
        request=request,
        webrtc_connection_callback=webrtc_connection_callback,
    )
    return answer

# ✅ Required for ICE candidate exchange
@app.patch("/offer")
async def ice_candidate(request: SmallWebRTCPatchRequest):
    logger.debug(f"Received ICE candidate patch: {request}")
    await small_webrtc_handler.handle_patch_request(request)
    return {"status": "success"}