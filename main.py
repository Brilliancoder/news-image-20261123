"""make.fun news-image-20261123: copy the pre-rendered entry.png to the output dir."""
import os
import shutil
from pathlib import Path

out = Path(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'))
out.mkdir(parents=True, exist_ok=True)
shutil.copyfile(Path(__file__).with_name('entry.png'), out / 'entry.png')
