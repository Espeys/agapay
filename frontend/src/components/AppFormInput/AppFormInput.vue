<template>
  <q-toggle
    v-if="fieldType === 'toggle'"
    @input="$emit('input', $event)"
    :value="value"
    v-bind="$attrs"
    v-on="$listeners"
  >
    <slot v-for="slot in Object.keys($slots)" :name="slot" :slot="slot" />

    <template
      v-for="slot in Object.keys($scopedSlots)"
      :slot="slot"
      slot-scope="scope"
      ><slot :name="slot" v-bind="scope"
    /></template>
  </q-toggle>
  <q-select
    v-else-if="fieldType === 'select'"
    @input="$emit('input', $event)"
    :value="value"
    v-bind="$attrs"
    v-on="$listeners"
    dropdown-icon="fas fa-chevron-down"
    class="text-body1"
    clear-icon="fas fa-times"
    stack-label
    :behavior="$q.screen.lt.md ? 'dialog' : 'menu'"
    :bottom-slots="!!$attrs['error-message']"
    :error="!!$attrs['error-message']"
    hide-bottom-space
    no-error-icon
  >
    <template #label v-if="$attrs.label">
      <span
        class="text-body1 text-weight-medium q-mb-sm block"
        :class="$q.dark.isActive ? ' text-white' : ' text-grey-9'"
        v-text="$attrs.label"
      />
    </template>
    <slot v-for="slot in Object.keys($slots)" :name="slot" :slot="slot" />

    <template
      v-for="slot in Object.keys($scopedSlots)"
      :slot="slot"
      slot-scope="scope"
      ><slot :name="slot" v-bind="scope"
    /></template>
  </q-select>
  <q-checkbox
    v-else-if="fieldType === 'checkbox'"
    @input="$emit('input', $event)"
    :value="value"
    v-bind="$attrs"
    v-on="$listeners"
  >
    <slot v-for="slot in Object.keys($slots)" :name="slot" :slot="slot" />

    <template
      v-for="slot in Object.keys($scopedSlots)"
      :slot="slot"
      slot-scope="scope"
      ><slot :name="slot" v-bind="scope"
    /></template>
  </q-checkbox>
  <q-input
    v-else
    @input="$emit('input', $event)"
    :value="value"
    v-bind="$attrs"
    v-on="$listeners"
    class="text-body1"
    hide-bottom-space
    stack-label
    clear-icon="fas fa-times"
    :bottom-slots="!!$attrs['error-message']"
    :error="!!$attrs['error-message']"
    no-error-icon
  >
    <template #label v-if="$attrs.label">
      <span
        class="text-body1 text-weight-medium q-mb-sm block"
        :class="$q.dark.isActive ? ' text-white' : ' text-grey-9'"
        v-text="$attrs.label"
      />
    </template>
    <slot v-for="slot in Object.keys($slots)" :name="slot" :slot="slot" />

    <template
      v-for="slot in Object.keys($scopedSlots)"
      :slot="slot"
      slot-scope="scope"
      ><slot :name="slot" v-bind="scope"
    /></template>
  </q-input>
</template>

<script src="./AppFormInput.js" />
