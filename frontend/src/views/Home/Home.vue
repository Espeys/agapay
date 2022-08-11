<template>
  <div class="row justify-lg-around q-pl-md-lg q-pl-lg-none">
    <div class="col-12 col-md-8 col-lg-7">
      <div class="q-pa-md q-pa-md-none q-mb-sm q-mb-md-lg row items-center">
        <span class="text-h4 text-weight-medium">Home</span>
        <q-space></q-space>
        <q-btn @click="showFilters" flat round dense
          ><q-icon name="fas fa-sliders-h" size="20px"></q-icon
        ></q-btn>
      </div>

      <div>
        <base-post
          v-for="(post, i) in posts"
          :key="post.slug"
          :post="post"
          @delete="deletePost(post.slug, i)"
          @save="bookmarkPost(post.slug, i, post.is_saved)"
          @report="showReportDialog(post.slug)"
          @support="showSupportDialog(post.slug)"
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
        <span class="">Post Filters</span>
      </template>
      <div class="q-mb-sm">
        <app-form-input
          v-model="filterViews"
          field-type="select"
          :options="filters"
          label="Categories"
          outlined
          map-options
          emit-value
        ></app-form-input>
      </div>
      <div class="q-mt-md row justify-end">
        <q-btn @click="onClear" no-caps class="on-left" outline>Clear</q-btn>
        <q-btn @click="onApply" no-caps color="primary">Apply</q-btn>
      </div>
    </app-dialog>
    <report-dialog ref="report" @click:report="reportPost" :loading="loading" />
    <support-dialog
      ref="support"
      @click:support="supportPost"
      :loading="loading"
    ></support-dialog>
  </div>
</template>

<script src="./Home.js" />
