<template>
  <div class="row no-wrap full-width items-start">
    <q-avatar
      v-if="user"
      @click="
        user.slug === (user.slug || '')
          ? $router.push({ name: 'Profile' })
          : $router.push({
              name: 'User Profile',
              params: { slug: user.slug }
            })
      "
      :size="reply ? '32px' : '40px'"
      class="q-mr-md shadow-3 non-selectable"
      :class="{ 'cursor-pointer': !user.is_anonymous }"
      :color="user.is_anonymous ? 'accent' : user.icon_color || 'primary'"
    >
      <q-img v-if="user.photo" :src="user.photo"></q-img>
      <q-icon
        v-else
        :name="
          user.is_anonymous
            ? 'fas fa-mask'
            : user.icon_name || avatarIcon[user.groups[0]]
        "
        color="white"
      ></q-icon>
    </q-avatar>
    <div class="col-grow">
      <div class="column">
        <app-form-input
          @input="$emit('input', $event)"
          :value="value"
          :placeholder="reply ? 'Type your reply ...' : 'Type your comment ...'"
          autogrow
          outlined
        >
          <template #append>
            <q-btn dense flat round size="md">
              <q-icon name="far fa-grin" size="22px"></q-icon>
              <q-menu>
                <v-emoji-picker
                  emoji-size="24"
                  @select="$emit('select', $event)"
                  emojis-by-row="8"
                  :dark="$q.dark.isActive"
                />
              </q-menu>
            </q-btn>
          </template>
        </app-form-input>
        <div class="q-mt-md row justify-end">
          <q-btn
            @click="$emit('click:comment')"
            :disable="!value"
            color="primary"
            no-caps
          >
            <span v-text="reply ? 'Reply' : 'Comment'" />
          </q-btn>
        </div>
      </div>
    </div>
  </div>
</template>

<script src="./CommentField.js" />
