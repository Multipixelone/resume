import { Matrix4, Vector3 } from 'three';

/** Map native links in the 1050 x 600 artwork onto the rendered card.
 * The slight paper bow is below a pixel at this scale; the links use its plane.
 */
export function createLinkProjection() {
  const artwork = new Matrix4().set(
    3.5 / 1050, 0, 0, -1.75,
    0, -2 / 600, 0, 1,
    0, 0, 1, 0.008,
    0, 0, 0, 1
  );
  const viewport = new Matrix4();
  const matrix = new Matrix4();
  const normal = new Vector3();
  const left = new Vector3();
  const right = new Vector3();
  const top = new Vector3();
  const bottom = new Vector3();

  /** @param {Matrix4} world
   * @param {import('three').Camera} camera
   * @param {{width: number, height: number, left: number, top: number}} drawing
   */
  return (world, camera, drawing) => {
    viewport.set(
      drawing.width / 2, 0, 0, drawing.left + drawing.width / 2,
      0, -drawing.height / 2, 0, drawing.top + drawing.height / 2,
      0, 0, 1, 0,
      0, 0, 0, 1
    );
    matrix.copy(viewport).multiply(camera.projectionMatrix)
      .multiply(camera.matrixWorldInverse).multiply(world).multiply(artwork);
    normal.set(0, 0, 1).transformDirection(world);
    left.set(650, 303, 0).applyMatrix4(matrix);
    right.set(995, 303, 0).applyMatrix4(matrix);
    top.set(822.5, 169, 0).applyMatrix4(matrix);
    bottom.set(822.5, 437, 0).applyMatrix4(matrix);
    return {
      transform: `matrix3d(${matrix.elements.join(',')})`,
      scale: Math.min(
        Math.hypot(right.x - left.x, right.y - left.y) / 345,
        Math.hypot(bottom.x - top.x, bottom.y - top.y) / 268
      ),
      frontFacing: normal.z > 0.35
    };
  };
}
