<script lang="ts">
  import { onMount } from 'svelte';
  import { watchCurrentShows } from '$shows';
  import { sitePath } from '$lib/paths';
  import type { Show, CurrentShow } from '$lib/types';

  let { shows, watchOptions }: {
    shows: Show[];
    watchOptions?: Parameters<typeof watchCurrentShows>[2];
  } = $props();
  let current = $state<CurrentShow[]>([]);

  // Empty during SSR, even if a build happens during a production's run.
  // Test harnesses can inject the shared watcher's clock/timer options; no URL/debug state.
  onMount(() => watchCurrentShows(shows, (next: CurrentShow[]) => { current = next; }, watchOptions));

  // Presentation only: format the validated date without converting it to a visitor timezone.
  const dateFormat = new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' });
  const dateLabel = (iso: string) => dateFormat.format(new Date(`${iso}T12:00:00Z`));
</script>

{#if current.length}
  <section class="current-projects section-block" aria-labelledby="current-title">
    <h2 id="current-title">Current projects</h2>
    <div class="project-notes">
      {#each current as show (show.id)}
        <article class="project-note" aria-labelledby={`show-${encodeURIComponent(show.id)}`}>
          {#if show.photo}
            <img class="project-photo" src={sitePath(show.photo)} alt={show.photo_alt ?? ''} loading="lazy" decoding="async" />
          {/if}
          <div class="project-note-copy">
            <h3 id={`show-${encodeURIComponent(show.id)}`}>{show.title}</h3>
            <p class="project-role">{show.character}</p>
            <p class="project-company">{show.company}</p>
            <p class="project-status">{show.status === 'rehearsing' ? 'In rehearsal' : 'Performing'}</p>
            <p class="project-dates">
              <time datetime={show.performance_start}>{dateLabel(show.performance_start)}</time>
              {#if show.performance_start !== show.closing_night}
                <span>{' to '}</span><time datetime={show.closing_night}>{dateLabel(show.closing_night)}</time>
              {/if}
            </p>
            {#if show.ticket_url}
              <a class="ticket-link" href={show.ticket_url} aria-label={`Tickets for ${show.title}`}>Tickets <span aria-hidden="true">↗</span></a>
            {/if}
          </div>
        </article>
      {/each}
    </div>
  </section>
{/if}
