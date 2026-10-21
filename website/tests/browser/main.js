import { mount, unmount } from 'svelte';
import CurrentProjects from '../../src/lib/components/CurrentProjects.svelte';
import '../../src/styles/site.css';
import { fixtures } from './fixtures.mjs';

const target = document.querySelector('#component');
const select = document.querySelector('#fixture');
let component;
async function remove() {
  if (component) await unmount(component);
  component = undefined;
}
document.querySelector('#mount').addEventListener('click', async () => {
  await remove();
  component = mount(CurrentProjects, { target, props: { shows: fixtures[select.value] } });
});
document.querySelector('#unmount').addEventListener('click', remove);
