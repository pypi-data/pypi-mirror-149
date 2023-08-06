import argparse
import tempfile
import qrcode
from fpdf import FPDF
from qrcode.image.pil import PilImage
from getpass import getpass
from dataclasses import dataclass


@dataclass
class Config:
    ssid: str
    pw: str
    filename: str


def _save_as_pdf(img: PilImage, ssid: str, pw: str, filename: str) -> None:
    fp = tempfile.NamedTemporaryFile()
    img.save(fp, format="PNG")
    pdf = FPDF()
    pdf.add_page(orientation="P")
    pdf.set_font("Arial", "", 14)
    pdf.write(5, f"SSID: {ssid}\nPW: {pw}\n")
    pdf.image(fp.name, 0, None, 200, 200, type="PNG")
    pdf.output(filename)
    fp.close()


def _parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="python -m wifipass",
    )
    parser.add_argument("--ssid", required=False, help="network name")
    parser.add_argument("--pw", required=False, help="network password")
    parser.add_argument("--out", required=False, help="output filename")
    return parser.parse_args(argv)


def _qr_str(ssid: str, pw: str) -> str:
    return f"WIFI:T:WPA;S:{ssid};P:{pw};;"


def _assure_opts(args) -> Config:
    c = Config(args.ssid, args.pw, args.out)
    if not c.ssid:
        c.ssid = input("Please enter the ssid: ")

    if not c.pw:
        c.pw = getpass("Please enter the password: ")

    if not c.filename:
        c.filename = input("Please enter the output filename: ")

    return c


def main(argv=None):
    args = _parse_args(argv)
    config = _assure_opts(args)

    img = qrcode.make(_qr_str(config.ssid, config.pw))

    if config.filename.lower().endswith(".png"):
        img.save(config.filename, format="PNG")
    elif config.filename.lower().endswith(".pdf"):
        _save_as_pdf(img, config.ssid, config.pw, config.filename)
    else:
        img.save(f"{config.filename}.png", format="PNG")
