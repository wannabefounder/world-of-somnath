"""Build the static recruiter site (site/) from the portfolio media folder.

Usage: python3 scripts/build_work_site.py /path/to/harsh-portfolio/media
Copies only the media referenced below, makes small cover thumbnails, and
writes site/work/data.js with dimensions and video durations.
"""
import json, os, shutil, subprocess, sys
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/media_src/media'
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
OUT_MEDIA = os.path.join(ROOT, 'media')

# ---------- media helpers ----------------------------------------------------
def I(key, cap=None):  return {'k': 'i', 'f': key + '.webp', 'cap': cap}
def S(name, cap=None): return {'k': 's', 'f': name + '.svg', 'cap': cap}
def V(name, cap=None): return {'k': 'v', 'f': name, 'cap': cap}

def W(t, p, m, c=False, n=None):
    """A work item: title, product tag, media list, concept flag, note."""
    return {'t': t, 'p': p, 'm': m, 'c': c, 'n': n}

def rng(prefix, nums): return [I(prefix + str(n)) for n in nums]

# ---------- the work, by discipline -> type ----------------------------------
WORK = {
 'Product design': {
  'App screens': [
   W('Snapmint UPI home and headers', 'Snapmint UPI',
     [I('upi__headers-interm__home-app', 'Home, intermediate iteration'),
      I('upi__final-headers__upi-home-4x', 'Final header, UPI home'),
      I('upi__final-headers__snapmint-home-4x', 'Final header, Snapmint home')],
     n='Home headers for the Snapmint app and the new UPI home.'),
   W('UPI bottom navigation', 'Snapmint UPI',
     [I('upi__upi-bottom-nav__home'), I('upi__upi-bottom-nav__home-1')], n='Shipped in production.'),
   W('Secure login and linked-account home', 'Snapmint UPI',
     [I('upi__snapmint-upi-b__secure-login', 'Biometric secure login'),
      I('upi__snapmint-upi-b__upi-home-tpap-linked', 'UPI home after linking')]),
   W('Order processing screen', 'Snapmint', [I('op__order-processing')]),
   W('Order confirmation', 'Snapmint',
     [I('oc__initial', 'Initial'), I('oc__intermeddiate-__frame-48097907', 'Exploration, not shipped')]),
   W('Home: travel and recharges modal', 'Snapmint',
     [I('home__final-in-prod-__option-18', 'In production'), I('home__final-in-prod-__recharge-2')]),
   W('App onboarding and OTP', 'Snapmint',
     [I('onb__new-before-reb__login-mobile-number'), I('onb__new-before-reb__login-mobile-number-1'),
      I('onb__new-before-reb__login-mobile-number-2'), I('onb__new-before-reb__error-otp'),
      I('onb__new-before-reb__error-otp-1'), I('onb__new-before-reb__error-otp-2'),
      I('onb__old__mobile-number-filled', 'Before: the old screen')]),
   W('Checkout redesign', 'Snapmint',
     rng('co__snapmint-check__iphone-13-14-', [128, 129, 130, 131, 132, 133, 134, 135, 136, 137])
     + rng('co__snapmint-check__iphone-13-14-', [77, 80, 85, 87, 89, 94])
     + [I('co__snapmint-cheko__checkout-snapmint-com-otp-mobile-9742472', 'Before: the current checkout')],
     c=True, n='Final proposal, on hold for engineering bandwidth. Earlier iterations follow.'),
  ],
  'Landing pages and flows': [
   W('Credit Line on UPI landing page', 'Credit Line on UPI', [I('upi__credit-line-on-final__clou-landing-page')]),
   W('Credit line activation flow', 'Credit Line on UPI',
     [I('upi__credit-line-on-intermediate-f__activate-credit-line'),
      I('upi__credit-line-on-intermediate-f__activate-credit-line-1'),
      I('upi__credit-line-on-intermediate-f__activate-credit-line-2')]
     + rng('upi__credit-line-on-rough-credit-l__activate-credit-line-', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]),
     n='Pre-rebrand flow, followed by the early onboarding explorations.'),
  ],
  'Widgets and popups': [
   W('White-label pay-later widgets and popups', 'Whitelabel Widget',
     [I('wid__whitelabel-pop__man-matters'), I('wid__whitelabel-pop__one-carat'),
      I('wid__whitelabel-pop__section-1'), I('wid__whitelabel-pop__section-2'),
      I('wid__whitelabel-pop__glen'), I('wid__whitelabel-pop__andamen'),
      I('wid__whitelabel-pop__controlz-updated'), I('wid__whitelabel-pop__decorshed')],
     n='One widget system that takes on each merchant\'s brand.'),
   W('Reise Moto widget and popup', 'Whitelabel Widget',
     [I('wid__reise-widgetan__mp-2-0'), I('wid__reise-widgetan__frame-1')]),
  ],
  'Icons and illustration': [
   W('UPI isometric icon exploration', 'Snapmint UPI',
     [I('upi__upi-homepage-i__gradient1-5'), I('upi__upi-homepage-i__gradient1-1'),
      I('upi__upi-homepage-i__gradient1-3'), I('upi__upi-homepage-i__home-upi-first-time-user-proposed-icon', 'Proposed icons'),
      I('upi__upi-homepage-i__home-upi-first-time-oldicon', 'Old icons'),
      S('ic-scan'), S('ic-send'), S('ic-history'), S('ic-wallet')], c=True),
   W('Travel and recharge icons', 'Snapmint',
     [I('home__final-in-prod-__aeroplane-1'), I('home__final-in-prod-__bus-1'),
      I('home__final-in-prod-__train-1'), S('ic-recharge')], n='In production on the app home.'),
   W('Trust icons', 'Snapmint', [I('trust-icons__pdp-delivery-tat-26-may-2075')]),
   W('Pay Later logo', 'Snapmint', [S('paylater-b'), S('paylater-a')]),
   W('Snapmint UPI app icon', 'Snapmint UPI', [S('upi-logo'), I('upi__logo-icon__vertical-on-primary')]),
  ],
  'Internal tools': [
   W('ID Studio: ID card automation', 'ID Studio',
     [I('ids__public__og'), I('ids__public-templates__front-financial-services'),
      I('ids__public-templates__back-financial-services'), I('ids__public-templates__front-credit-advisory'),
      I('ids__public-templates__back-credit-advisory'), I('ids__public-share-template__new-joiner-front-v2'),
      I('ids__public-share-template__new-joiner-back-v2')],
     n='Company ID card and new-joiner post automation, designed and built by me.'),
   W('Wholesale store, designed and built', 'Ajay Sanjay',
     [I('ws__apps-web-public-assets-products-house__ajay-sanjay-atta'),
      I('ws__apps-web-public-assets-products-house__ajay-sanjay-rice'),
      I('ws__apps-web-public-assets-products-house__ajay-sanjay-dal'),
      I('ws__apps-web-public-assets-products-house__ajay-sanjay-oil'),
      I('ws__apps-web-public-assets-products-house__ajay-sanjay-chilli'),
      I('ws__apps-web-public-assets-products-house__ajay-sanjay-salt')],
     n='A full wholesale store, designed and coded by me. Shown here: the house-brand product images.'),
  ],
 },
 'Video': {
  'UGC ads': [
   W('Smart shopping secrets', 'Snapmint', [V('ugc-secrets')]),
   W('Earphone reel', 'Snapmint', [V('ugc-earphone')]),
   W('Creator testimonial', 'Snapmint', [V('ugc-shilpi')]),
   W('Infinix at Rs 450 + EMI', 'Snapmint', [V('ugc-infinix')]),
   W('Motorola reel', 'Snapmint', [V('ugc-moto')]),
  ],
  'AI video': [
   W('Rs 19 se shopping start', 'Snapmint', [V('ai-1')]),
   W('Earphones at Rs 19', 'Snapmint', [V('ai-2')]),
   W('POCO at Rs 299 + EMI later', 'Snapmint', [V('ai-poco')]),
   W('Redmi A4 5G offer', 'Snapmint', [V('ai-redmi')]),
   W('Noise offer film', 'Snapmint', [V('ai-noise')]),
   W('Snapmint for business', 'Snapmint', [V('ai-b2b')]),
   W('UPI with Pay Later', 'Snapmint UPI', [V('upi-ai')]),
   W('Hiring film', 'Propzilla', [V('ai-hiring')]),
   W('GenAI study: the eye', 'Personal', [V('genai-a')]),
   W('GenAI study: particles', 'Personal', [V('genai-b')]),
  ],
  'Product films': [
   W('Snapmint UPI app film', 'Snapmint UPI', [V('upi-app')]),
   W('Credit Line on UPI: intro', 'Credit Line on UPI', [V('clou-intro')]),
   W('Credit Line on UPI: link your line', 'Credit Line on UPI', [V('upi-link')]),
   W('How to pay Credit Line on UPI bills', 'Credit Line on UPI', [V('upi-repay')]),
   W('Credit Line on UPI: pay on Amazon', 'Credit Line on UPI', [V('clou-amazon')]),
   W('Credit Line on UPI: pay with GPay', 'Credit Line on UPI', [V('clou-gpay')]),
   W('Credit Line on UPI: pay with PhonePe', 'Credit Line on UPI', [V('clou-phonepe')]),
   W('Credit Line on UPI: Hindi film', 'Credit Line on UPI', [V('clou-hindi')]),
   W('Play Store video', 'Snapmint', [V('play-store')]),
  ],
  'Events and culture': [
   W('Office moments', 'Snapmint', [V('office-moments')]),
   W('Live event reel', 'Snapmint', [V('pancham')]),
   W('Event presentation film', 'Snapmint', [V('event-deck')]),
  ],
 },
 'Editing': {
  'Music videos': [
   W('Devotional music video, 2026', 'Music label', [V('mv-2026')] + rng('mv-2026-', range(1, 7))),
   W('Devotional music video, 2024', 'Music label', [V('mv-2024')] + rng('mv-2024-', range(1, 7))),
   W('Devotional music video, 2022', 'Music label', [V('mv-2022')] + rng('mv-2022-', range(1, 7))),
  ],
  'Podcast': [
   W('Buy the Way: podcast trailer', 'Buy the Way', [V('pod-trailer')]),
  ],
 },
 'Motion graphics': {
  'Sale promos': [
   W('Break the Payment Sale, v1', 'Snapmint', [V('sale-v1')]),
   W('Break the Payment Sale, v2', 'Snapmint', [V('sale-v2')]),
  ],
  'Retail LED displays': [
   W('Sleep now, pay later: Duroflex store loop', 'Snapmint', [V('led-duroflex')]),
   W('Buy now: Frido store loop', 'Snapmint', [V('led-frido')]),
   W('Slot machine store loop', 'Snapmint', [V('led-slot')]),
  ],
  'UI motion': [
   W('Splash animation, A', 'Snapmint', [V('splash-a')]),
   W('Splash animation, B', 'Snapmint', [V('splash-b')]),
   W('0% EMI loader', 'Snapmint', [V('loader-pie')]),
   W('Processing loader', 'Snapmint', [V('loader-processing')]),
   W('Titan product page journey', 'Snapmint', [V('titan-journey')]),
  ],
  'Brand loops': [
   W('Business website loops', 'Snapmint', [V('biz-loops')]),
  ],
  'Character animation': [
   W('Mug Mountain: launch film', 'GATTI', [V('gatti-v31')], c=True),
   W('The Mug Quits', 'GATTI', [V('gatti-short')], c=True),
   W('What is GATTI, 15s', 'GATTI', [V('gatti-15')], c=True),
   W('Hi, I\'m the welcome mug', 'GATTI', [V('gatti-v1')], c=True),
   W('Culture made solid', 'GATTI', [V('gatti-v2')], c=True),
   W('Pitch: Diwali week', 'GATTI', [V('gatti-bl')], c=True),
   W('Pitch: Big Billion Days', 'GATTI', [V('gatti-fk')], c=True),
   W('Pitch: Mega Blockbuster Sale', 'GATTI', [V('gatti-me')], c=True),
  ],
 },
 'Graphic design': {
  'Communication banners': [
   W('In-app communication banners', 'Snapmint',
     [I('comm__comunication-p__property-1-variant' + str(n)) for n in (10, 11, 6, 13, 20, 23, 9, 14)]
     + [I('comm__comunication-p__property-1-timer-big-expanded'), I('comm__comunication-p__property-1-bottom-bar')]),
   W('WhatsApp banners', 'Snapmint',
     [I('comm__whatsapp-banne__frame-' + s) for s in ('2147228177', '2147228224', '2147228225', '2147228226', '2147228227')]
     + [I('comm__flights-whatsapp-banner'), I('comm__snitch-whatsapp-banner')]),
   W('WhatsApp carousel', 'Snapmint',
     [I('comm__whtsapp-crouse__one'), I('comm__whtsapp-crouse__two'), I('comm__whtsapp-crouse__two-1'),
      I('comm__whtsapp-crouse__two-2'), I('comm__whtsapp-crouse__two-3'), I('comm__whtsapp-crouse__two-4')]),
   W('Travel push notifications', 'Snapmint',
     [I('comm__travel-push-no__ram-navami'), I('comm__travel-push-no__5'), I('comm__travel-push-no__6')]),
   W('Sale strips', 'Snapmint',
     [I('misc__sale-strips__prebuzz'), I('misc__sale-strips__during-sale-non-signed-up'),
      I('misc__sale-strips__signup-already'), I('misc__sale-strips__desktop-live'),
      I('misc__sale-strips__desktop-live-after-sign-up'), I('misc__sale-strips__group-1244830166')]),
  ],
  'Partner banners': [
   W('Titan, Fastrack and Sonata banners', 'Snapmint',
     [I('titan__app-1'), I('titan__app-2'), I('titan__titan-1'), I('titan__titan-2'),
      I('titan__fastrack-1'), I('titan__fastrack-2'), I('titan__sonata-1'), I('titan__sonata-2')]),
  ],
  'Performance marketing': [
   W('Performance marketing creatives', 'Snapmint',
     [I('perf__frame-10'), I('perf__frame-8'), I('perf__wrench-18136869-258'), I('perf__wrench-18136869-275')]),
  ],
  'Emailers': [
   W('Snapmint Ads emailers', 'Snapmint',
     [I('emailers__snapmint-ads-e__snapmint-ads-emailer'), I('emailers__snapmint-ads-e__snapmint-ads-emailer-1')]),
   W('Christmas EMI sale emailer', 'Snapmint', [I('emailers__snapmint-ads-e__christmas-emi-sale-emailer')]),
  ],
  'Print and retail': [
   W('In-store standees', 'Snapmint', [I('standee__standee-final-6'), I('standee__duroflex-standee-2')]),
   W('Offline and co-branded QR codes', 'Snapmint',
     [I('qr__snapmint-rebrandedqr-mannunalwork'), I('qr__co-branded-qr__5295-omaxechandnichowk-delhincr'),
      I('qr__iniitial-desig__a4-1', 'Initial design')]),
   W('Event invite', 'Snapmint', [I('invites__8270-lower-parel')]),
  ],
  'Identity': [
   W('Buy the Way: podcast identity', 'Buy the Way',
     [S('pod-final', 'Final logo'), I('pod__podcast-cuecar__frame-13', 'Cue cards'), I('pod__podcast-cuecar__frame-14'),
      S('cue-q'), S('pod-01', 'Explorations'), S('pod-06'), S('pod-09'), S('pod-11'), S('pod-14'), S('pod-16')]),
   W('MokshaVastra: brand and products', 'MokshaVastra',
     [S('mv-logo-black'), I('mv__public-hero__adiyogi-poster'), I('mv__public-hero__mahabali-poster')]
     + [I('mv__public-products__' + n + '-front') for n in
        ('adiyogi', 'mahabali', 'kali-tandav', 'shiva-trinetra', 'krishna-leela', 'hanuman-gada',
         'vighnaharta', 'om-namah-shivay', 'nritya-shiva-hoodie', 'astral-hoodie', '108-hoodie', 'bhakt')]),
   W('GATTI: identity and pitch', 'GATTI',
     [I('gatti__linkedin__gatti-page-logo'), I('gatti__linkedin__gatti-page-cover')]
     + [I('gatti__pitch-round2-linkedin-carou-slides__slide-%02d' % n) for n in range(1, 12)]
     + [I('gatti__pitch-round2__pitch2-blinkit-diwali-set-4x5-poster'),
        I('gatti__pitch-round2__pitch2-flipkart-bbd-set-4x5-poster'),
        I('gatti__pitch-round2__pitch2-meesho-blockbuster-set-4x5-poster')], c=True),
  ],
  'Social': [
   W('LinkedIn creatives', 'Snapmint',
     [I('linkedin__linkedin-1__linkden-1'), I('linkedin__linkedin-1__linkden-2'), I('linkedin__linkedin-1__linkden-3')]),
   W('Personal LinkedIn banner and character', 'Personal',
     [I('gatti__linkedin-personal__personal-banner'), I('gatti__linkedin-personal__harsh-the-builder-character')]),
  ],
 },
}

