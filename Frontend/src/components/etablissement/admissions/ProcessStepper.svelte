<script>
  import Icon from '@iconify/svelte';
  export let steps;
</script>

<nav aria-label="Progress">
  <ol class="overflow-hidden">
    {#each steps as step, index}
      <li class={`relative pb-10 ${index !== steps.length - 1 ? '' : 'pb-0'}`}>
        {#if step.status === 'complete'}
          <div class="absolute left-4 top-4 -ml-px mt-0.5 h-full w-0.5 bg-green-600" aria-hidden="true"></div>
          <div class="group relative flex items-start">
            <span class="flex h-9 items-center">
              <span class="relative z-10 flex h-8 w-8 items-center justify-center rounded-full bg-green-600">
                <Icon icon="heroicons:check" class="h-5 w-5 text-white" />
              </span>
            </span>
            <span class="ml-4 flex min-w-0 flex-col">
              <span class="text-sm font-medium text-gray-900">{step.name}</span>
            </span>
          </div>
        {:else if step.status === 'current'}
          <div class="absolute left-4 top-4 -ml-px mt-0.5 h-full w-0.5 bg-gray-300" aria-hidden="true"></div>
          <div class="group relative flex items-start" aria-current="step">
            <span class="flex h-9 items-center" aria-hidden="true">
              <span class="relative z-10 flex h-8 w-8 items-center justify-center rounded-full border-2 border-green-600 bg-white">
                <span class="h-2.5 w-2.5 rounded-full bg-green-600"></span>
              </span>
            </span>
            <span class="ml-4 flex min-w-0 flex-col">
              <span class="text-sm font-medium text-green-600">{step.name}</span>
              <span class="text-sm text-gray-500">En cours</span>
            </span>
          </div>
        {:else}
          <div class="absolute left-4 top-4 -ml-px mt-0.5 h-full w-0.5 bg-gray-300" aria-hidden="true"></div>
          <div class="group relative flex items-start">
            <span class="flex h-9 items-center" aria-hidden="true">
              <span class="relative z-10 flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-300 bg-white">
                <span class="h-2.5 w-2.5 rounded-full bg-transparent"></span>
              </span>
            </span>
            <span class="ml-4 flex min-w-0 flex-col">
              <span class="text-sm font-medium text-gray-500">{step.name}</span>
            </span>
          </div>
        {/if}
      </li>
    {/each}
  </ol>
</nav>