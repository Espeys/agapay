<template>
  <app-dialog
    ref="supportPost"
    :maximized="$q.screen.lt.md"
    width="560px"
    card-class="q-px-lg q-pb-lg q-pt-md"
    :loading="loading"
    close
  >
    <template #header>
      <span class="">Support Post</span>
    </template>
    <template #default="{cancel}">
      <p class="text-body1 q-mb-sm text-weight-medium">
        What issues are you having with this post?
      </p>
      <div>
        <q-chip
          v-for="reason in supportReasons"
          :key="reason"
          @click="supportData.reason = reason"
          clickable
          class="q-mb-md"
          :class="{
            'bg-accent text-white': reason === supportData.reason
          }"
        >
          <span
            class="text-body1"
            :class="{ 'text-weight-medium': reason === supportData.reason }"
            v-text="reason"
          ></span>
        </q-chip>
      </div>
      <div class="q-mt-md q-mb-lg">
        <p class="text-body1 q-mb-sm text-weight-medium">
          Please tag any of your followed service provider that might help this
          post
          <span class="text-weight-regular text-italic"></span>
        </p>
        <app-form-input
          v-model="supportData.slugs"
          field-type="select"
          :options="following"
          outlined
          multiple
          emit-value
          map-options
        >
        </app-form-input>
      </div>
      <div class="q-mt-md">
        <p class="text-body1 q-mb-sm text-weight-medium">
          Kindly help us to understand it further by giving your feedback about
          the supported issue?
          <span class="text-weight-regular text-italic">(Optional)</span>
        </p>
        <app-form-input
          v-model="supportData.description"
          type="textarea"
          rows="3"
          outlined
        >
        </app-form-input>
      </div>
      <div class="q-mt-lg">
        <q-btn
          @click="submit"
          :disabled="!supportData.reason && !supportData.slugs.length"
          no-caps
          color="primary"
          class=" on-left"
          >Support</q-btn
        >
        <q-btn @click="cancel" no-caps outline>Cancel</q-btn>
      </div>
    </template>
  </app-dialog>
</template>

<script src="./SupportDialog.js" />
