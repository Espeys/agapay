<template>
  <div class="row justify-lg-around q-pl-md-lg q-pl-lg-none">
    <div class="col-12 col-md-8 col-lg-7">
      <div class="q-pa-md q-pa-md-none q-mb-sm q-mb-md-lg">
        <span class="text-h4 text-weight-medium">
          Emotional and Mental Health
        </span>
        <p class="q-mt-sm text-body1">
          Browse various resources and information from experts and service
          providers that can help you to take care of your mental and emotional
          health.
        </p>

        <div class="text-body1 bg-primary q-pa-md rounded-borders text-white">
          Do you want to contribute on this page and share your work that it is
          relavant to our goal? Please email at
          <span class="text-weight-bold">agapayph@gmail.com</span> and we are
          looking forward on what you are going to submit.
        </div>
      </div>

      <div>
        <q-video
          class="rounded-borders q-mb-lg"
          :ratio="16 / 9"
          src="https://www.youtube.com/embed/sgCtfRGLmi8"
        />

        <managing-stress-article class="q-mb-lg"></managing-stress-article>

        <q-video
          class="rounded-borders q-mb-lg"
          :ratio="16 / 9"
          src="https://www.youtube.com/embed/BVJkf8IuRjE"
        />

        <q-video
          class="rounded-borders q-mb-lg"
          :ratio="16 / 9"
          src="https://www.youtube.com/embed/z-IR48Mb3W0"
        />
      </div>
    </div>
    <div class="col-12 col-md-2 col-lg-4 gt-md">
      <ads-trends-column></ads-trends-column>
      <sticky-side-section></sticky-side-section>
    </div>
  </div>
</template>

<script src="./EmotionalMentalHealth.js" />
