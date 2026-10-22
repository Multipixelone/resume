<script lang="ts">
  import { onMount } from 'svelte';
  import { watchCurrentShows } from '$shows';
  import { sitePath } from '$lib/paths';
  import { paperMotion } from '$lib/motion';
  import Arrow from './Arrow.svelte';
  import type { Show, CurrentShow } from '$lib/types';

  let { shows, watchOptions }: {
    shows: Show[];
    watchOptions?: Parameters<typeof watchCurrentShows>[2];
  } = $props();
  let current = $state<CurrentShow[]>([]);
  let today = $state('');

  // Empty during SSR, even if a build happens during a production's run.
  // Test harnesses can inject the shared watcher's clock/timer options; no URL/debug state.
  onMount(() => watchCurrentShows(shows, (next: CurrentShow[], date: string) => {
    current = next;
    today = date;
  }, watchOptions));

  // Presentation only: format the validated date without converting it to a visitor timezone.
  const format = (options: Intl.DateTimeFormatOptions) => {
    const formatter = new Intl.DateTimeFormat('en-US', { ...options, timeZone: 'UTC' });
    return (iso: string) => formatter.format(new Date(`${iso}T12:00:00Z`));
  };
  const weekday = format({ weekday: 'short' });
  const monthDay = format({ month: 'short', day: 'numeric' });
  const year = format({ year: 'numeric' });

  const oneNight = (show: CurrentShow) => show.performance_start === show.closing_night;
  function statusLabel(show: CurrentShow) {
    if (show.status === 'rehearsing') return 'In rehearsal';
    if (oneNight(show)) return 'Tonight';
    if (today === show.performance_start) return 'Opening night';
    if (today === show.closing_night) return 'Closing night';
    return 'Now playing';
  }
</script>

{#if current.length}
  <section class="now-showing section-block" aria-labelledby="current-title">
    <h2 id="current-title" class="now-heading">{current.length === 1 ? 'Current project' : 'Current projects'}.</h2>
    {#each current as show (show.id)}
      {@const id = `show-${encodeURIComponent(show.id)}`}
      <article class="now-show" aria-labelledby={id}>
        <div class="now-copy">
          <p class="now-status">{statusLabel(show)}</p>
          <h3 {id}>{show.title}</h3>
          <dl class="now-credits">
            <!-- A cabaret singer billed as "Self" is the convention on paper, but says nothing here. -->
            {#if show.character !== 'Self'}
              <div><dt>Role</dt><dd>{show.character}</dd></div>
            {/if}
            <div><dt>Venue</dt><dd>{show.company}</dd></div>
            <div><dt>Directed by</dt><dd>{show.director}</dd></div>
          </dl>
        </div>

        <div class="now-aside" use:paperMotion>
          {#if show.photo}
            <img class="now-photo" src={sitePath(show.photo)} alt={show.photo_alt ?? ''} loading="lazy" decoding="async" />
          {/if}
          <svelte:element
            this={show.ticket_url ? 'a' : 'div'}
            class="now-stub-shadow"
            class:now-stub-link={!!show.ticket_url}
            href={show.ticket_url}
            aria-labelledby={show.ticket_url ? `${id}-tickets ${id} ${id}-date ${id}-run${show.livestream ? ` ${id}-stream` : ''}` : undefined}
            data-paper-arrival
          >
            <div class="now-stub">
              <span class="stub-admit" aria-hidden="true">Admit one</span>
              <div class="stub-body">
                <time id={`${id}-date`} class="stub-date" datetime={show.performance_start}>
                  <span class="stub-day">{monthDay(show.performance_start)}</span>
                  <span class="stub-detail">{weekday(show.performance_start)} / {year(show.performance_start)}</span>
                </time>
                <p id={`${id}-run`} class="stub-run">
                  {#if oneNight(show)}
                    One night only
                  {:else}
                    Through <time datetime={show.closing_night}>{monthDay(show.closing_night)}{year(show.performance_start) !== year(show.closing_night) ? `, ${year(show.closing_night)}` : ''}</time>
                  {/if}
                </p>
                {#if show.livestream}
                  <p id={`${id}-stream`} class="stub-stream">Livestream available</p>
                {/if}
              </div>
              {#if show.ticket_url}
                <span id={`${id}-tickets`} class="stub-action">Get tickets <Arrow /></span>
              {/if}
            </div>
          </svelte:element>
        </div>
      </article>
    {/each}
  </section>
{/if}
