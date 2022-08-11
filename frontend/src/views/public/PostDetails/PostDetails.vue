<template>
  <div class="row justify-lg-around q-pl-md-lg q-pl-lg-none">
    <div class="col-12 col-md-8 col-lg-7">
      <base-post
        :post="{ ...postDetails }"
        whole-post
        ref="post"
        @delete="deletePost(postDetails.slug)"
        @save="bookmarkPost(postDetails.slug, postDetails.is_saved)"
        @report="showReportDialog(postDetails.slug)"
        @support="showSupportDialog(postDetails.slug)"
      />
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

<script src="./PostDetails.js" />
