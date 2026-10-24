/** @param {number} value @param {number} [limit] */
export const clamp = (value, limit = 1) => Math.max(-limit, Math.min(limit, value));

/** Shortest signed distance, including across the device's +/-180-degree seam.
 * @param {number} value @param {number} origin */
export function angleDelta(value, origin) {
  return ((value - origin + 540) % 360 + 360) % 360 - 180;
}

/** Map relative device tilt into screen axes, in portrait or landscape.
 * @param {number} beta @param {number} gamma
 * @param {[number, number]} origin @param {number} angle */
export function deviceTilt(beta, gamma, origin, angle) {
  const radians = angle * Math.PI / 180;
  const vertical = angleDelta(beta, origin[0]);
  const horizontal = angleDelta(gamma, origin[1]);
  const deadzone = (value) => Math.abs(value) < 0.6 ? 0 : clamp(value / 25);
  return {
    x: deadzone(vertical * Math.cos(radians) + horizontal * Math.sin(radians)),
    y: deadzone(horizontal * Math.cos(radians) - vertical * Math.sin(radians))
  };
}

/** Exact critically damped spring: independent of refresh rate, no flip overshoot.
 * @param {number} value @param {number} velocity @param {number} target
 * @param {number} seconds @param {number} [speed] */
export function spring(value, velocity, target, seconds, speed = 15) {
  const displacement = value - target;
  const decay = Math.exp(-speed * seconds);
  const term = velocity + speed * displacement;
  return {
    value: target + (displacement + term * seconds) * decay,
    velocity: (velocity - speed * term * seconds) * decay
  };
}

/** @param {number} rotation */
export function nearestFace(rotation) {
  const turns = Math.round(rotation / Math.PI);
  return { rotation: turns * Math.PI, back: Math.abs(turns % 2) === 1 };
}
