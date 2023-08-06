import argparse
import tempfile
import qrcode
from fpdf import FPDF


def main(argv=None):
    file_format = ["PNG", "PDF", "BOTH"]
    parser = argparse.ArgumentParser(
        prog="python -m wifipass",
    )
    parser.add_argument("--ssid", required=True, help="network name")
    parser.add_argument("--pw", required=True, help="network password")
    parser.add_argument("--format", required=True, choices=file_format)
    parser.add_argument("--out", required=False, help="basename for the outputfile(s)")
    args = parser.parse_args(argv)

    use_format = args.format
    ssid = args.ssid
    pw = args.pw
    if args.out:
        out_name = args.out
    else:
        out_name = f"wifipass_{ssid}"

    img = qrcode.make(f"WIFI:T:WPA;S:{ssid};P:{pw};;")

    if use_format == "PNG" or use_format == "BOTH":
        img.save(f"{out_name}.png", format="PNG")
    elif use_format == "PDF" or use_format == "BOTH":
        fp = tempfile.NamedTemporaryFile()
        img.save(fp, format="PNG")
        pdf = FPDF()
        pdf.add_page(orientation="P")
        pdf.set_font("Arial", "", 14)
        pdf.write(5, f"SSID: {ssid}\nPW: {pw}\n")
        pdf.image(fp.name, 0, None, 200, 200, type="PNG")
        pdf.output(f"{out_name}.pdf")
        fp.close()
