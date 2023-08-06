import argparse
import tempfile
import qrcode
from fpdf import FPDF
from qrcode.image.pil import PilImage


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
    parser.add_argument("--ssid", required=True, help="network name")
    parser.add_argument("--pw", required=True, help="network password")
    parser.add_argument("--out", required=False, help="output filename")
    args = parser.parse_args(argv)
    if not args.out:
        args.out = f"wifipass_{args.ssid}"
    return args


def _qr_str(ssid: str, pw: str) -> str:
    return f"WIFI:T:WPA;S:{ssid};P:{pw};;"


def main(argv=None):
    args = _parse_args(argv)
    img = qrcode.make(_qr_str(args.ssid, args.pw))

    if args.out.lower().endswith(".png"):
        img.save(args.out, format="PNG")
    elif args.out.lower().endswith(".pdf"):
        _save_as_pdf(img, args.ssid, args.pw, args.out)
    else:
        img.save(f"{args.out}.png", format="PNG")
