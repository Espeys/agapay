<template>
  <q-dialog
    v-model="isVisible"
    v-bind="$attrs"
    persistent
    :content-class="{
      'darkest-opacity': isVisible && !$q.dark.isActive,
      'darker-opacity': isVisible && $q.dark.isActive
    }"
  >
    <q-card
      style="max-width: 100vw; "
      :style="`width: ${width}; height: ${$q.screen.lt.md ? null : height}`"
    >
      <div class="relative-position">
        <div
          v-if="$scopedSlots.header || close"
          :class="{
            absolute: !$scopedSlots.header,
            'q-pt-md': $scopedSlots.header
          }"
          class="text-center"
        >
          <span class="text-h5 text-weight-medium">
            <slot name="header" />
          </span>
        </div>
        <q-btn
          v-if="close"
          class="absolute-top-right"
          style="top: 14px; right: 8px"
          icon="fas fa-times"
          size="16px"
          flat
          round
          dense
          v-close-popup
        />
        <div :class="cardClass">
          <slot :cancel="cancel" :confirm="confirm" />
        </div>
        <q-inner-loading :showing="loading">
          <q-spinner-hourglass color="primary" size="5.5em" class="q-mb-md" />
          <span class="text-body2"> Please wait ...</span>
        </q-inner-loading>
      </div>
    </q-card>
  </q-dialog>
</template>

<script src="./AppDialog.js" />

<style>
.dark-opacity {
  background-color: rgba(0, 0, 0, 0.3);
}
.darker-opacity {
  background-color: rgba(0, 0, 0, 0.8);
}
.darkest-opacity {
  background-color: rgba(0, 0, 0, 0.85);
}
</style>
