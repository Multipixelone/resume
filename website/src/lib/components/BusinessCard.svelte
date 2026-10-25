<script lang="ts">
  import { onMount } from 'svelte';
  import { sitePath } from '$lib/paths';
  import { clamp, deviceTilt, nearestFace, spring } from '$lib/business-card/motion';
  import type { CardPose, CardScene } from '$lib/business-card/scene';

  const id = $props.id();
  let stage: HTMLDivElement;
  let contactLinks: HTMLDivElement;
  let canvas: HTMLCanvasElement;
  let frontImage: HTMLImageElement;
  let backImage: HTMLImageElement;
  let mounted = $state(false);
  let webgl = $state(false);
  let frontFacing = $state(false);
  let back = $state(false);
  let reduced = $state(false);
  let dragging = $state(false);
  let fine = $state(false);
  let tiltAvailable = $state(false);
  let tiltEnabled = $state(false);
  let tiltPending = $state(false);
  let message = $state('');
  let flip = () => { back = !back; };
  let toggleTilt = () => {};

  onMount(() => {
    mounted = true;
    const motionPreference = matchMedia('(prefers-reduced-motion: reduce)');
    const forcedColors = matchMedia('(forced-colors: active)');
    const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
    type OrientationAPI = typeof DeviceOrientationEvent & {
      requestPermission?: () => Promise<'granted' | 'denied'>;
    };
    const orientationAPI = window.DeviceOrientationEvent as OrientationAPI | undefined;
    let scene: CardScene | undefined;
    let loading = false;
    let failed = false;
    let destroyed = false;
    let visible = false;
    let frame = 0;
    let previousTime = 0;
    let floatTime = 0;
    let driftWeight = 1;
    let driftVelocity = 0;
    let faceRotation = 0;
    // The float plays one full figure eight, then rests until a hand returns.
    const floatCycle = 12;
    let floatBudget = floatCycle;
    let focused = false;
    let listening = false;
    let origin: [number, number] | undefined;
    let sensorTimeout: ReturnType<typeof setTimeout> | undefined;
    let suppressClick = false;
    let pointer: {
      id: number; x: number; y: number; rotation: number; moved: boolean;
      capture: HTMLElement; link: HTMLAnchorElement | null;
    } | undefined;
    // Keep the resting face close to frontal, with a small natural lean.
    const restingPose: CardPose = { x: 0.12, y: -0.14, z: -0.045, lift: 0 };
    const pose = { ...restingPose };
    const target = { ...pose };
    const velocity: CardPose = { x: 0, y: 0, z: 0, lift: 0 };
    const axes = ['x', 'y', 'z', 'lift'] as const;
    // Like the header ticket, a hand or keyboard focus squares the card up:
    // its lean eases out to a level face, nearly flat, lifted toward the viewer.
    const presentedPose: CardPose = { x: 0.03, y: 0, z: -0.017, lift: 0.55 };
    let presenting = false;
    let hovered = false;

    function cancelFrame() {
      cancelAnimationFrame(frame);
      frame = 0;
      previousTime = 0;
    }

    function requestFrame() {
      if (!frame && webgl && visible && !document.hidden && !destroyed) {
        frame = requestAnimationFrame(render);
      }
    }

    function render(time: number) {
      frame = 0;
      if (!scene || !webgl || !visible || document.hidden || destroyed) return;
      const elapsed = time - previousTime;
      const driftTarget = pointer || tiltEnabled || focused || floatBudget <= 0 || target.lift > 0
        || Math.abs(pose.y - target.y) > 0.02 ? 0 : 1;
      const responding = axes.some(axis => Math.abs(pose[axis] - target[axis]) > 0.00015
        || Math.abs(velocity[axis]) > 0.001)
        || Math.abs(driftWeight - driftTarget) > 0.00015 || Math.abs(driftVelocity) > 0.001;
      // The slow float only needs 30fps. Input and spring motion use the full
      // display rate, and no frame work runs while hidden or offscreen.
      if (!responding && previousTime && elapsed < 1000 / 30 - 0.5) {
        requestFrame();
        return;
      }
      const seconds = previousTime ? Math.min(elapsed / 1000, 0.064) : 1 / 60;
      previousTime = time;
      // Let the visitor's hand take over quickly, then bring the idle tilt
      // back more slowly. Keep this separate from the actual drag/flip pose.
      // Presenting eases the float out as slowly as it returns, so the card
      // settles into its straightened pose rather than stopping mid-sway.
      const drift = spring(driftWeight, driftVelocity, driftTarget, seconds, driftTarget || presenting ? 6 : 12);
      let moving = Math.abs(drift.value - driftTarget) > 0.00015 || Math.abs(drift.velocity) > 0.001;
      driftWeight = moving ? drift.value : driftTarget;
      driftVelocity = moving ? drift.velocity : 0;
      for (const axis of axes) {
        const next = spring(pose[axis], velocity[axis], target[axis], seconds, dragging ? 23 : presenting ? 8 : 14);
        pose[axis] = next.value;
        velocity[axis] = next.velocity;
        if (Math.abs(pose[axis] - target[axis]) > 0.00015 || Math.abs(next.velocity) > 0.001) {
          moving = true;
        } else {
          pose[axis] = target[axis];
          velocity[axis] = 0;
        }
      }
      // A 2:1 pitch/yaw rhythm traces a small figure eight over twelve seconds.
      // Its vertical float keeps the existing six-second cadence. Holding the
      // card freezes the phase; returning to it never jumps ahead in the loop.
      if (!pointer) floatTime = (floatTime + seconds) % 12;
      if (driftTarget) floatBudget -= seconds;
      const phase = floatTime * Math.PI / 6;
      const sway = Math.sin(phase);
      const rise = Math.sin(phase * 2);
      try {
        const links = scene.render({
          ...pose,
          x: pose.x + rise * 0.025 * driftWeight,
          y: pose.y + sway * 0.055 * driftWeight,
          z: pose.z + sway * 0.008 * driftWeight
        }, rise * 0.055);
        contactLinks.style.setProperty('--card-projection', links.transform);
        contactLinks.style.setProperty('--projected-scale', String(Math.max(0.01, links.scale)));
        frontFacing = links.frontFacing;
      } catch {
        fail();
        return;
      }
      if (moving || (!pointer && driftWeight > 0)) requestFrame();
      else previousTime = 0;
    }

    function wake() {
      floatBudget = floatCycle;
      requestFrame();
    }

    function present() {
      presenting = true;
      target.x = presentedPose.x;
      target.y = faceRotation + presentedPose.y;
      target.z = presentedPose.z;
      target.lift = presentedPose.lift;
      requestFrame();
    }

    function updatePresentation() {
      if ((hovered || focused) && !pointer && !tiltEnabled) present();
      else if (presenting) {
        presenting = false;
        rest();
        wake();
      }
    }

    function settle() {
      if (presenting) present();
      else rest();
    }

    function focusChanged() {
      focused = stage.matches(':focus-within');
      updatePresentation();
    }

    function rest() {
      target.x = restingPose.x;
      target.y = faceRotation + restingPose.y;
      target.z = restingPose.z;
      target.lift = 0;
      requestFrame();
    }

    function resize() {
      if (!scene) return;
      const bounds = stage.getBoundingClientRect();
      const { width, height } = bounds;
      if (width > 0 && height > 0) {
        // Let the shadow reach beyond the stage on every side. Clamp the
        // horizontal bleed to the viewport so phones never gain a scrollbar.
        const left = Math.min(width * 0.2, Math.max(0, bounds.left));
        const right = Math.min(width * 0.2, Math.max(0, document.documentElement.clientWidth - bounds.right));
        canvas.style.left = `${-left}px`;
        canvas.style.width = `${width + left + right}px`;
        const drawing = canvas.getBoundingClientRect();
        scene.resize(width, height, { width: drawing.width, height: drawing.height, left: drawing.left - bounds.left });
        requestFrame();
      }
    }

    function fail() {
      if (failed) return;
      failed = true;
      webgl = false;
      cancelFrame();
      stopTilt();
      tiltAvailable = false;
      scene?.dispose();
      scene = undefined;
      // The already-rendered ink and the HTML contact links stay usable.
    }

    async function initialize() {
      if (scene || loading || failed || reduced || forcedColors.matches || destroyed) return;
      loading = true;
      try {
        const [{ createCardScene }] = await Promise.all([
          import('$lib/business-card/scene'), frontImage.decode(), backImage.decode()
        ]);
        if (destroyed || reduced || forcedColors.matches) return;
        scene = createCardScene(canvas, frontImage, backImage);
        webgl = true;
        updateTiltAvailability();
        resize();
      } catch {
        if (!destroyed) fail();
      } finally {
        loading = false;
      }
    }

    flip = () => {
      if (destroyed) return;
      faceRotation = nearestFace(faceRotation).rotation + Math.PI;
      back = nearestFace(faceRotation).back;
      origin = undefined;
      settle();
    };

    function pointerDown(event: PointerEvent) {
      if (!event.isPrimary || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      const link = (event.target as Element).closest<HTMLAnchorElement>('.card-contact');
      const capture = link ?? stage;
      suppressClick = false;
      pointer = { id: event.pointerId, x: event.clientX, y: event.clientY, rotation: target.y, moved: false, capture, link };
      // A contact tap keeps native link focus and activation. Once it becomes
      // a drag, capture moves to the stage and navigation is suppressed.
      if (event.pointerType === 'mouse' && !link) event.preventDefault();
      capture.setPointerCapture(event.pointerId);
    }

    function pointerMove(event: PointerEvent) {
      const bounds = stage.getBoundingClientRect();
      if (pointer && pointer.id === event.pointerId) {
        const dx = event.clientX - pointer.x;
        const dy = event.clientY - pointer.y;
        if (Math.hypot(dx, dy) > 7) pointer.moved = true;
        if (pointer.moved && pointer.capture !== stage) {
          pointer.capture = stage;
          stage.setPointerCapture(event.pointerId);
        }
        if (!pointer.moved || !webgl || reduced) return;
        dragging = true;
        target.y = pointer.rotation + dx / bounds.width * Math.PI * 2;
        target.x = clamp(restingPose.x + dy / bounds.height, 0.55);
        target.z = restingPose.z + clamp(dx / bounds.width) * 0.06;
        target.lift = 1;
      } else if (webgl && !reduced && finePointer.matches && event.pointerType === 'mouse' && !tiltEnabled) {
        if (!hovered) {
          hovered = true;
          updatePresentation();
        }
        return;
      } else return;
      requestFrame();
    }

    function releasePointer(event: PointerEvent) {
      if (!pointer || pointer.id !== event.pointerId) return;
      if (event.type === 'lostpointercapture' && event.target !== pointer.capture) return;
      const { moved: wasDrag, capture, link } = pointer;
      pointer = undefined;
      dragging = false;
      floatBudget = floatCycle;
      suppressClick = wasDrag || event.type !== 'pointerup';
      if (capture.hasPointerCapture(event.pointerId)) capture.releasePointerCapture(event.pointerId);
      if (event.type === 'pointerup' && !wasDrag && !link) flip();
      else {
        const side = nearestFace(target.y);
        faceRotation = side.rotation;
        back = side.back;
        origin = undefined;
        presenting = false;
        updatePresentation();
        if (!presenting) rest();
      }
    }

    function preventDragNavigation(event: MouseEvent) {
      if (!suppressClick || event.detail === 0) return;
      event.preventDefault();
      event.stopPropagation();
      suppressClick = false;
    }

    function pointerLeave() {
      hovered = false;
      if (!pointer && !tiltEnabled) updatePresentation();
    }

    function screenAngle() {
      return window.screen.orientation?.angle ?? (window as Window & { orientation?: number }).orientation ?? 0;
    }

    function orient(event: DeviceOrientationEvent) {
      if (event.beta == null || event.gamma == null || !Number.isFinite(event.beta) || !Number.isFinite(event.gamma)) return;
      if (!tiltEnabled || !webgl || reduced || document.hidden || !visible || pointer) return;
      clearTimeout(sensorTimeout);
      tiltPending = false;
      message = '';
      origin ??= [event.beta, event.gamma];
      const tilt = deviceTilt(event.beta, event.gamma, origin, screenAngle());
      const x = restingPose.x + tilt.x * 0.22;
      const y = faceRotation + restingPose.y + tilt.y * 0.28;
      // Ignore small sensor jitter so it cannot twitch the resting angle.
      if (Math.abs(target.x - x) < 0.003 && Math.abs(target.y - y) < 0.003) return;
      target.x = x;
      target.y = y;
      target.lift = 0.4;
      requestFrame();
    }

    function detachSensor() {
      window.removeEventListener('deviceorientation', orient);
      listening = false;
      origin = undefined;
      clearTimeout(sensorTimeout);
    }

    function syncSensor() {
      const shouldListen = tiltEnabled && webgl && !reduced && visible && !document.hidden && !destroyed;
      if (!shouldListen) { detachSensor(); return; }
      if (listening) return;
      listening = true;
      window.addEventListener('deviceorientation', orient, { passive: true });
      sensorTimeout = setTimeout(() => {
        stopTilt();
        message = 'No motion data received. You can still drag or turn the card.';
      }, 4000);
    }

    function stopTilt() {
      tiltEnabled = false;
      tiltPending = false;
      detachSensor();
      rest();
    }

    toggleTilt = async () => {
      if (tiltEnabled) { stopTilt(); message = ''; return; }
      if (!tiltAvailable || tiltPending) return;
      tiltPending = true;
      message = '';
      try {
        // Call synchronously from the tap, before any other await: iOS requires
        // transient user activation. No compass (absolute orientation) access.
        const permission = orientationAPI?.requestPermission
          ? await orientationAPI.requestPermission() : 'granted';
        if (destroyed || reduced || forcedColors.matches || !webgl) return;
        if (permission !== 'granted') {
          message = 'Device tilt was not allowed. You can still drag or turn the card.';
          return;
        }
        tiltEnabled = true;
        message = 'Move your phone gently to tilt the card.';
        syncSensor();
      } catch {
        message = 'Device tilt is unavailable. You can still drag or turn the card.';
      } finally {
        tiltPending = false;
      }
    };

    function updateTiltAvailability() {
      fine = finePointer.matches;
      tiltAvailable = webgl && !reduced && !forcedColors.matches && window.isSecureContext
        && !!orientationAPI && (navigator.maxTouchPoints > 0 || !finePointer.matches);
    }

    function preferencesChanged() {
      reduced = motionPreference.matches;
      if (reduced || forcedColors.matches) {
        webgl = false;
        cancelFrame();
        stopTilt();
        message = '';
        pointer = undefined;
        dragging = false;
      } else if (scene) {
        webgl = true;
        rest();
        for (const axis of axes) { pose[axis] = target[axis]; velocity[axis] = 0; }
        resize();
      } else if (visible) void initialize();
      updateTiltAvailability();
    }

    function visibilityChanged() {
      if (document.hidden) {
        cancelFrame();
        pointer = undefined;
        dragging = false;
        rest();
      } else requestFrame();
      syncSensor();
    }

    function recalibrate() { origin = undefined; }
    function contextLost(event: Event) { event.preventDefault(); fail(); }
    const observer = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      if (visible) { void initialize(); requestFrame(); }
      else cancelFrame();
      syncSensor();
    });
    const resizer = new ResizeObserver(resize);
    observer.observe(stage);
    resizer.observe(stage);
    preferencesChanged();
    stage.addEventListener('pointerdown', pointerDown);
    stage.addEventListener('pointermove', pointerMove);
    stage.addEventListener('pointerup', releasePointer);
    stage.addEventListener('pointercancel', releasePointer);
    stage.addEventListener('lostpointercapture', releasePointer);
    stage.addEventListener('pointerleave', pointerLeave);
    stage.addEventListener('focusin', focusChanged);
    stage.addEventListener('focusout', focusChanged);
    stage.addEventListener('click', preventDragNavigation, true);
    canvas.addEventListener('webglcontextlost', contextLost);
    motionPreference.addEventListener('change', preferencesChanged);
    forcedColors.addEventListener('change', preferencesChanged);
    finePointer.addEventListener('change', updateTiltAvailability);
    document.addEventListener('visibilitychange', visibilityChanged);
    window.addEventListener('resize', resize, { passive: true });
    window.screen.orientation?.addEventListener('change', recalibrate);
    window.addEventListener('orientationchange', recalibrate);

    return () => {
      destroyed = true;
      cancelFrame();
      detachSensor();
      observer.disconnect();
      resizer.disconnect();
      stage.removeEventListener('pointerdown', pointerDown);
      stage.removeEventListener('pointermove', pointerMove);
      stage.removeEventListener('pointerup', releasePointer);
      stage.removeEventListener('pointercancel', releasePointer);
      stage.removeEventListener('lostpointercapture', releasePointer);
      stage.removeEventListener('pointerleave', pointerLeave);
      stage.removeEventListener('focusin', focusChanged);
      stage.removeEventListener('focusout', focusChanged);
      stage.removeEventListener('click', preventDragNavigation, true);
      canvas.removeEventListener('webglcontextlost', contextLost);
      motionPreference.removeEventListener('change', preferencesChanged);
      forcedColors.removeEventListener('change', preferencesChanged);
      finePointer.removeEventListener('change', updateTiltAvailability);
      document.removeEventListener('visibilitychange', visibilityChanged);
      window.removeEventListener('resize', resize);
      window.screen.orientation?.removeEventListener('change', recalibrate);
      window.removeEventListener('orientationchange', recalibrate);
      scene?.dispose();
    };
  });
