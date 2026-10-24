import test from 'node:test';
import assert from 'node:assert/strict';
import { angleDelta, deviceTilt, nearestFace, spring } from '../src/lib/business-card/motion.js';
import { Euler, Matrix4, PerspectiveCamera, Vector3 } from 'three';
import { createLinkProjection } from '../src/lib/business-card/links.js';

test('device tilt is relative to the hand and wraps the orientation seam', () => {
  assert.deepEqual(deviceTilt(55, -12, [55, -12], 0), { x: 0, y: 0 });
  assert.equal(angleDelta(-179, 179), 2);
  assert.equal(angleDelta(179, -179), -2);
  assert.deepEqual(deviceTilt(60, 13, [35, -12], 0), { x: 1, y: 1 });
  assert.deepEqual(deviceTilt(35.3, -12.4, [35, -12], 0), { x: 0, y: 0 });
});

test('landscape tilt rotates into screen axes and extreme readings are bounded', () => {
  const landscape = deviceTilt(60, -12, [35, -12], 90);
  assert.equal(landscape.x, 0);
  assert.equal(landscape.y, -1);
  const opposite = deviceTilt(60, -12, [35, -12], 270);
  assert.equal(opposite.x, 0);
  assert.equal(opposite.y, 1);
  assert.deepEqual(deviceTilt(145, 80, [35, -12], 0), { x: 1, y: 1 });
});

test('flip springs settle consistently at 30, 60, and 120 Hz without overshooting', () => {
  const results = [30, 60, 120].map(rate => {
    let value = 0;
    let velocity = 0;
    for (let frame = 0; frame < rate; frame++) {
      ({ value, velocity } = spring(value, velocity, Math.PI, 1 / rate));
      assert.ok(value >= 0 && value <= Math.PI);
    }
    assert.ok(Math.abs(value - Math.PI) < 0.0001);
    return value;
  });
  assert.ok(Math.abs(results[0] - results[2]) < 1e-10);
});

test('drag release picks the nearest readable side in either rotation direction', () => {
  assert.deepEqual(nearestFace(0.7), { rotation: 0, back: false });
  assert.deepEqual(nearestFace(2.4), { rotation: Math.PI, back: true });
  assert.deepEqual(nearestFace(-2.4), { rotation: -Math.PI, back: true });
  assert.deepEqual(nearestFace(5.8), { rotation: Math.PI * 2, back: false });
});

test('native contact targets follow the artwork through tilt, resize, and unequal canvas bleed', () => {
  const projectLinks = createLinkProjection();
  for (const width of [280, 350, 736]) {
    const height = width / 1.42;
    const drawing = { width: width + 80, height: height * 1.4, left: -20, top: -height * 0.2 };
    const camera = new PerspectiveCamera(11, width / height, 0.1, 30);
    camera.position.z = 16;
    camera.updateMatrixWorld();
    camera.setViewOffset(width, height, drawing.left, drawing.top, drawing.width, drawing.height);
    for (const yaw of [-0.4, 0, 0.4]) {
      const world = new Matrix4().makeRotationFromEuler(new Euler(0.2, yaw, -0.05));
      world.setPosition(0, 0.07, 0);
      const projection = projectLinks(world, camera, drawing);
      assert.equal(projection.frontFacing, true);
      assert.ok(projection.scale > 0);
      const css = new Matrix4().fromArray(projection.transform.slice(9, -1).split(',').map(Number));
      assert.notEqual(css.determinant(), 0, 'CSS transforms must remain invertible for hit testing');
      for (const [x, y] of [[650, 169], [995, 303], [650, 303], [995, 437]]) {
        const rendered = new Vector3(x / 300 - 1.75, 1 - y / 300, 0.008)
          .applyMatrix4(world).project(camera);
        const expectedX = drawing.left + (rendered.x + 1) * drawing.width / 2;
        const expectedY = drawing.top + (1 - rendered.y) * drawing.height / 2;
        const actual = new Vector3(x, y, 0).applyMatrix4(css);
        assert.ok(Math.abs(actual.x - expectedX) < 1e-8);
        assert.ok(Math.abs(actual.y - expectedY) < 1e-8);
      }
    }
  }
});

test('front contact links are unavailable on the back and near the thin edge', () => {
  const projectLinks = createLinkProjection();
  const camera = new PerspectiveCamera(11, 1.42, 0.1, 30);
  camera.position.z = 16;
  camera.updateMatrixWorld();
  const drawing = { width: 700, height: 500, left: 0, top: 0 };
  for (const yaw of [Math.PI / 2, Math.PI, -Math.PI, Math.PI * 1.5]) {
    assert.equal(projectLinks(new Matrix4().makeRotationY(yaw), camera, drawing).frontFacing, false);
  }
  assert.equal(projectLinks(new Matrix4().makeRotationY(Math.PI * 2), camera, drawing).frontFacing, true);
});
