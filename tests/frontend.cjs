const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const read = file => fs.readFileSync(path.join(root, file), 'utf8');

function open(page, { theme, stored = null, blocked = false, reduced = false } = {}) {
    const html = read(`HTML/${page}.html`);
    const events = {}, handlers = {}, attributes = {}, timers = [];
    const selector = { value: '', addEventListener(name, fn) { handlers[name] = fn; } };
    let removed = false, visible = false;
    const explosion = html.includes('id="explosion"') ? {
        style: {}, remove() { removed = true; }, classList: { add() { visible = true; } }
    } : null;
    const links = ['index.html', 'diagnostico.html', 'drivers.html', 'red.html', 'https://example.com/index.html'].map(href => ({
        href, attrs: {}, getAttribute() { return this.href; }, closest() { return true; },
        setAttribute(k, v) { this.attrs[k] = v; }, removeAttribute(k) { delete this.attrs[k]; }
    }));
    const context = {
        URL, Set, Math,
        location: { href: `file:///C:/HTML/${page}.html${theme ? '?theme=' + theme : ''}`, pathname: `/C:/HTML/${page}.html` },
        localStorage: {
            getItem() { if (blocked) throw Error('Storage unavailable'); return stored; },
            setItem(k, value) { if (blocked) throw Error('Storage unavailable'); stored = value; }
        },
        setTimeout(fn) { timers.push(fn); },
        window: { matchMedia() { return { matches: reduced }; }, addEventListener(name, fn) { (events[name] ??= []).push(fn); } },
        document: {
            readyState: 'loading',
            getElementById(id) { return id === 'theme-selector' ? selector : id === 'explosion' ? explosion : null; },
            querySelectorAll(query) { return query === 'a[href]' ? links : []; },
            documentElement: { setAttribute(k, v) { attributes[k] = v; }, getAttribute(k) { return attributes[k]; } },
            body: { classList: { add() {}, remove() {} } }
        }
    };
    const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
    vm.runInNewContext(scripts.join('\n;\n'), context);
    for (const fn of events.load || []) fn();
    return { selector, handlers, links, attributes, timers, removed, visible, events, html };
}

for (const page of ['index', 'diagnostico', 'drivers', 'red']) {
    const p = open(page);
    assert.equal(p.selector.value, 'black');
    for (const theme of ['blue', 'violet', 'cosmos', 'grey', 'black']) {
        p.selector.value = theme;
        p.handlers.change();
        assert.equal(p.attributes['data-theme'], theme);
        for (const link of p.links.slice(0, 4)) assert.equal(new URL(link.href).searchParams.get('theme'), theme);
    }
    assert.equal(p.links[4].href, 'https://example.com/index.html');
    assert.equal(p.links.find(link => new URL(link.href).pathname.endsWith(`/${page}.html`)).attrs['aria-current'], 'page');
    assert.equal(p.visible, page === 'index');
    assert.equal(p.html.includes('id="explosion"'), page === 'index');
    if (page !== 'index') assert.equal(p.timers.length, 0);
    assert.equal(open(page, { theme: 'violet', stored: 'grey' }).selector.value, 'violet');
    assert.equal(open(page, { theme: 'invalid', stored: 'blue' }).selector.value, 'blue');
    const blocked = open(page, { theme: 'cosmos', blocked: true });
    for (const fn of blocked.events.pageshow || []) fn();
    assert.equal(blocked.selector.value, 'cosmos');
    console.log(`OK ${page}: five themes, local navigation, active link, blocked storage, explosion policy`);
}
assert.equal(open('index', { reduced: true }).removed, true);
console.log('OK reduced motion');
