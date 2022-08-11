<template>
  <div>
    <q-card
      class="q-py-md q-px-lg q-mb-lg"
      :square="$q.screen.lt.md"
      flat
      bordered
    >
      <span class="text-h5 text-weight-medium"> Popular Topics</span>
      <div v-for="item in items.slice(0, 3)" :key="item.slug" class="q-py-sm">
        <span
          class="text-h6 text-primary link-text cursor-pointer"
          @click="$router.push({ name: 'Search', keyword: item.text })"
          v-text="item.text"
        />
        <p class="q-mb-none text-body1">
          <span class="text-weight-medium">Posts: </span>
          <span v-text="item.num_count"></span>
        </p>
      </div>
    </q-card>
  </div>
</template>

<script src="./AdsTrendsColumn.js" />