PROJECTS = [
 {'p': 'Snapmint UPI', 'y': 'Product design, motion, film',
  'b': 'A UPI app inside Snapmint: home and headers, navigation, secure login, the app icon, an isometric icon exploration and the launch films.',
  'cover': I('upi__snapmint-upi-b__upi-home-tpap-linked')},
 {'p': 'Credit Line on UPI', 'y': 'Landing page, flows, film',
  'b': 'Pay on any UPI app with a Snapmint credit line. The landing page, the activation flow from rough to final, and a series of explainer films.',
  'cover': I('upi__credit-line-on-intermediate-f__activate-credit-line')},
 {'p': 'Whitelabel Widget', 'y': 'Product design',
  'b': 'A pay-later widget and popup system that merchants drop into their storefronts, restyled to each brand.',
  'cover': I('wid__whitelabel-pop__man-matters')},
 {'p': 'GATTI', 'y': 'Identity, character animation', 'c': True,
  'b': 'A concept brand starring a mug character: identity, a pitch carousel and a set of character films.',
  'cover': I('gatti__films-v1-film1-not-a-mu__film1-not-a-mug-4x5-poster')},
 {'p': 'Buy the Way', 'y': 'Identity, editing',
  'b': 'Snapmint\'s podcast: logo exploration to final mark, cue cards and the trailer edit.',
  'cover': S('pod-final')},
 {'p': 'MokshaVastra', 'y': 'Brand, product graphics',
  'b': 'A devotional apparel label: logo, hero posters and the full run of product graphics.',
  'cover': I('mv__public-hero__adiyogi-poster')},
 {'p': 'ID Studio', 'y': 'Internal tool',
  'b': 'Company ID cards and new-joiner posts, automated so non-designers can make them on brand.',
  'cover': I('ids__public__og')},
]

