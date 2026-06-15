"""Server lifecycle and ZeroMQ request helpers for integration tests."""

import shutil
import signal
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

import zmq

DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 9090


@dataclass
class RequestResult:
    received: bool
    reply: object


@dataclass
class ManagedServer:
    process: subprocess.Popen
    workdir: Path
    ip: str = DEFAULT_IP
    port: int = DEFAULT_PORT

    def stop(self):
        if self.process.poll() is None:
            self.process.send_signal(signal.SIGINT)
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=2)

    def read_output(self):
        if not self.process.stdout:
            return ""
        try:
            return self.process.stdout.read()
        except Exception:
            return ""


def make_isolated_workspace(project_root: Path, tmp_path: Path) -> Path:
    workspace = tmp_path / "phon_book_workspace"
    shutil.copytree(project_root, workspace)
    return workspace


def remove_db(workdir: Path):
    db_path = workdir / "sab.db"
    if db_path.exists():
        db_path.unlink()


def start_server(workdir: Path, python_bin: str, ip: str = DEFAULT_IP, port: int = DEFAULT_PORT) -> ManagedServer:
    proc = subprocess.Popen(
        [python_bin, str(workdir / "server.py")],
        cwd=str(workdir),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    time.sleep(0.8)
    return ManagedServer(process=proc, workdir=workdir, ip=ip, port=port)


def send_commands(commands, ip: str = DEFAULT_IP, port: int = DEFAULT_PORT, timeout_ms: int = 3000) -> RequestResult:
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REQ)
    socket.bind(f"tcp://{ip}:{port}")
    try:
        socket.send_json(commands)
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)
        socks = dict(poller.poll(timeout_ms))
        if socks.get(socket) == zmq.POLLIN:
            return RequestResult(received=True, reply=socket.recv_json())
        return RequestResult(received=False, reply=None)
    finally:
        socket.close(0)
        ctx.term()
