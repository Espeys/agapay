<template>
  <div class="row justify-lg-around q-pl-md-lg q-pl-lg-none">
    <div class="col-12 col-md-8 col-lg-7">
      <div class="q-pa-md q-pa-md-none q-mb-sm q-mb-md-md">
        <div class="row items-center">
          <span class="text-h4 text-weight-medium">Mood Tracking</span>
          <q-space></q-space>
          <q-btn @click="showFilters" flat round dense
            ><q-icon name="fas fa-sliders-h" size="20px"></q-icon
          ></q-btn>
        </div>

        <p class="text-body1 q-mb-none q-mt-sm">
          Explore your daily thoughts and emotions by writing them on a private
          and personal diary
        </p>
        <div class="q-mt-md q-mb-sm">
          <q-btn
            :to="{ name: 'Post Creation', query: { type: 'diary' } }"
            color="primary"
            rounded
            no-caps
          >
            Create entry for today
          </q-btn>
        </div>
        <div class="row">
          <q-card class="q-px-md q-py-lg q-px-md-lg q-mt-md col-12" bordered>
            <div class="row justify-between items-center no-wrap">
              <div>
                <span class="text-subtitle2"
                  >Your overall mood for this week</span
                >
                <div class="q-mt-xs">
                  <span
                    class="text-h5 text-weight-bold text-negative text-uppercase"
                    >Angry</span
                  >
                  <p class="text-body2 text-italic q-mr-md q-mb-none">
                    "For every minute you remain angry, you give up sixty
                    seconds of peace of mind. "
                  </p>
                </div>
              </div>
              <vue-reaction-emoji
                reaction="hate"
                is-active
                width="70px"
                height="70px"
              />
            </div>
            <q-separator class="q-my-md"></q-separator>
            <div class="row justify-between">
              <div class="col-12 col-md-7">
                <span class="text-weight-medium"
                  >Additional information about your overall mood</span
                >
                <q-list>
                  <q-item>
                    <q-item-section avatar>
                      <q-avatar color="accent" size="32px">
                        <q-icon name="far fa-bookmark" color="white"></q-icon>
                      </q-avatar>
                    </q-item-section>
                    <q-item-section class="text-body-1">
                      <q-item-label>
                        <a
                          href="https://au.reachout.com/articles/8-ways-to-deal-with-anger"
                          target="_blank"
                          class="text-primary text-weight-medium link-text"
                        >
                          8 ways to deal with anger
                        </a>
                      </q-item-label>
                      <q-item-label caption>
                        reachout.com
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>
              <div class="col-md-4">
                <q-img :src="require('@/assets/mood.svg')"></q-img>
              </div>
            </div>
          </q-card>
        </div>
        <div class="q-mt-lg row items-center">
          <q-icon class="fas fa-calendar-alt" size="16px" left></q-icon>
          <span class="text-h6 text-weight-medium"
            ><span v-text="selectedMonth"/> <span v-text="selectedYear"
          /></span>
        </div>
      </div>
      <div>
        <base-post
          v-for="(post, i) in posts"
          :key="post.slug"
          :post="post"
          @delete="deletePost(post.slug, i)"
          @save="bookmarkPost(post.slug, i, post.is_saved)"
        ></base-post>
      </div>
      <div class="q-py-md text-center">
        <span class="text-body1 text-grey-7"
          >There are no more post to show right now.</span
        >
      </div>
    </div>
    <div class="col-12 col-md-2 col-lg-4 gt-md">
      <ads-trends-column></ads-trends-column>
      <sticky-side-section></sticky-side-section>
    </div>
    <app-dialog
      ref="postFilters"
      @close-dialog="onCloseDialog"
      :maximized="$q.screen.lt.md"
      width="560px"
      height="400px"
      card-class="q-py-lg q-px-md"
      close
    >
      <template #header>
        <span class="">Filters</span>
      </template>
      <div class="q-mb-sm">
        <app-form-input
          v-model="selectedYear"
          field-type="select"
          :options="yearOptions"
          label="Year"
          outlined
        ></app-form-input>
      </div>
      <div class="q-mb-sm">
        <app-form-input
          v-model="selectedMonth"
          field-type="select"
          :options="monthOptions"
          label="Month"
          outlined
        ></app-form-input>
      </div>
      <div class="q-mt-md row justify-end">
        <q-btn @click="onClear" no-caps class="on-left" outline>Clear</q-btn>
        <q-btn @click="onApply" no-caps color="primary">Apply</q-btn>
      </div>
    </app-dialog>
  </div>
</template>

<script src="./MoodTracking.js" />
