# -*- coding: utf-8 -*-
"""บิลด์เว็บ NekojomXNexplay: เติมรูปทั้งหมดลงเทมเพลต แล้วอัปเดตไฟล์ + แพ็กเกจ Vercel"""
import base64, os, re, zipfile

def b64(path, mime):
    with open(path,'rb') as f:
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode()

def build():
    tpl = open('site_template.html', encoding='utf-8').read()
    html = tpl.replace('__BG__', b64('assets/compressed/bg.jpg','image/jpeg'))
    for i in range(1,6):
        html = html.replace(f'__PACK{i}__', b64(f'assets/compressed/pack{i}.jpg','image/jpeg'))
    for i in range(1,4):
        html = html.replace(f'__MAP{i}__', b64(f'assets/compressed/map{i}.jpg','image/jpeg'))
    for i in range(1,5):
        html = html.replace(f'__COVER{i}__', b64(f'assets/compressed/cover{i}.jpg','image/jpeg'))
    html = html.replace('__ADMIN__', b64('assets/compressed/admin.jpg','image/jpeg'))
    html = html.replace('__PANELBG__', b64('assets/compressed/panelbg.jpg','image/jpeg'))
    html = html.replace('__ROBUX__', b64('assets/compressed/robux.png','image/png'))
    html = html.replace('__FAVICON__', b64('assets/compressed/favicon.png','image/png'))
    html = html.replace('__FAVICON180__', b64('assets/compressed/apple-touch.png','image/png'))
    for i in range(1,8):
        html = html.replace(f'__PROMO{i}__', b64(f'assets/compressed/promo{i}.jpg','image/jpeg'))

    tokens = ['__BG__','__ADMIN__','__PANELBG__','__ROBUX__','__FAVICON__','__FAVICON180__'] \
           + [f'__PACK{i}__' for i in range(1,6)] + [f'__MAP{i}__' for i in range(1,4)] \
           + [f'__COVER{i}__' for i in range(1,5)] + [f'__PROMO{i}__' for i in range(1,8)]
    left = [t for t in tokens if t in html]
    assert not left, f'placeholder ไม่ถูกแทน: {left}'

    open('NekojomXNexplay.html','w',encoding='utf-8').write(html)
    print('NekojomXNexplay.html:', os.path.getsize('NekojomXNexplay.html')//1024, 'KB')

    # อัปเดตแพ็กเกจ Vercel
    os.makedirs('vercel-deploy', exist_ok=True)
    with open('vercel-deploy/index.html','w',encoding='utf-8') as f:
        f.write(html)
    with zipfile.ZipFile('vercel-deploy.zip','w',zipfile.ZIP_DEFLATED) as z:
        z.write('vercel-deploy/index.html','index.html')
    print('vercel-deploy.zip อัปเดตแล้ว')

    # เช็ค JS
    scripts = re.findall(r'<script>(.*?)</script>', html, re.S)
    open('/tmp/check.js','w',encoding='utf-8').write('\n'.join(scripts))
    print('ไฟล์ JS สำหรับตรวจ: /tmp/check.js')

if __name__ == '__main__':
    build()
