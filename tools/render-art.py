"""Rasterize original vector artwork to Nexus' 640x360 gameart contract."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]

def main():
    # Native vector geometry, drawn directly; no copyrighted game media is redistributed.
    scale = 2
    image = Image.new('RGB', (640 * scale, 360 * scale))
    draw = ImageDraw.Draw(image)
    for y in range(360 * scale):
        t = y / (360 * scale)
        color = tuple(int(a + (b - a) * t) for a, b in zip((16, 28, 41), (52, 78, 83)))
        draw.line((0, y, 640 * scale, y), fill=color)
    def poly(points, fill):
        draw.polygon([(x * scale, y * scale) for x, y in points], fill=fill)
    def rect(bounds, fill, outline=None, width=1):
        draw.rectangle(tuple(n * scale for n in bounds), fill=fill, outline=outline, width=width * scale)
    draw.ellipse((439*scale,42*scale,495*scale,98*scale), fill='#879e98')
    poly([(0,225),(110,206),(242,219),(420,212),(640,211),(640,360),(0,360)], '#203538')
    for x, y, size in [(35,53,1),(119,87,.9),(548,99,.85),(608,51,1.1)]:
        poly([(x,y),(x-30*size,y+94*size),(x-17*size,y+94*size),(x-47*size,y+188*size),(x+47*size,y+188*size),(x+17*size,y+94*size),(x+30*size,y+94*size)], '#172b30')
    rect((223,197,420,303), '#493c32')
    for y in range(215,300,17):
        draw.line((223*scale,y*scale,420*scale,y*scale), fill='#322e29', width=3*scale)
    poly([(365,105),(385,105),(385,152),(365,136)], '#343e3e')
    poly([(199,205),(320,105),(443,205)], '#697571')
    poly([(205,202),(320,111),(437,202)], '#1a2327')
    poly([(211,200),(320,113),(429,200)], '#2b3435')
    for x in [250,344]:
        rect((x,220,x+43,262), '#e4b16c', '#242d2e', 6)
        draw.line(((x+22)*scale,223*scale,(x+22)*scale,259*scale), fill='#3e3930', width=3*scale)
        draw.line(((x+3)*scale,241*scale,(x+40)*scale,241*scale), fill='#3e3930', width=3*scale)
    rect((307,239,335,303), '#1d2528', '#716450', 3)
    draw.ellipse((327*scale,273*scale,331*scale,277*scale), fill='#d9ae68')
    poly([(295,304),(347,304),(389,360),(254,360)], '#414f4d')
    for x,y in [(53,112),(578,161)]:
        poly([(x,y),(x-27,y+88),(x-14,y+88),(x-50,360),(x+50,360),(x+14,y+88),(x+27,y+88)], '#101e23')
    image = image.resize((640,360), Image.Resampling.LANCZOS)
    target = ROOT / 'extension' / 'gameart.png'
    image.save(target, optimize=True)
    print(f'confirmed: original gameart {target}, {target.stat().st_size} bytes, {image.size}')

if __name__ == '__main__':
    main()
