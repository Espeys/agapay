<template>
  <div class="row justify-lg-around q-pl-md-lg q-pl-lg-none">
    <div class="col-12 col-md-8 col-lg-7">
      <div class="q-pa-md q-pa-md-none q-mb-sm q-mb-md-lg">
        <span class="text-h4 text-weight-medium">
          Promotions that might interest you
        </span>
      </div>
      <base-post
        v-for="(post, i) in pseudoPosts"
        :key="post.slug"
        :post="post"
        @delete="deletePost(post.slug, i)"
        @save="bookmarkPost(post.slug, i, post.is_saved)"
        @report="showReportDialog(post.slug)"
        @support="showSupportDialog(post.slug)"
      ></base-post>
      <base-post
        v-for="(post, i) in posts"
        :key="post.slug"
        :post="post"
        @delete="deletePost(post.slug, i)"
        @save="bookmarkPost(post.slug, i, post.is_saved)"
        @report="showReportDialog(post.slug)"
        @support="showSupportDialog(post.slug)"
      ></base-post>
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
    <report-dialog ref="report" @click:report="reportPost" :loading="loading" />
    <support-dialog
      ref="support"
      @click:support="supportPost"
      :loading="loading"
    ></support-dialog>
  </div>
</template>

<script src="./PublicNewsFeed.js" />
