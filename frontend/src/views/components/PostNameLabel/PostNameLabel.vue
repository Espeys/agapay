<template>
  <div>
    <span
      v-if="author"
      @click="
        anonymous
          ? null
          : user.slug === (author.slug || '')
          ? $router.push({ name: 'Profile' })
          : $router.push({
              name: 'User Profile',
              params: { slug: author.slug }
            })
      "
      class="text-body1 text-weight-medium"
      :class="{ 'link-text cursor-pointer': !anonymous }"
      v-text="author.full_name || author.fullname"
    />

    <slot></slot>
  </div>
</template>

<script src="./PostNameLabel.js" />
