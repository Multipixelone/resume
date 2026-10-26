import test from 'node:test';
import assert from 'node:assert/strict';
import { registerHooks } from 'node:module';

// Exercise the production wrapper with the Kit 3 pathname contract at both mounts.
for (const base of ['', '/resume']) {
  test(`sitePath preserves paths and encoding at ${base || '/'} mount`, async () => {
    const hooks = registerHooks({
      resolve(specifier, context, nextResolve) {
        if (specifier === '$app/paths') {
          return { url: `test:app-paths${base}`, shortCircuit: true };
        }
        return nextResolve(specifier, context);
      },
      load(url, context, nextLoad) {
        if (url === `test:app-paths${base}`) {
          return { format: 'module', shortCircuit: true, source: `
            export function resolve(path) {
              if (path.startsWith('/')) throw new Error('Kit 3 pathnames have no leading slash');
              return ${JSON.stringify(base)} + '/' + path;
            }
          ` };
        }
        return nextLoad(url, context);
      }
    });
    try {
      const { sitePath } = await import(`../src/lib/paths.js?mount=${base}`);
      for (const [path, expected] of [
        ['/', '/'],
        ['/resume/', '/resume/'],
        ['/shows/example/', '/shows/example/'],
        ['/resumes/FINN RUTIS.pdf', '/resumes/FINN%20RUTIS.pdf'],
        ['/media/Résumé 日本語.png', '/media/R%C3%A9sum%C3%A9%20%E6%97%A5%E6%9C%AC%E8%AA%9E.png'],
        ['/media/100%.png', '/media/100%25.png'],
        ['/nested/file', '/nested/file']
      ]) assert.equal(sitePath(path), base + expected);
      for (const path of [null, undefined, 42, '', 'relative', '//other.test',
        'https://other.test/', '/a/../b', '/./a', '/a?query', '/a#hash', '/a\\b']) {
        assert.throws(() => sitePath(path), TypeError, String(path));
      }
    } finally {
      hooks.deregister();
    }
  });
}