# ---------- build ----------------------------------------------------------
def dur(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                         capture_output=True, text=True).stdout.strip()
    return round(float(out), 1)

def size_of(path):
    if path.endswith('.svg'):
        import re
        head = open(path).read(400)
        m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', head)
        return (round(float(m.group(1))), round(float(m.group(2))))
    return Image.open(path).size

for d in ('i', 'v', 'p', 's', 't'):
    os.makedirs(os.path.join(OUT_MEDIA, d), exist_ok=True)

missing = []
def resolve(m):
    """Copy the file, return the JS record."""
    if m['k'] == 'v':
        src = os.path.join(SRC, 'v', m['f'] + '.mp4'); poster = os.path.join(SRC, 'p', m['f'] + '.jpg')
        if not os.path.exists(src): missing.append(src); return None
        shutil.copy2(src, os.path.join(OUT_MEDIA, 'v', m['f'] + '.mp4'))
        shutil.copy2(poster, os.path.join(OUT_MEDIA, 'p', m['f'] + '.jpg'))
        w, h = Image.open(poster).size
        rec = {'v': f"/media/v/{m['f']}.mp4", 'src': f"/media/p/{m['f']}.jpg", 'w': w, 'h': h,
               'd': dur(src)}
        thumb_src = poster
    else:
        sub = 'i' if m['k'] == 'i' else 'svg'
        src = os.path.join(SRC, sub, m['f'])
        if not os.path.exists(src): missing.append(src); return None
        dst_dir = 'i' if m['k'] == 'i' else 's'
        shutil.copy2(src, os.path.join(OUT_MEDIA, dst_dir, m['f']))
        w, h = size_of(src)
        rec = {'src': f"/media/{dst_dir}/{m['f']}", 'w': w, 'h': h}
        thumb_src = src if m['k'] == 'i' else None
    if m.get('cap'): rec['cap'] = m['cap']
    # Small cover thumbnail (raster only)
    if thumb_src:
        name = os.path.splitext(os.path.basename(thumb_src))[0] + '.webp'
        tp = os.path.join(OUT_MEDIA, 't', name)
        if not os.path.exists(tp):
            im = Image.open(thumb_src); im.thumbnail((640, 800))
            if im.mode not in ('RGB', 'RGBA'): im = im.convert('RGBA')
            im.save(tp, 'WEBP', quality=78)
        rec['t'] = f"/media/t/{name}"
    return rec

