<template>
  <app-dialog
    ref="reportPost"
    :maximized="$q.screen.lt.md"
    width="560px"
    card-class="q-px-lg q-pb-lg q-pt-md"
    :loading="loading"
    close
  >
    <template #header>
      <span class="">Report Post</span>
    </template>
    <template #default="{cancel}">
      <p class="text-body1 q-mb-sm text-weight-medium">
        What problem are you having with this post?
      </p>
      <div>
        <q-chip
          v-for="reason in reportReasons"
          :key="reason"
          @click="reportData.reason = reason"
          clickable
          class="q-mb-md"
          :class="{
            'bg-accent text-white': reason === reportData.reason
          }"
        >
          <span
            class="text-body1"
            :class="{ 'text-weight-medium': reason === reportData.reason }"
            v-text="reason"
          ></span>
        </q-chip>
      </div>
      <div class="q-mt-md">
        <p class="text-body1 q-mb-sm text-weight-medium">
          Kindly help us to understand it further by giving your feedback about
          the reported issue?
          <span class="text-weight-regular text-italic">(Optional)</span>
        </p>
        <app-form-input
          v-model="reportData.description"
          type="textarea"
          rows="3"
          outlined
        >
        </app-form-input>
      </div>
      <div class="q-mt-lg">
        <q-btn
          @click="submit"
          :disable="!reportData.reason"
          no-caps
          color="primary"
          class=" on-left"
          >Report</q-btn
        >
        <q-btn @click="cancel" no-caps outline>Cancel</q-btn>
      </div>
    </template>
  </app-dialog>
</template>

<script src="./ReportDialog.js" />
