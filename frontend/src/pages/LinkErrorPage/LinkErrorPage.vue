<template>
  <div class="q-mt-lg">
    <div class="row justify-center q-mb-lg q-mb-md-none">
      <q-img
        :src="
          require($q.dark.isActive
            ? '@/assets/h-logo-white.png'
            : '@/assets/h-logo.png')
        "
        width="180px"
      ></q-img>
    </div>
    <div>
      <div class="col-grow row-md column items-center justify-center">
        <q-img
          :src="require('@/assets/error404.svg')"
          class="q-mr-md-xl"
          width="240px"
        ></q-img>
        <div
          class="q-mt-lg"
          style="width: 480px"
          :class="[$q.screen.lt.md ? 'text-center' : 'text-left']"
        >
          <span class="text-h4 text-weight-medium">The link was broken.</span>
          <p class="text-body1 q-mt-sm">
            Sorry but there is a problem on the link you are visiting.
          </p>
          <q-btn
            :to="{ name: 'Home' }"
            color="accent"
            :class="{ 'full-width': $q.screen.lt.md }"
            no-caps
            >Go to page</q-btn
          >
        </div>
      </div>
    </div>
  </div>
</template>