data = []
for disc, types in WORK.items():
    for typ, items in types.items():
        for it in items:
            media = [r for r in (resolve(m) for m in it['m']) if r]
            data.append({'d': disc, 's': typ, 't': it['t'], 'p': it['p'], 'c': it['c'], 'n': it['n'], 'm': media})
projects = []
for pr in PROJECTS:
    rec = dict(pr); rec['cover'] = resolve(pr['cover']); projects.append(rec)

os.makedirs(os.path.join(ROOT, 'work'), exist_ok=True)
with open(os.path.join(ROOT, 'work', 'data.js'), 'w') as f:
    f.write('// Generated by scripts/build_work_site.py\n')
    f.write('window.DISCIPLINES = ' + json.dumps(list(WORK.keys())) + ';\n')
    f.write('window.TYPES = ' + json.dumps({d: list(t.keys()) for d, t in WORK.items()}) + ';\n')
    f.write('window.WORK = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
    f.write('window.PROJECTS = ' + json.dumps(projects, ensure_ascii=False, separators=(',', ':')) + ';\n')

os.makedirs(os.path.join(ROOT, 'resume'), exist_ok=True)
shutil.copy2(os.path.join(SRC, 'Harsh-Vishvakarma-Resume.pdf'), os.path.join(ROOT, 'resume', 'Harsh-Vishvakarma-Resume.pdf'))

print('items', len(data), 'media', sum(len(d['m']) for d in data), 'missing', missing)
