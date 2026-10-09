// Case-study content for World of Somnath v2. Facts come from the project folders,
// their READMEs/docs, and Harsh's own notes. No invented metrics.
(() => {
const I = k => '/media/i/' + k + '.webp';
const S = k => '/media/s/' + k + '.svg';
const V = k => ({ v: '/media/v/' + k + '.mp4', p: '/media/p/' + k + '.jpg' });
const X = (site, f) => '/media/sites/' + site + '/' + f + '.webp';
const WL = f => '/media/wl/' + f + '.webp';

const CASES = [
// ─────────────────────────────────────────────── 01
{
  slug: 'snapmint-upi', n: '01', title: 'Snapmint UPI', short: 'Snapmint UPI',
  kicker: 'Product design · Icons · Motion · Film',
  line: 'Turning a pay-later shopping app into a place you pay from every day.',
  bg: '#ff6f00', fg: '#fff', acc: '#ffd23f',
  facts: [['Role', 'Design owner'], ['Scope', 'UI, icons, motion, launch films'], ['Company', 'Snapmint'], ['Status', 'Shipped (icons: concept)']],
  hero: [
    { k: 'phone', m: I('upi__headers-interm__home-app'), x: '8%', y: '10%', w: 250, rot: -6, par: .18 },
    { k: 'phone', m: I('upi__snapmint-upi-b__upi-home-tpap-linked'), x: '38%', y: '0%', w: 290, rot: 0, par: .08 },
    { k: 'phone', m: I('upi__snapmint-upi-b__secure-login'), x: '68%', y: '12%', w: 250, rot: 6, par: .22 },
  ],
  tile: { c: 7, rw: 3, art: [
    { k: 'phone', m: I('upi__headers-interm__home-app'), x: '46%', y: '16%', w: 150, rot: -8, hx: '-12px', hrot: '-10deg' },
    { k: 'phone', m: I('upi__snapmint-upi-b__upi-home-tpap-linked'), x: '68%', y: '6%', w: 170, rot: 4, hy: '-16px' },
    { k: 'img', m: S('upi-logo'), x: '8%', y: '22%', w: '22%', rot: -8 },
  ], tags: ['Product', 'Film'] },
  sections: [
    { t: 'lede', eyebrow: 'The brief', h: 'UPI, inside the app people already trusted for EMIs.',
      p: 'Snapmint added UPI payments to its shopping app. I designed how UPI lives on the home screen, how you switch between shopping and paying, the secure login, the icon system, the app icon, and the films that launched it.' },
    { t: 'ba', eyebrow: 'Home screen · before / after', h: 'Same brief. Two directions.',
      p: 'An agency proposed the first home. I reworked it so Shop and UPI sit in one switch at the top, the available credit is always one glance away, and the category rail does the browsing.',
      before: { m: I('upi__headers-propos__home-app'), label: 'Agency proposal' }, after: { m: I('upi__headers-interm__home-app'), label: 'My direction' } },
    { t: 'scrolly', dark: true, eyebrow: 'Walkthrough', frame: 'phone', steps: [
      { h: 'One header, two modes.', p: 'Shop and UPI live in the same app, separated by a single switch, with the credit limit pinned beside it.', m: I('upi__headers-interm__home-app') },
      { h: 'Scan & Pay in the thumb zone.', p: 'The bottom navigation was rebuilt around a raised Scan & Pay button. This version is live in the app.', m: I('upi__upi-bottom-nav__home') },
      { h: 'Biometric secure login.', p: 'A calm, single-purpose lock screen for the moment money moves.', m: I('upi__snapmint-upi-b__secure-login') },
      { h: 'After you link a UPI app.', p: 'The home re-arranges itself around send, scan, history and balance once an account is linked.', m: I('upi__snapmint-upi-b__upi-home-tpap-linked') },
      { h: 'Headers for both worlds.', p: 'Final header artwork for the Snapmint shopping home and the UPI home.', m: I('upi__final-headers__snapmint-home-4x') },
    ] },
    { t: 'ba', flip: true, eyebrow: 'Icons · concept', h: 'From flat glyphs to a 3D icon family.',
      p: 'An exploration for first-time UPI users: chunky, isometric icons in the brand orange and navy, so each action reads at a glance. Not shipped yet.', concept: true,
      before: { m: I('upi__upi-homepage-i__home-upi-first-time-oldicon'), label: 'Current icons' }, after: { m: I('upi__upi-homepage-i__home-upi-first-time-user-proposed-icon'), label: 'Proposed' } },
    { t: 'rail', eyebrow: 'Icon system', h: 'Eight objects, one light source.', frame: 'sq', items: [
      { m: S('ic-scan'), cap: 'Scan & Pay' }, { m: S('ic-send'), cap: 'Send money' }, { m: S('ic-history'), cap: 'History' }, { m: S('ic-wallet'), cap: 'Wallet' },
      { m: S('ic-recharge'), cap: 'Recharge' }, { m: S('ic-plane'), cap: 'Flights (in production)' }, { m: S('ic-bus'), cap: 'Bus (in production)' }, { m: S('ic-train'), cap: 'Trains (in production)' },
    ] },
    { t: 'films', dark: true, eyebrow: 'Launch films', h: 'Then I made people want to try it.',
      p: 'I made the launch films too, from script to final cut.', items: [
        { m: V('upi-app'), cap: 'Snapmint UPI app film' }, { m: V('upi-ai'), cap: 'UPI with Pay Later, AI film' },
      ] },
    { t: 'gallery', eyebrow: 'Brand pieces', h: 'The mark on your home screen.', items: [
      { m: S('upi-logo'), cap: 'Snapmint UPI app icon', s: 4, contain: true },
      { m: I('upi__upi-homepage-i__gradient1-5'), cap: 'Isometric exploration, gradient study', s: 8 },
    ] },
  ],
},
// ─────────────────────────────────────────────── 02
{
  slug: 'credit-line-on-upi', n: '02', title: 'Credit Line on UPI', short: 'Credit Line on UPI',
  kicker: 'Flows · Landing page · AI film campaign',
  line: 'A credit line with no card. You spend it from any UPI app and pay next month.',
  bg: '#0e3b2c', fg: '#f4f1e8', acc: '#9be15d',
  facts: [['Role', 'Product + campaign design'], ['Scope', 'Activation flow, landing page, films'], ['Company', 'Snapmint'], ['Status', 'Shipped']],
  hero: [
    { k: 'phone', m: I('upi__credit-line-on-intermediate-f__activate-credit-line'), x: '10%', y: '8%', w: 260, rot: -5, par: .2 },
    { k: 'phone', k2: 'video', m: V('upi-link'), x: '40%', y: '0%', w: 290, rot: 0, par: .06 },
    { k: 'phone', m: I('upi__credit-line-on-intermediate-f__activate-credit-line-2'), x: '68%', y: '10%', w: 260, rot: 5, par: .24 },
  ],
  tile: { c: 5, rw: 3, art: [
    { k: 'phone', m: I('upi__credit-line-on-intermediate-f__activate-credit-line'), x: '14%', y: '10%', w: 150, rot: -6 },
    { k: 'phone', m: I('upi__credit-line-on-intermediate-f__activate-credit-line-1'), x: '50%', y: '18%', w: 150, rot: 6, hy: '-18px' },
  ], tags: ['Product', 'AI film'] },
  sections: [
    { t: 'lede', eyebrow: 'The product', h: 'Credit, without the plastic.',
      p: 'Snapmint\'s Credit Line on UPI is a digital credit line that you link inside a UPI app and spend anywhere UPI works. My job was to make activation feel like a two-minute thing, then explain it to people who had never heard of it.' },
    { t: 'scrolly', eyebrow: 'Activation flow', frame: 'phone', steps: [
      { h: 'It started rough.', p: 'Nineteen rough screens to find the shape of onboarding: what to ask, in what order, and what to promise up front.', m: I('upi__credit-line-on-rough-credit-l__activate-credit-line-3') },
      { h: 'Then it got short.', p: 'The pre-rebrand flow cut it down to a single promise: spend everywhere, pay next month.', m: I('upi__credit-line-on-intermediate-f__activate-credit-line') },
      { h: 'Ask only what credit needs.', p: 'PAN and email, with the approval promise right under the field.', m: I('upi__credit-line-on-intermediate-f__activate-credit-line-1') },
      { h: 'Say how it works, in three lines.', p: 'Get instant credit, open a bank account in one tap, pay on any UPI app.', m: I('upi__credit-line-on-intermediate-f__activate-credit-line-2') },
    ] },
    { t: 'tall', eyebrow: 'Landing page', h: 'One long scroll that sells it.', p: 'The Credit Line on UPI landing page, shown here scrolling as you scroll.', frame: 'phone', m: I('upi__credit-line-on-final__clou-landing-page') },
    { t: 'rail', dark: true, eyebrow: 'The rough pass', h: 'Explorations before the flow settled.', frame: 'phone', items:
      [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12].map(n => ({ m: I('upi__credit-line-on-rough-credit-l__activate-credit-line-' + n) })) },
    { t: 'films', eyebrow: 'Campaign', h: 'A campaign to explain one product.',
      p: 'An AI video campaign with 10+ scene variations, mixing live action and 2D animation, made with tools like Veo 3 and Seedance and finished by me.', items: [
        { m: V('upi-link'), cap: 'Link your credit line' }, { m: V('upi-repay'), cap: 'How to repay' }, { m: V('clou-hindi'), cap: 'Hindi film' },
      ] },
    { t: 'wides', eyebrow: 'Where to spend it', items: [
      { m: V('clou-intro'), cap: 'Intro' }, { m: V('clou-amazon'), cap: 'Pay on Amazon' }, { m: V('clou-gpay'), cap: 'Pay with GPay' }, { m: V('clou-phonepe'), cap: 'Pay with PhonePe' },
    ] },
  ],
},
// ─────────────────────────────────────────────── 03
{
  slug: 'checkout-and-onboarding', n: '03', title: 'Checkout & Onboarding', short: 'Checkout',
  kicker: 'Product design · Before / after · Motion',
  line: 'Every Snapmint purchase passes through these screens. I redesigned them.',
  bg: '#2340d9', fg: '#fff', acc: '#f5c400',
  facts: [['Role', 'Product designer'], ['Scope', 'Login, OTP, checkout, wait states, confirmation'], ['Company', 'Snapmint'], ['Status', 'Onboarding shipped · checkout concept']],
  hero: [
    { k: 'phone', m: I('onb__new-before-reb__login-mobile-number'), x: '10%', y: '8%', w: 250, rot: -5, par: .2 },
    { k: 'phone', m: I('co__snapmint-check__iphone-13-14-128'), x: '39%', y: '0%', w: 290, rot: 0, par: .06 },
    { k: 'phone', m: I('oc__initial'), x: '68%', y: '10%', w: 250, rot: 5, par: .24 },
  ],
  tile: { c: 4, rw: 3, art: [
    { k: 'phone', m: I('co__snapmint-check__iphone-13-14-128'), x: '10%', y: '8%', w: 140, rot: -7 },
    { k: 'phone', m: I('oc__initial'), x: '48%', y: '20%', w: 140, rot: 6, hy: '-16px' },
  ], tags: ['Product', 'Before/after'] },
  sections: [
    { t: 'lede', eyebrow: 'The journey', h: 'From typing your number to “order confirmed”.',
      p: 'Login, OTP, checkout, the wait while an order processes, and the confirmation. These are the screens every shopper sees on every purchase, so small fixes compound. Onboarding shipped; the checkout redesign is designed end to end and waiting for engineering time.' },
    { t: 'ba', eyebrow: 'Onboarding · before / after', h: 'A login that tells you why.',
      p: 'The old screen was a bare number field. The new one leads with what you get, a credit limit, and keeps the form to one field and one button.',
      before: { m: I('onb__old__mobile-number-filled'), label: 'Before' }, after: { m: I('onb__new-before-reb__login-mobile-number'), label: 'After' } },
    { t: 'rail', eyebrow: 'Edge cases', h: 'The unhappy paths got design too.', frame: 'phone', items: [
      { m: I('onb__new-before-reb__login-mobile-number-1'), cap: 'Number entered' }, { m: I('onb__new-before-reb__login-mobile-number-2'), cap: 'Ready to send' },
      { m: I('onb__new-before-reb__error-otp'), cap: 'Wrong OTP' }, { m: I('onb__new-before-reb__error-otp-1'), cap: 'Retry state' }, { m: I('onb__new-before-reb__error-otp-2'), cap: 'Locked out' },
    ] },
    { t: 'ba', flip: true, dark: true, concept: true, eyebrow: 'Checkout · concept', h: 'Checkout, rebuilt around the EMI.',
      p: 'The current checkout opens on an OTP wall. The redesign shows the order, the pay-now amount and the plan first, then asks for the OTP.',
      before: { m: I('co__snapmint-cheko__checkout-snapmint-com-otp-mobile-9742472'), label: 'Live today' }, after: { m: I('co__snapmint-check__iphone-13-14-128'), label: 'Proposed' } },
    { t: 'rail', dark: true, eyebrow: 'Checkout · final proposal', h: 'Ten screens, end to end.', frame: 'phone', items:
      [128, 129, 130, 131, 132, 133, 134, 135, 136, 137].map(n => ({ m: I('co__snapmint-check__iphone-13-14-' + n) })) },
    { t: 'films', eyebrow: 'Waiting, designed', h: 'Splash screens and loaders.',
      p: 'The rebranded splash is built around a receipt tearing open to reveal the orange brand. The loaders keep people calm while an order is approved.', items: [
        { m: V('splash-a'), cap: 'Splash, version A' }, { m: V('splash-b'), cap: 'Splash, version B' }, { m: V('loader-processing'), cap: 'Processing loader', contain: true }, { m: V('loader-pie'), cap: '0% EMI loader', contain: true },
      ] },
    { t: 'ba', eyebrow: 'Order confirmation', h: 'The happiest screen in the app.',
      p: 'The confirmation that shipped, next to an exploration that was turned down: a fuller order overview with rewards.',
      before: { m: I('oc__initial'), label: 'Shipped' }, after: { m: I('oc__intermeddiate-__frame-48097907'), label: 'Exploration' } },
  ],
},
// ─────────────────────────────────────────────── 04
{
  slug: 'whitelabel-widget', n: '04', title: 'White-label Pay Later', short: 'White-label widget',
  kicker: 'Design system · Merchant widgets',
  line: 'One pay-later widget that becomes part of every merchant\'s store.',
  bg: '#f6efe2', fg: '#17150f', acc: '#234a87',
  facts: [['Role', 'Product designer'], ['Scope', 'PDP widget, popup, cart strip, OTP'], ['Merchants shown', 'Seven'], ['Format', 'Mobile web']],
  hero: [
    { k: 'img', m: WL('andamen-popup'), x: '4%', y: '6%', w: '24%', rot: -5, par: .22 },
    { k: 'img', m: WL('manmatters-popup'), x: '28%', y: '0%', w: '24%', rot: 2, par: .1 },
    { k: 'img', m: WL('decorshed-popup'), x: '52%', y: '8%', w: '22%', rot: -2, par: .18 },
    { k: 'img', m: WL('controlz-popup'), x: '75%', y: '2%', w: '21%', rot: 5, par: .26 },
  ],
  tile: { c: 8, rw: 2, art: [
    { k: 'img', m: WL('manmatters-popup'), x: '3%', y: '20%', w: '19%', rot: -6 },
    { k: 'img', m: WL('andamen-popup'), x: '23%', y: '8%', w: '20%', rot: 3, hy: '-16px' },
    { k: 'img', m: WL('decorshed-popup'), x: '44%', y: '18%', w: '18%', rot: -3 },
    { k: 'img', m: WL('controlz-popup'), x: '63%', y: '6%', w: '17%', rot: 5, hy: '-14px' },
  ], tags: ['Design system'] },
  sections: [
    { t: 'lede', eyebrow: 'The idea', h: 'Same structure. Their brand.',
      p: 'Snapmint\'s pay-later offer sits on merchant product pages and in their carts. Instead of one Snapmint-orange box everywhere, I designed it as a system: the same layout and logic, re-skinned in each merchant\'s colours, type and logo, so it feels native to their store.' },
    { t: 'switcher', eyebrow: 'Try it', h: 'Pick a merchant.', brands: [
      { id: 'manmatters', name: 'Man Matters', c: '#234a87', extra: 'more', extraLabel: 'Wellness report' },
      { id: 'andamen', name: 'Andamen', c: '#a56e2e', extra: 'bag', extraLabel: 'Cart drawer' },
      { id: 'onecarat', name: 'One Carat', c: '#2b2d50', extra: 'otp', extraLabel: 'OTP step' },
      { id: 'glen', name: 'Glen', c: '#2f6df0', extra: 'cart', extraLabel: 'Cart' },
      { id: 'controlz', name: 'ControlZ', c: '#0000ff', extra: null },
      { id: 'decorshed', name: 'Decorshed', c: '#ec6a3a', extra: 'cart', extraLabel: 'Cart' },
      { id: 'reise', name: 'Reise Moto', c: '#f2c12e', extra: null },
    ] },
    { t: 'facts', eyebrow: 'What stays fixed', h: 'The system underneath.', items: [
      ['3', 'parts: the inline PDP strip, the explainer popup, the cart strip'],
      ['1', 'layout grid every merchant inherits'],
      ['2', 'popup patterns: EMI pie charts, or option cards with a lead form'],
      ['0', 'Snapmint orange forced onto anyone\'s store'],
    ] },
    { t: 'gallery', dark: true, eyebrow: 'Reise Moto', h: 'Teaching it on the store, too.', items: [
      { m: WL('reise-explainer'), cap: 'How-to-use explainer for Reise Moto Pay Later', s: 6 },
      { m: WL('reise-popup'), cap: 'Popup with lead form', s: 3 },
      { m: WL('reise-widget'), cap: 'Inline widget', s: 3 },
    ] },
  ],
},
// ─────────────────────────────────────────────── 05
{
  slug: 'mokshavastra', n: '05', title: 'MokshaVastra', short: 'MokshaVastra',
  kicker: 'My clothing brand · Identity · Catalogue · Store',
  line: 'Spiritual streetwear. My own label, built end to end, from the logo to the checkout.',
  bg: '#0b0b0a', fg: '#f4ead8', acc: '#e8a33d',
  facts: [['Role', 'Founder · designer · developer'], ['Catalogue', '19 pieces, 5 collections'], ['Store', 'Custom Next.js, Razorpay'], ['Status', 'Live']],
  links: [['Visit the store', 'https://mokshavastra.store']],
  hero: [
    { k: 'img', m: I('mv__public-products__mahabali-back-cut'), x: '2%', y: '14%', w: '30%', rot: -8, par: .25, free: true },
    { k: 'phone', m: X('mokshavastra', 'mobile-home'), x: '38%', y: '0%', w: 280, rot: 0, par: .06 },
    { k: 'img', m: I('mv__public-products__adiyogi-back-cut'), x: '66%', y: '10%', w: '30%', rot: 8, par: .2, free: true },
  ],
  tile: { c: 4, rw: 4, art: [
    { k: 'img', m: I('mv__public-products__mahabali-back-cut'), x: '-6%', y: '24%', w: '70%', rot: -8, free: true },
    { k: 'phone', m: X('mokshavastra', 'mobile-home'), x: '50%', y: '8%', w: 150, rot: 6, hy: '-16px' },
  ], tags: ['Brand', 'E-com'] },
  sections: [
    { t: 'lede', dark: true, eyebrow: 'Moksha — liberation. Vastra — garment.', h: 'Clothing for the inner journey.',
      p: 'MokshaVastra is my oversized streetwear label rooted in Indian mythology. I designed the identity and every graphic, and built the store myself, with no Shopify: phone-OTP login, Razorpay checkout and partial cash-on-delivery.' },
    { t: 'flips', dark: true, eyebrow: 'The catalogue', h: 'Hover a piece to turn it around.', items:
      ['mahabali', 'adiyogi', 'kali-tandav', 'shiva-trinetra', 'krishna-leela', 'hanuman-gada', 'vighnaharta', 'om-namah-shivay', 'saarthi-krishna', 'janm-mrityu', 'bhakt', 'kali', 'kundalini', '108-hoodie', 'astral-hoodie', 'bhairavi-hoodie', 'nritya-shiva-hoodie', 'shiva-hoodie', 'kundalini-hoodie']
        .map(k => ({ k, name: k.replace(/-hoodie$/, '').split('-').map(w => w[0].toUpperCase() + w.slice(1)).join(' '), type: /hoodie/.test(k) ? 'Hoodie' : 'Oversized tee',
          front: I('mv__public-products__' + k + '-front-cut'), back: I('mv__public-products__' + k + '-back-cut') })) },
    { t: 'scrolly', dark: true, eyebrow: 'The store', frame: 'phone', steps: [
      { h: 'Opens on a film, not a banner.', p: 'A full-screen product film per drop, with a swipe between pieces and a tap through to buy.', m: X('mokshavastra', 'mobile-home') },
      { h: 'Five paths.', p: 'Mahadev, Shakti, Saarthi, Kundalini and Bhakti. Each collection has its own colour and story.', m: X('mokshavastra', 'mobile-collections') },
      { h: 'Every piece has a story.', p: 'A Sanskrit name, the myth behind the graphic, sizes and a delivery check by pincode.', m: X('mokshavastra', 'mobile-product-buy') },
      { h: 'Know the story, earn the discount.', p: 'The Katha Challenge: answer three questions about the myth to unlock up to 10% off.', m: X('mokshavastra', 'mobile-product-full'), tall: true },
      { h: 'Cash on delivery that kills fake orders.', p: 'Pay ₹199 online now, the rest at the door. Or one-tap Razorpay Magic Checkout.', m: X('mokshavastra', 'mobile-checkout') },
    ] },
    { t: 'gallery', dark: true, eyebrow: 'Identity & film', h: 'The mark and the drops.', items: [
      { m: I('mv__public-hero__mahabali-poster'), cap: 'Mahabali drop', s: 3 },
      { m: I('mv__public-hero__adiyogi-poster'), cap: 'Adiyogi drop', s: 3 },
      { m: S('mv-logo-white'), cap: 'Wordmark', s: 6, contain: true, darkbg: true },
    ] },
    { t: 'facts', eyebrow: 'Under the hood', h: 'A store I can run alone.', items: [
      ['19', 'pieces across 13 tees and 6 hoodies'], ['5', 'themed collections, each with its own colour'], ['₹199', 'online token on COD orders to stop fake orders'], ['₹0', 'monthly infrastructure on free tiers'],
    ] },
  ],
},
// ─────────────────────────────────────────────── 06
{
  slug: 'ajay-sanjay', n: '06', title: 'Ajay Sanjay', short: 'Ajay Sanjay',
  kicker: 'Commerce platform · Designed and built',
  line: 'One grocery business, one stock ledger, two very different customers.',
  bg: '#ffd23f', fg: '#151a17', acc: '#008632',
  facts: [['Role', 'Product owner · designer · builder'], ['Surfaces', 'Shop, trade portal, staff app, control centre'], ['Client', 'Ajay Sanjay, Raigarh'], ['Status', 'Live']],
  links: [['Visit ajaysanjay.com', 'https://ajaysanjay.com']],
  hero: [
    { k: 'browser', m: X('ajay', 'desktop-home-hero'), url: 'ajaysanjay.com', x: '4%', y: '6%', w: '62%', rot: -2, par: .12 },
    { k: 'phone', m: X('ajay', 'mobile-home-hero'), x: '62%', y: '0%', w: 260, rot: 4, par: .22 },
  ],
  tile: { c: 8, rw: 3, art: [
    { k: 'browser', m: X('ajay', 'desktop-home-hero'), url: 'ajaysanjay.com', x: '4%', y: '14%', w: '62%', rot: -3 },
    { k: 'phone', m: X('ajay', 'mobile-product-added'), x: '66%', y: '6%', w: 160, rot: 5, hy: '-16px' },
  ], tags: ['Web app', 'Built it'] },
  sections: [
    { t: 'lede', eyebrow: 'The problem', h: 'A kirana supplier wanted to sell to households too.',
      p: 'Ajay Sanjay sells groceries, spices and dry fruit from one counter in Raigarh. It started as an invite-only trade system for shops. Then the owner wanted Blinkit-style home delivery from the same stock. I designed and built the platform that serves both without mixing them up.' },
    { t: 'quote', q: 'These are not the same customer wearing different hats, and the most expensive mistake available here is to build them as though they were.', by: 'From the project\'s product-decision log' },
    { t: 'compare', eyebrow: 'Two-audience model', h: 'Shared catalogue. Separate everything else.', head: ['', 'Retailer', 'Household'], rows: [
      ['Price', 'Negotiated per account, hidden until sign-in', 'One published price, visible to anyone'],
      ['Buying', 'Request → quotation → confirm → order', 'Add to cart → checkout'],
      ['Payment', 'Credit, settled against a statement', 'Cash or UPI at the door'],
      ['Identity', 'Invited account, 6-digit Store PIN', 'A mobile number at checkout'],
      ['Quantity', 'Cases, bags and tins', 'One packet'],
    ] },
    { t: 'tall', eyebrow: 'The shop', h: 'Big pictures, a price you see at once, one tap to add.', p: 'The household shop, benchmarked against Blinkit and Zepto. It scrolls as you scroll.', frame: 'browser', url: 'ajaysanjay.com', m: X('ajay', 'desktop-home'), side: X('ajay', 'mobile-product-added') },
    { t: 'rail', eyebrow: 'On the phone', h: 'Built for one-handed shopping.', frame: 'phone', items: [
      { m: X('ajay', 'mobile-home-hero'), cap: 'Home with seasonal campaign' }, { m: X('ajay', 'mobile-category-dry-fruits'), cap: 'Dry fruits' }, { m: X('ajay', 'mobile-search'), cap: 'Search: “kaju”' },
      { m: X('ajay', 'mobile-product-added'), cap: 'Added: the button becomes a stepper' }, { m: X('ajay', 'mobile-cart'), cap: 'Cart with WhatsApp and call options' }, { m: X('ajay', 'mobile-trade'), cap: 'Trade storefront' },
    ] },
    { t: 'scrolly', dark: true, eyebrow: 'Behind the counter', frame: 'browser', steps: [
      { h: 'Trade, invite-only.', p: 'Retailers sign in with a mobile number and a Store PIN. Accounts are opened by the team, not a signup form.', m: X('ajay', 'desktop-retailer-login'), url: 'retailer.ajaysanjay.com' },
      { h: 'A control centre that splits the two.', p: 'Every number is reported separately for households and for trade. (Local build with demo data.)', m: X('ajay', 'desktop-admin-dashboard'), url: 'admin.ajaysanjay.com' },
      { h: 'Seasonal storefronts.', p: 'Festive Bachat, Mewa Mela, Shaadi Season: the owner switches the whole shop\'s mood from one screen.', m: X('ajay', 'desktop-admin-storefront'), url: 'admin.ajaysanjay.com' },
      { h: 'WhatsApp, with a human in the loop.', p: 'The system prepares the message; a person sends it from the official app and confirms. Nothing is claimed as delivered that wasn\'t.', m: X('ajay', 'desktop-admin-whatsapp'), url: 'admin.ajaysanjay.com' },
    ] },
    { t: 'gallery', eyebrow: 'House packs', h: 'When there\'s no photo, it gets a pack — never a fake one.', items:
      ['atta', 'rice', 'dal', 'oil', 'chilli', 'salt'].map(k => ({ m: I('ws__apps-web-public-assets-products-house__ajay-sanjay-' + k), cap: 'Ajay Sanjay ' + k, s: 2 })) },
    { t: 'facts', eyebrow: 'By the numbers', h: 'What\'s live today.', items: [
      ['452', 'products on the live trade page'], ['586', 'pack sizes'], ['57', 'brands across 18 categories'], ['1,143', 'automated tests passing (9 Sep)'],
    ] },
  ],
},
// ─────────────────────────────────────────────── 07
{
  slug: 'id-studio', n: '07', title: 'ID Studio', short: 'ID Studio',
  kicker: 'Internal tool · Designed and built',
  line: 'ID cards that design themselves, and arrive print-ready.',
  bg: '#fff3e6', fg: '#17150f', acc: '#ff6f00',
  facts: [['Role', 'Designer · builder'], ['Users', 'Every new joiner, and HR'], ['Output', 'PDF/X-4, CR80, 3 mm bleed'], ['Company', 'Snapmint']],
  hero: [
    { k: 'img', m: X('idstudio', '50-card-aarav-credit-advisory-front'), x: '6%', y: '10%', w: '20%', rot: -8, par: .24 },
    { k: 'browser', m: X('idstudio', '04-portrait-studio-desktop'), url: 'ID Studio', x: '24%', y: '0%', w: '54%', rot: 0, par: .08 },
    { k: 'img', m: X('idstudio', '50-card-meera-financial-services-front'), x: '76%', y: '12%', w: '20%', rot: 8, par: .26 },
  ],
  tile: { c: 4, rw: 2, art: [
    { k: 'img', m: X('idstudio', '50-card-aarav-credit-advisory-front'), x: '18%', y: '10%', w: '30%', rot: -8 },
    { k: 'img', m: X('idstudio', '50-card-meera-financial-services-front'), x: '50%', y: '16%', w: '30%', rot: 7, hy: '-16px' },
  ], tags: ['Tool', 'Built it'] },
  sections: [
    { t: 'lede', eyebrow: 'The problem', h: 'Every ID card was laid out by hand. And the artwork wasn\'t print-safe.',
      p: 'Collecting details and photos and laying out each card by hand took a designer\'s time. The supplied card files were also 3.5× too big for an ID card, with text inside the safe margin. ID Studio fixes both: employees make their own card, and the tool outputs files a print vendor can use as-is.' },
    { t: 'scrolly', eyebrow: 'Five short steps', frame: 'browser', steps: [
      { h: 'Which Snapmint do you work for?', p: 'Two entities, two colours. The choice drives the whole card.', m: X('idstudio', '01-entity-step-desktop'), url: 'ID Studio · Company' },
      { h: 'A portrait studio in the browser.', p: 'The background is removed on the device, the face is found and fitted, and you can drag and zoom inside a head-safe frame.', m: X('idstudio', '04-portrait-studio-desktop'), url: 'ID Studio · Photo' },
      { h: 'Details, formatted for you.', p: 'Names, IDs and phone numbers are cleaned up the same way in the browser, the API, an edge function and the database.', m: X('idstudio', '05-details-step-desktop'), url: 'ID Studio · Details' },
      { h: 'Three emojis. Exactly three.', p: '“Core vibes” and “side quests” — a bit of personality on the back of every card.', m: X('idstudio', '06b-emoji-picker-open-desktop'), url: 'ID Studio · Vibes' },
      { h: 'A live card, the whole way.', p: 'Front and back update as you type, so there are no surprises at print.', m: X('idstudio', '08-live-preview-back-desktop'), url: 'ID Studio · Preview' },
      { h: 'HR gets a print queue.', p: 'Review states, search, entity override, CSV, single PDFs and ZIP print packs.', m: X('idstudio', '22-hr-submissions-desktop'), url: 'ID Studio · HR' },
    ] },
    { t: 'gallery', dark: true, eyebrow: 'The output', h: 'Cards for both entities, and a post for LinkedIn.', items: [
      { m: X('idstudio', '51-cards-both-entities-front-back'), cap: 'Credit Advisory (orange) and Financial Services (green), front and back', s: 12 },
      { m: X('idstudio', '30-linkedin-newjoiner-slide1-1080'), cap: 'LinkedIn new-joiner card, slide 1', s: 6 },
      { m: X('idstudio', '31-linkedin-newjoiner-slide2-1080'), cap: 'Slide 2: “Snapster at heart”', s: 6 },
      { m: X('idstudio', '40-print-pdf-front-with-cropmarks'), cap: 'Print PDF with crop marks and bleed', s: 6 },
      { m: X('idstudio', '41-print-pdf-back-with-cropmarks'), cap: 'Back, print PDF', s: 6 },
    ] },
    { t: 'facts', eyebrow: 'Print spec, automated', h: 'What the vendor receives.', items: [
      ['CR80', '53.98 × 85.60 mm card trim'], ['3 mm', 'bleed, built by extending edge pixels'], ['PDF/X-4', 'CMYK with FOGRA39 output intent'], ['5', 'steps for the employee, about two minutes'],
    ] },
    { t: 'note', p: 'Screens show fictional sample employees and placeholder portraits.' },
  ],
},
// ─────────────────────────────────────────────── 08
{
  slug: 'qr-studio', n: '08', title: 'QR Studio', short: 'QR Studio',
  kicker: 'Internal tool · Designed and built',
  line: 'One merchant ID in. A finished, verified QR poster out.',
  bg: '#1a1814', fg: '#f6f1e7', acc: '#ff6b2b',
  facts: [['Role', 'Designer · builder'], ['Users', 'Snapmint\'s offline team'], ['Cost', '₹0/month on free tiers'], ['Company', 'Snapmint']],
  hero: [
    { k: 'browser', m: X('qrstudio', 'desktop-login'), url: 'qrlab-atlas.vercel.app', x: '6%', y: '4%', w: '58%', rot: -2, par: .1 },
    { k: 'img', m: I('qr__snapmint-rebrandedqr-mannunalwork'), x: '64%', y: '0%', w: '22%', rot: 5, par: .24 },
    { k: 'img', m: I('qr__co-branded-qr__5295-omaxechandnichowk-delhincr'), x: '78%', y: '14%', w: '18%', rot: 10, par: .3 },
  ],
  tile: { c: 4, rw: 2, art: [
    { k: 'img', m: I('qr__snapmint-rebrandedqr-mannunalwork'), x: '14%', y: '12%', w: '34%', rot: -7 },
    { k: 'img', m: I('qr__co-branded-qr__5295-omaxechandnichowk-delhincr'), x: '48%', y: '18%', w: '32%', rot: 6, hy: '-16px' },
  ], tags: ['Tool', 'Built it'] },
  sections: [
    { t: 'lede', eyebrow: 'The problem', h: 'Every store QR was made by hand in Figma.',
      p: 'Snapmint\'s offline team puts QR posters and tent cards in partner stores. Each one needs that merchant\'s own checkout link inside the QR. Making them one by one in Figma was slow and easy to get wrong.' },
    { t: 'flow', eyebrow: 'How it works', h: 'MID in. Poster out.', items: [
      ['Input', 'One merchant ID, pasted rows, or an Excel file. Columns are matched even when headers vary.'],
      ['Generate', 'Builds the checkout link and draws the QR at the highest error correction.'],
      ['Compose', 'Drops the QR, logo and credit limit into colour-coded zones on the brand\'s template.'],
      ['Validate', 'Reads the QR back from the finished image. Only an exact match is marked verified.'],
      ['Output', 'Single PNGs or a ZIP of the whole batch, plus a library and an audit log.'],
    ] },
    { t: 'scrolly', dark: true, eyebrow: 'The app', frame: 'browser', steps: [
      { h: '“One MID. One poster. Done.”', p: 'The sign-in screen states the whole job. Only @snapmint.com accounts, approved by an admin.', m: X('qrstudio', 'desktop-login'), url: 'qrlab-atlas.vercel.app' },
      { h: 'Drop in a spreadsheet.', p: 'Excel, CSV or pasted rows. Invalid IDs are skipped with a note, not a crash.', m: X('qrstudio', 'desktop-studio-excel-upload'), url: 'Studio · Excel' },
      { h: 'Brands and templates.', p: 'Admins manage brand logos, templates and preset EMI amounts for tent cards.', m: X('qrstudio', 'desktop-admin-brands'), url: 'Admin · Brands' },
      { h: 'Every setting in one place.', p: 'QR dot style, label position, pill rotation, resolution and URL templates, all tunable without code.', m: X('qrstudio', 'desktop-admin-render-settings'), url: 'Admin · Render settings' },
      { h: 'An audit trail nobody can edit.', p: 'Logins, approvals, edits and generations are logged append-only and exportable.', m: X('qrstudio', 'desktop-admin-activity-audit'), url: 'Admin · Activity' },
      { h: '⌘K for everything.', p: 'Keyboard-first for the people who make hundreds a day.', m: X('qrstudio', 'desktop-command-palette'), url: 'Command palette' },
    ] },
    { t: 'gallery', eyebrow: 'In stores', h: 'What ends up on the counter.', items: [
      { m: I('qr__snapmint-rebrandedqr-mannunalwork'), cap: 'Rebranded store QR', s: 4 },
      { m: I('qr__co-branded-qr__5295-omaxechandnichowk-delhincr'), cap: 'Co-branded store QR', s: 4 },
      { m: I('qr__iniitial-desig__a4-1'), cap: 'Early A4 design', s: 4 },
      { m: I('standee__standee-final-6'), cap: 'In-store standee', s: 6 },
      { m: I('standee__duroflex-standee-2'), cap: 'Duroflex standee', s: 6 },
    ] },
    { t: 'note', p: 'App screens are from a local build with demo users and data.' },
  ],
},
// ─────────────────────────────────────────────── 09
{
  slug: 'gatti', n: '09', title: 'GATTI', short: 'GATTI', concept: true,
  kicker: 'Concept company · Brand · Character films · Website',
  line: 'Culture, made solid. A concept company that prints the moments at work people actually want to keep.',
  bg: '#ff5fa2', fg: '#17150f', acc: '#ffd23f',
  facts: [['Role', 'Everything: idea, brand, films, site'], ['Launch film', '2 min 18 s, 4,128 frames'], ['Cast', 'Six characters'], ['Status', 'Concept']],
  hero: [
    { k: 'img', m: I('gatti__films-v1-film1-not-a-mu__film1-not-a-mug-4x5-poster'), x: '6%', y: '8%', w: '24%', rot: -6, par: .22 },
    { k: 'wide', m: V('gatti-v31'), x: '30%', y: '0%', w: '42%', rot: 0, par: .08 },
    { k: 'img', m: I('gatti__films-v3-1__launch-v3-1-mug-mountain-4x5-poster'), x: '72%', y: '10%', w: '22%', rot: 6, par: .26 },
  ],
  tile: { c: 6, rw: 3, art: [
    { k: 'img', m: I('gatti__films-v1-film1-not-a-mu__film1-not-a-mug-4x5-poster'), x: '6%', y: '10%', w: '38%', rot: -6 },
    { k: 'img', m: I('gatti__films-v1-film3-blinkit__film3-blinkit-4x5-poster'), x: '46%', y: '16%', w: '36%', rot: 6, hy: '-16px' },
  ], tags: ['Concept', 'Animation'] },
  sections: [
    { t: 'lede', eyebrow: 'The idea', h: 'Nobody makes a mug for shipping the big one.',
      p: 'Companies mark big moments with welcome mugs that end up on a pile. GATTI is a concept company I invented to turn real moments at work into objects people keep. I wrote it, designed the brand and characters, animated the films and built the website.' },
    { t: 'wide', dark: true, eyebrow: 'Launch film · v3.1', h: 'Meera and the mug mountain.', p: 'Fifteen scenes at 150 BPM: day-one mug, a year of pens, the mug mountain, the night she ships, and the medal nobody else made.', m: V('gatti-v31') },
    { t: 'films', eyebrow: 'Pitch films', h: 'Same character, three brands\' big days.', ratio: '4/5', items: [
      { m: V('gatti-bl'), cap: 'It\'s Diwali week' }, { m: V('gatti-fk'), cap: 'It\'s Big Billion Days' }, { m: V('gatti-me'), cap: 'Mega Blockbuster Sale' }, { m: V('gatti-15'), cap: 'What is GATTI, 15 s' },
    ] },
    { t: 'tall', eyebrow: 'Website', h: 'A site that reads like a zine.', p: 'The GATTI website, scrolling as you scroll.', frame: 'browser', url: 'GATTI website', m: X('gatti', 'desktop-full'), side: X('gatti', 'mobile-home') },
    { t: 'rail', dark: true, eyebrow: 'Pitch carousel', h: 'Eleven slides for LinkedIn.', frame: 'card45', items:
      Array.from({ length: 11 }, (_, i) => ({ m: I('gatti__pitch-round2-linkedin-carou-slides__slide-' + String(i + 1).padStart(2, '0')) })) },
    { t: 'films', eyebrow: 'More cuts', h: 'Shorts and earlier versions.', ratio: '16/9', items: [
      { m: V('gatti-short'), cap: 'The Mug Quits' }, { m: V('gatti-v1'), cap: 'Hi, I\'m the welcome mug' }, { m: V('gatti-v2'), cap: 'Culture made solid, v2' },
    ] },
  ],
},
// ─────────────────────────────────────────────── 10
{
  slug: 'buy-the-way', n: '10', title: 'Buy the Way', short: 'Buy the Way',
  kicker: 'Podcast identity · Edit',
  line: 'Snapmint\'s podcast, from the first logo sketch to the trailer cut.',
  bg: '#111', fg: '#fff', acc: '#ff6f00',
  facts: [['Role', 'Identity, cue cards, trailer edit'], ['Show', 'Buy the Way, by Snapmint'], ['Logo rounds', '17 explorations'], ['Status', 'Live']],
  hero: [
    { k: 'img', m: S('pod-final'), x: '10%', y: '4%', w: '34%', rot: -6, par: .2, free: true },
    { k: 'phone', k2: 'video', m: V('pod-trailer'), x: '50%', y: '0%', w: 270, rot: 4, par: .08 },
  ],
  tile: { c: 6, rw: 2, art: [
    { k: 'img', m: S('pod-final'), x: '8%', y: '6%', w: '42%', rot: -6, free: true },
    { k: 'phone', k2: 'video', m: V('pod-trailer'), x: '58%', y: '8%', w: 140, rot: 5, hy: '-16px' },
  ], tags: ['Identity', 'Edit'] },
  sections: [
    { t: 'lede', dark: true, eyebrow: 'The show', h: 'A podcast, branded from scratch.',
      p: 'Buy the Way is Snapmint\'s podcast. I designed its identity, the on-set cue cards and edited the trailer.' },
    { t: 'gallery', eyebrow: 'Logo exploration', h: 'Seventeen rounds to one mark.', items:
      ['pod-01', 'pod-02', 'pod-04', 'pod-06', 'pod-08', 'pod-09', 'pod-11', 'pod-13', 'pod-15', 'pod-16', 'pod-17'].map(k => ({ m: S(k), s: 2, contain: true }))
        .concat([{ m: S('pod-final'), cap: 'Final', s: 2, contain: true, hl: true }]) },
    { t: 'gallery', dark: true, eyebrow: 'On set', h: 'Cue cards for the conversation.', items: [
      { m: I('pod__podcast-cuecar__frame-13'), cap: 'Question card', s: 6 }, { m: I('pod__podcast-cuecar__frame-14'), cap: 'Logo card', s: 6 },
    ] },
    { t: 'films', eyebrow: 'Trailer', h: 'Forty seconds to make you press play.', items: [{ m: V('pod-trailer'), cap: 'Superkicks episode trailer' }] },
    { t: 'yt', eyebrow: 'Full episode', h: 'Watch the episode.', id: 'B8Pv1Dv7Q3U' },
  ],
},
];

window.CASES = CASES;
})();
