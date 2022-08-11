<template>
  <div class="row no-wrap full-width items-start">
    <q-avatar
      v-if="comment.created_by"
      @click="
        comment.is_anonymous
          ? null
          : user.slug === (comment.created_by.slug || '')
          ? $router.push({ name: 'Profile' })
          : $router.push({
              name: 'User Profile',
              params: { slug: comment.created_by.slug }
            })
      "
      :size="reply ? '32px' : '40px'"
      class="q-mr-md shadow-3 non-selectable"
      :class="{ 'cursor-pointer': !comment.is_anonymous }"
      :color="
        comment.is_anonymous
          ? 'accent'
          : comment.created_by.icon_color || 'primary'
      "
    >
      <q-img
        v-if="comment.created_by.photo"
        :src="comment.created_by.photo"
      ></q-img>
      <q-icon
        v-else
        :name="
          comment.is_anonymous
            ? 'fas fa-mask'
            : comment.created_by.icon_name ||
              avatarIcon[comment.created_by.groups[0]]
        "
        color="white"
      ></q-icon>
    </q-avatar>
    <div class="column full-width q-pr-md">
      <div class="row no-wrap">
        <q-card class="q-py-sm q-px-md" flat bordered>
          <slot name="author" />
          <p class="text-body1 q-mb-none" v-text="comment.description" />
        </q-card>
        <div>
          <q-btn class="q-mx-xs col-auto" round flat dense>
            <q-icon name="fas fa-ellipsis-h" size="14px"></q-icon>
            <q-menu
              v-model="isContextMenuVisible"
              content-class="shadow-10"
              anchor="bottom middle"
              self="top middle"
              auto-close
            >
              <q-list padding style="width: 300px" class="q-px-sm">
                <template v-for="menu in contextMenu">
                  <q-item
                    @click="$emit(menu.action)"
                    :key="menu.name"
                    class="rounded-borders"
                    v-ripple
                    clickable
                  >
                    <q-item-section top avatar>
                      <q-avatar size="md" square>
                        <q-icon
                          :name="menu.icon"
                          :color="menu.critical ? 'red' : null"
                          size="xs"
                        />
                      </q-avatar>
                    </q-item-section>
                    <q-item-section>
                      <q-item-label
                        class="row text-body1"
                        :class="{ 'text-red': menu.critical }"
                      >
                        <span v-text="menu.name" />
                      </q-item-label>
                      <q-item-label
                        v-if="menu.description"
                        v-text="menu.description"
                        caption
                      />
                    </q-item-section>
                  </q-item>
                  <q-separator
                    v-if="menu.separator"
                    :key="`${menu.name}-divider-${comment.slug}`"
                    class="q-my-sm q-mx-md"
                  />
                </template>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </div>
      <div class="q-mt-xs q-mb-md text-body2">
        <span
          v-if="!reply"
          @click="$emit('reply', comment.slug)"
          class="link-text text-primary cursor-pointer"
          >Reply</span
        >
        <q-icon
          v-if="!reply"
          name="fas fa-circle"
          size="4px"
          style="margin-top: -2px"
          color="grey-6"
          class="q-mx-sm"
        ></q-icon>
        <span
          :class="$q.dark.isActive ? ' text-grey-6' : ' text-grey-9'"
          v-text="$date(comment.updated_at).fromNow()"
        />
      </div>
      <slot name="replies" />
    </div>
  </div>
</template>

<script src="./CommentReply.js" />
