import {
  BoxGeometry, CanvasTexture, Color, DataTexture, DirectionalLight, Group,
  LinearFilter, LinearMipmapLinearFilter, Mesh, MeshLambertMaterial, NoToneMapping, PerspectiveCamera,
  PlaneGeometry, RepeatWrapping, RGBAFormat, Scene, ShaderMaterial,
  SRGBColorSpace, WebGLRenderer, AmbientLight
} from 'three';
import type { Texture } from 'three';
import { createLinkProjection } from './links.js';

export type CardPose = { x: number; y: number; z: number; lift: number };
export type CardScene = ReturnType<typeof createCardScene>;

/** A small scene. The component owns animation, visibility and input. */
export function createCardScene(canvas: HTMLCanvasElement, front: HTMLImageElement, back: HTMLImageElement) {
  const renderer = new WebGLRenderer({ canvas, alpha: true, antialias: true, powerPreference: 'low-power' });
  renderer.setClearColor(0x000000, 0);
  renderer.outputColorSpace = SRGBColorSpace;
  renderer.toneMapping = NoToneMapping;

  const scene = new Scene();
  const camera = new PerspectiveCamera(11, 1.42, 0.1, 30);
  // A longer viewing distance keeps the near corner from looking enlarged.
  // Resize adjusts the field of view to preserve the card's overall size.
  camera.position.z = 16;
  const textures: Texture[] = [];
  const projectLinks = createLinkProjection();
  let drawingBounds = { width: 0, height: 0, left: 0, top: 0 };

  // Uncoated stock has a little variation even in flat light. Keep this in
  // the paper layer so the exported lettering and QR remain untouched.
  const size = 256;
  const paper = document.createElement('canvas');
  paper.width = paper.height = size;
  const paperContext = paper.getContext('2d');
  if (!paperContext) throw new Error('Paper texture canvas unavailable');
  const paperPixels = paperContext.createImageData(size, size);
  const grain = new Uint8Array(size * size * 4);
  let seed = 41;
  const random = () => {
    seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
    return seed / 0x100000000;
  };
  const pulp = Array.from({ length: 256 }, () => random() - 0.5);
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const cellX = x >> 4;
      const cellY = y >> 4;
      const tx = (x % 16) / 16;
      const ty = (y % 16) / 16;
      const sx = tx * tx * (3 - 2 * tx);
      const sy = ty * ty * (3 - 2 * ty);
      const sample = (dx: number, dy: number) => pulp[((cellY + dy) % 16) * 16 + (cellX + dx) % 16];
      const top = sample(0, 0) * (1 - sx) + sample(1, 0) * sx;
      const bottom = sample(0, 1) * (1 - sx) + sample(1, 1) * sx;
      const height = (random() - 0.5) * 48 + (top * (1 - sy) + bottom * sy) * 40;
      const index = (y * size + x) * 4;
      const shade = height * 0.09;
      paperPixels.data.set([252 + shade, 250 + shade, 245 + shade, 255], index);
      const value = Math.round(128 + height);
      grain.set([value, value, value, 255], index);
    }
  }
  paperContext.putImageData(paperPixels, 0, 0);
  paperContext.strokeStyle = 'rgba(111, 100, 86, 0.09)';
  paperContext.lineWidth = 0.4;
  paperContext.lineCap = 'round';
  for (let fiber = 0; fiber < 180; fiber++) {
    const x = 5 + random() * (size - 10);
    const y = 5 + random() * (size - 10);
    const angle = random() * Math.PI * 2;
    const length = 1.5 + random() * 4;
    paperContext.beginPath();
    paperContext.moveTo(x, y);
    paperContext.lineTo(x + Math.cos(angle) * length, y + Math.sin(angle) * length);
    paperContext.stroke();
  }

  function inkTexture(image: HTMLImageElement) {
    const surface = document.createElement('canvas');
    surface.width = image.naturalWidth;
    surface.height = image.naturalHeight;
    const context = surface.getContext('2d');
    if (!context) throw new Error('Card texture canvas unavailable');
    context.fillStyle = context.createPattern(paper, 'repeat') ?? '#fcfaf5';
    context.fillRect(0, 0, surface.width, surface.height);
    context.drawImage(image, 0, 0);
    const texture = new CanvasTexture(surface);
    texture.colorSpace = SRGBColorSpace;
    texture.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
    textures.push(texture);
    return texture;
  }

  // The same seeded pulp field supplies shallow relief. Mipmaps keep it from
  // sparkling when the card tilts or is drawn small on a phone.
  const relief = new DataTexture(grain, size, size, RGBAFormat);
  relief.wrapS = relief.wrapT = RepeatWrapping;
  relief.repeat.set(3.5, 2);
  relief.magFilter = LinearFilter;
  relief.minFilter = LinearMipmapLinearFilter;
  relief.generateMipmaps = true;
  relief.needsUpdate = true;
  textures.push(relief);

  // Lambert shading has no specular lobe: the ink and paper cannot acquire a
  // plastic highlight at grazing angles, even as the visitor turns the card.
  const stock = { reflectivity: 0, bumpMap: relief, bumpScale: 0.004 };
  const edge = new MeshLambertMaterial({ ...stock, color: '#d4c7ad', bumpScale: 0.001 });
  const face = new MeshLambertMaterial({ ...stock, map: inkTexture(front) });
  const reverse = new MeshLambertMaterial({ ...stock, map: inkTexture(back) });
  const geometry = new BoxGeometry(3.5, 2, 0.014, 40, 24, 1);
  // Almost imperceptible bow: it catches the light along a real stock edge.
  const positions = geometry.attributes.position;
  for (let index = 0; index < positions.count; index++) {
    const x = positions.getX(index) / 1.75;
    const y = positions.getY(index);
    positions.setZ(index, positions.getZ(index) + 0.009 * (x * x - 0.5) + 0.003 * y * y);
  }
  geometry.computeVertexNormals();
  const card = new Mesh(geometry, [edge, edge, edge, edge, face, reverse]);
  const hand = new Group();
  hand.add(card);
  scene.add(hand);

  scene.add(new AmbientLight(0xffffff, 2.75));
  const windowLight = new DirectionalLight(0xfff8ed, 0.6);
  windowLight.position.set(-3, 5, 8);
  scene.add(windowLight);
  const fill = new DirectionalLight(0xffffff, 0.25);
  fill.position.set(4, -1, -5);
  scene.add(fill);

  // An analytically blurred rectangle: as the projected card narrows, its
  // shadow loses density instead of collapsing into a dark strip. One draw
  // call, with no postprocessing or continuously updated shadow map.
  const shadowGeometry = new PlaneGeometry(6.4, 4.8);
  const shadowMaterial = new ShaderMaterial({
    transparent: true,
    depthWrite: false,
    uniforms: {
      ink: { value: new Color('#2b2520') },
      extent: { value: [1.7, 0.96] },
      softness: { value: 0.28 },
      strength: { value: 0.14 }
    },
    vertexShader: `varying vec2 point;
      void main() {
        point = position.xy;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }`,
    fragmentShader: `varying vec2 point;
      uniform vec3 ink;
      uniform vec2 extent;
      uniform float softness;
      uniform float strength;
      vec2 gaussianCDF(vec2 value) {
        vec2 t = 1.0 / (1.0 + 0.2316419 * abs(value));
        vec2 density = 0.39894228 * exp(-0.5 * value * value);
        vec2 tail = density * t * (0.31938153 + t * (-0.356563782
          + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))));
        return mix(tail, 1.0 - tail, step(0.0, value));
      }
      void main() {
        vec2 coverage = gaussianCDF((point + extent) / softness)
          - gaussianCDF((point - extent) / softness);
        float alpha = max(0.0, coverage.x * coverage.y) * strength;
        gl_FragColor = vec4(ink, alpha);
        #include <colorspace_fragment>
      }`
  });
  const shadow = new Mesh(shadowGeometry, shadowMaterial);
  shadow.position.set(0.12, -0.22, -0.8);
  // Keep the shadow's footprint at the page plane as perspective makes
  // objects farther from the camera smaller.
  shadow.scale.setScalar((camera.position.z - shadow.position.z) / camera.position.z);
  scene.add(shadow);

  return {
    resize(width: number, height: number, drawing: { width: number; height: number; left: number }) {
      drawingBounds = { ...drawing, top: (height - drawing.height) / 2 };
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      renderer.setSize(drawing.width, drawing.height, false);
      const viewWidth = Math.max(4.25, 2.9 * width / height);
      const viewHeight = viewWidth * height / width;
      camera.fov = 2 * Math.atan(viewHeight / (2 * camera.position.z)) * 180 / Math.PI;
      // Preserve the card's scale at z=0 while extending the perspective
      // frustum into the canvas bleed, including unequal viewport margins.
      camera.setViewOffset(width, height, drawing.left, (height - drawing.height) / 2,
        drawing.width, drawing.height);
    },
    render(pose: CardPose, floatHeight = 0) {
      hand.rotation.set(pose.x, 0, pose.z);
      hand.position.y = pose.lift * 0.035 + floatHeight;
      card.rotation.y = pose.y;
      const projectedWidth = Math.abs(Math.cos(pose.y));
      const turn = Math.abs(Math.sin(pose.y));
      shadowMaterial.uniforms.extent.value = [1.7 * projectedWidth + 0.007 * turn, 0.96 * Math.abs(Math.cos(pose.x))];
      shadowMaterial.uniforms.softness.value = 0.28 + pose.lift * 0.075 + turn * 0.1 + floatHeight * 0.55;
      shadowMaterial.uniforms.strength.value = (0.14 - pose.lift * 0.03 - floatHeight * 0.16)
        * (0.6 + 0.4 * projectedWidth);
      shadow.rotation.z = pose.z;
      shadow.position.y = -0.22 - pose.lift * 0.06 - floatHeight * 0.35;
      renderer.render(scene, camera);
      return projectLinks(card.matrixWorld, camera, drawingBounds);
    },
    dispose() {
      geometry.dispose();
      shadowGeometry.dispose();
      for (const material of [edge, face, reverse, shadowMaterial]) material.dispose();
      for (const texture of textures) texture.dispose();
      renderer.dispose();
      renderer.forceContextLoss();
    }
  };
}
