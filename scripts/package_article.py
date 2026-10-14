#!/usr/bin/env python3
# Modified 2026-10-14: naming and package-path cleanup; see THIRD_PARTY_NOTICES.md.
"""Prepare the confirmed footer or wrap a validated article for local preview."""
import argparse
import base64
import html
import importlib.util
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('果汁哥AI大本营_星球.webp', '果汁哥AI_Agent交流群.png')
FOOTER = '果汁哥固定文末_摸鱼绿.html'
MIME = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.webp': 'image/webp', '.gif': 'image/gif'}


def write_if_same_or_new(path, data):
    if path.exists() and path.read_bytes() != data:
        raise ValueError(f'同名文件内容不同，请明确处理后重试：{path}')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def prepare(article, source):
    manifest = json.loads((source / 'manifest.json').read_text(encoding='utf-8'))
    files = {article / 'assets' / name: (source / name).read_bytes()
             for name in (*NAMES, FOOTER)}
    urls = {f'assets/{name}': manifest['source_urls'][name] for name in NAMES}
    files[article / 'assets/qr-source-urls.json'] = json.dumps(
        urls, ensure_ascii=False, indent=2).encode()
    # Check conflicts before creating any output.
    for path, data in files.items():
        if path.exists() and path.read_bytes() != data:
            raise ValueError(f'同名文件内容不同，请明确处理后重试：{path}')
    for path, data in files.items():
        write_if_same_or_new(path, data)
    print(f'已准备文末与双入口素材：{article / "assets"}')


class ImageSources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.sources.append(dict(attrs).get('src', ''))


COPY_JS = r'''
var juiceImageMap = __IMAGE_MAP__;
function juiceCopy(){
  var fragment=document.getElementById('juice-content').cloneNode(true);
  fragment.querySelectorAll('img').forEach(function(img){
    var src=img.getAttribute('src');
    if(juiceImageMap[src])img.setAttribute('src',juiceImageMap[src]);
  });
  var bad=[...fragment.querySelectorAll('img')].some(function(img){
    return !/^(https?:\/\/|data:image\/)/i.test(img.getAttribute('src')||'');
  });
  if(bad){juiceShowToast('图片路径未处理，复制已停止');return;}
  var payload=fragment.innerHTML, copied=false;
  var handler=function(event){
    event.clipboardData.setData('text/html',payload);
    event.clipboardData.setData('text/plain',fragment.textContent);
    event.preventDefault();copied=true;
  };
  var range=document.createRange();
  range.selectNodeContents(document.getElementById('juice-content'));
  var sel=window.getSelection();sel.removeAllRanges();sel.addRange(range);
  document.addEventListener('copy',handler);
  var ok=false;
  try{ok=document.execCommand('copy') && copied;}catch(e){ok=false;}
  finally{document.removeEventListener('copy',handler);sel.removeAllRanges();}
  window.juiceLastCopy={success:ok,images:fragment.querySelectorAll('img').length,
    localImagePaths:0,htmlLength:payload.length};
  juiceShowToast(ok?'已复制，去公众号编辑器按Ctrl/⌘+V粘贴':'自动复制失败，请换用Chrome重试');
}
'''


def preview(clean, engine):
    content = clean.read_text(encoding='utf-8')
    if not content.strip().startswith('<section') or not content.strip().endswith('</section>'):
        raise ValueError('输入必须是干净section正文')
    spec = importlib.util.spec_from_file_location('juice_validator', engine / 'scripts/validate_article_html.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    errors, warnings, _ = module.validate(content, str(clean))
    if errors or warnings:
        raise ValueError(f'HTML未通过：{len(errors)} ERROR / {len(warnings)} WARNING\n' +
                         '\n'.join(errors + warnings))
    parser = ImageSources()
    parser.feed(content)
    map_path = clean.parent / 'assets/qr-source-urls.json'
    fixed = json.loads(map_path.read_text(encoding='utf-8')) if map_path.exists() else {}
    image_map = {}
    for src in parser.sources:
        url = urlsplit(src)
        if not src:
            raise ValueError('存在空图片src')
        if url.scheme in ('http', 'https', 'data'):
            continue
        if src in fixed:
            if not (clean.parent / unquote(url.path)).is_file():
                raise ValueError(f'预览二维码图片不存在：{src}')
            if not fixed[src].startswith('https://mmbiz.qpic.cn/'):
                raise ValueError(f'二维码缺少已确认的微信原图URL：{src}')
            image_map[src] = fixed[src]
            continue
        if Path(unquote(url.path)).name in NAMES:
            raise ValueError('固定二维码缺少映射，请先运行prepare')
        if url.scheme or src.startswith('//'):
            raise ValueError(f'不支持的图片路径：{src}')
        local = (clean.parent / unquote(url.path)).resolve()
        if not local.is_relative_to(clean.parent.resolve()):
            raise ValueError(f'先把图片复制到本篇assets：{src}')
        mime = MIME.get(local.suffix.lower())
        if not mime:
            raise ValueError(f'不支持的本地图片类型：{src}')
        image_map[src] = f'data:{mime};base64,' + base64.b64encode(local.read_bytes()).decode()
    subprocess.run([sys.executable, str(engine / 'scripts/wrap_preview.py'), str(clean)], check=True)
    out = clean.with_name(clean.stem + '_预览.html')
    result = out.read_text(encoding='utf-8')
    script = re.search(r'<script>(.*?)</script>', result, re.S)
    if not script or 'function juiceCopy()' not in script.group(1):
        raise ValueError('引擎预览模板发生变化，无法注入复制映射')
    prefix = script.group(1).split('function juiceCopy()', 1)[0]
    encoded = json.dumps(image_map, ensure_ascii=False).replace('<', '\\u003c')
    replacement = '<script>' + prefix + COPY_JS.replace('__IMAGE_MAP__', encoded) + '</script>'
    result = result[:script.start()] + replacement + result[script.end():]
    result = result.replace('<title>' + clean.stem, '<title>' + html.escape(clean.stem))
    out.write_text(result, encoding='utf-8')
    print('校验：0 ERROR / 0 WARNING；复制映射已生成，需实际点击验收。')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    commands = ap.add_subparsers(dest='mode', required=True)
    stage = commands.add_parser('prepare')
    stage.add_argument('article', type=Path)
    stage.add_argument('--source', type=Path, default=ROOT / 'assets/footer')
    wrap = commands.add_parser('preview')
    wrap.add_argument('clean', type=Path)
    wrap.add_argument('--engine', type=Path, default=ROOT / 'vendor/layout-engine')
    args = ap.parse_args()
    try:
        if args.mode == 'prepare':
            prepare(args.article.resolve(), args.source.resolve())
        else:
            preview(args.clean.resolve(), args.engine.resolve())
    except (ValueError, OSError, KeyError, ImportError, subprocess.CalledProcessError) as exc:
        ap.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