</script>

<figure class="business-card" aria-label="Finn Rutis's business card">
  <div bind:this={stage} class="card-stage" class:interactive={mounted} class:dragging class:webgl>
    <button class="card-turn" type="button" disabled={!mounted}
      aria-label={back ? 'Show front of business card' : 'Turn business card over'}
      aria-describedby={`${id}-identity ${id}-instruction ${id}-side`}
      onclick={(event) => { if (event.detail === 0) flip(); }}>
      <span class="card-flat" aria-hidden={webgl}>
        <img bind:this={frontImage} hidden={back} src={sitePath('/cards/performance/front-web-ink.png')}
          width="1050" height="600" draggable="false"
          alt="Finn Rutis, they / them, musical theatre performer." />
        <!-- The headshot makes this the heavier texture; the visible front loads first. -->
        <img bind:this={backImage} hidden={!back} src={sitePath('/cards/performance/back-ink.png')}
          width="1050" height="600" draggable="false" fetchpriority="low"
          alt="Back of Finn Rutis's business card: Finn's headshot beside a QR code for https://finnrut.is." />
      </span>
      <canvas bind:this={canvas} aria-hidden="true"></canvas>
    </button>
    <div bind:this={contactLinks} class="card-links" hidden={back || (webgl && !frontFacing)}>
      <a class="card-contact card-email" href="mailto:me@finnrut.is" draggable="false"
        aria-label="Email Finn at me@finnrut.is"><span class="sr-only">me@finnrut.is</span></a>
      <a class="card-contact card-instagram" href="https://www.instagram.com/finnrutis/" draggable="false"
        aria-label="Instagram, @finnrutis"><span class="sr-only">@finnrutis</span></a>
    </div>
  </div>
  <figcaption class="card-caption">
    <span id={`${id}-identity`} class="sr-only">Finn Rutis, they / them, musical theatre performer.</span>
    <span class="card-instruction" id={`${id}-instruction`}>
      {#if webgl && !reduced}Drag to turn{' · '}{fine ? 'Click' : 'Tap'} to flip{:else if mounted}{fine ? 'Click' : 'Tap'} to flip{:else}Business card{/if}
    </span>
    <!-- Plain text beside the card's mailto, for webmail users who copy it. -->
    <span class="card-address">me@finnrut.is</span>
    <div class="card-actions" hidden={!mounted || !tiltAvailable}>
      {#if tiltAvailable}
        <button class="card-action card-tilt" type="button" onclick={() => toggleTilt()}
          aria-pressed={tiltEnabled} disabled={tiltPending}>
          <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="7" y="3" width="10" height="18" rx="2" /><path d="M10 17h4M3 8 1 12l2 4m18-8 2 4-2 4" /></svg>
          {tiltEnabled ? 'Turn off tilt' : 'Use device tilt'}
        </button>
      {/if}
    </div>
    <span id={`${id}-side`} class="sr-only" aria-live="polite">{back ? 'Headshot and QR back' : 'Contact front'}</span>
    <span class="card-status" role="status">{message}</span>
  </figcaption>
</figure>

<style>
  .business-card { min-width: 0; }
  .card-stage { container-type: inline-size; position: relative; width: 100%; aspect-ratio: 1.42; touch-action: pan-y pinch-zoom; user-select: none; -webkit-user-select: none; }
  .card-turn { position: absolute; inset: 0; width: 100%; height: 100%; margin: 0; padding: 0; border: 0; border-radius: 0; background: transparent; appearance: none; overflow: visible; cursor: inherit; }
  .card-stage.interactive { cursor: pointer; }
  .card-stage.webgl { cursor: grab; }
  .card-stage.dragging { cursor: grabbing; }
  .card-flat { position: absolute; width: 82.35%; left: 50%; top: 50%; transform: translate(-50%, -50%) rotate(-2.58deg); background: var(--ticket-paper); box-shadow: 0 2px 4px rgb(43 37 32 / .1), 5px 19px 32px -10px rgb(43 37 32 / .25); }
  .card-flat img { width: 100%; height: auto; }
  .card-flat img[hidden] { display: none; }
  .card-stage canvas { display: block; position: absolute; inset: -20% 0; width: 100%; height: 140%; opacity: 0; pointer-events: none; }
  .webgl canvas { opacity: 1; }
  .webgl .card-flat { opacity: 0; }
  /* Coordinates follow the approved 1050 x 600 artwork. The two hit areas
     meet between its contact rows, so 44px phone targets never overlap. */
  .card-links { --card-scale: 1; position: absolute; left: 50%; top: 50%; width: 1050em; height: 600em; font-size: calc(82.35cqw / 1050); transform: translate(-50%, -50%) rotate(-2.58deg); pointer-events: none; }
  .card-links[hidden] { display: none; }
  .webgl .card-links { --card-scale: var(--projected-scale, 1); left: 0; top: 0; font-size: 1px; transform-origin: 0 0; transform: var(--card-projection); }
  .card-contact { position: absolute; left: 650em; width: 345em; height: 134em; min-height: calc(44px / var(--card-scale)); pointer-events: auto; cursor: pointer; outline-offset: calc(3px / var(--card-scale)); }
  .card-email { bottom: 297em; }
  .card-instagram { top: 303em; }
  .card-contact::after { content: ''; position: absolute; left: 74em; height: calc(1px / var(--card-scale)); background: var(--accent); }
  .card-email::after { bottom: 28em; width: 253em; }
  .card-instagram::after { top: 73em; width: 187em; }
  .card-contact:hover::after { height: calc(2px / var(--card-scale)); background: var(--accent-hover); }
  .card-contact:focus-visible { outline-width: calc(3px / var(--card-scale)); }
  .dragging .card-contact { cursor: grabbing; }
  .card-caption { position: relative; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: .1rem 1rem; margin: -1rem 8.825% 0; }
  .card-instruction { color: var(--muted); font: .6875rem/1.6 var(--font-mono); letter-spacing: .015em; }
  .card-address { color: var(--muted); font: .6875rem/1.6 var(--font-mono); letter-spacing: .015em; user-select: all; -webkit-user-select: all; }
  .card-actions { display: flex; flex-wrap: wrap; gap: 0 1.25rem; }
  .card-actions[hidden] { display: none; }
  .card-action { display: inline-flex; align-items: center; justify-content: center; gap: .4rem; min-height: 44px; padding: .5rem 0; border: 0; background: transparent; color: var(--accent); text-decoration: underline; text-underline-offset: .2em; font-size: 1rem; }
  .card-action:hover { color: var(--accent-hover); text-decoration-thickness: 2px; }
  .card-action:disabled { color: var(--muted); cursor: wait; }
  .card-action svg { width: 1rem; height: 1rem; fill: none; stroke: currentColor; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; flex: none; }
  .card-tilt[aria-pressed='true'] { color: var(--accent-hover); }
  .card-status { flex-basis: 100%; color: var(--muted); font-size: .9375rem; line-height: 1.5; }
  .card-status:empty { display: none; }
  .sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; border: 0; }
  @media (max-width: 40em) {
    .card-caption { margin-top: -.5rem; gap: .15rem .75rem; }
    .card-actions { gap: 0 1rem; }
    .card-instruction { flex-basis: 100%; }
  }
  @media (prefers-reduced-motion: reduce) {
    .card-stage.interactive { cursor: pointer; }
    .card-flat, .card-links { transform: translate(-50%, -50%); }
  }
  @media (forced-colors: active) {
    .card-stage canvas { display: none; }
    .card-flat, .webgl .card-flat { opacity: 1; background: var(--ticket-paper); forced-color-adjust: none; box-shadow: none; border: 1px solid CanvasText; transform: translate(-50%, -50%); }
    .card-links { transform: translate(-50%, -50%); }
    .card-contact { display: flex; align-items: center; padding: 2px; background: Canvas; color: LinkText; }
    .card-contact::after { display: none; }
    .card-contact .sr-only { position: static; width: auto; height: auto; margin: 0; overflow: visible; clip-path: none; white-space: normal; overflow-wrap: anywhere; font: 1rem/1.3 var(--font-body); }
    .card-action { color: LinkText; }
  }
</style>
