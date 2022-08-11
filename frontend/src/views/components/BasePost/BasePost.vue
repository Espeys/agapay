<template>
  <div>
    <q-card
      v-if="post.slug"
      class="q-pt-md q-mb-lg"
      :class="{ 'q-pb-xs': !shared }"
      :square="$q.screen.lt.md"
      :flat="shared"
      bordered
    >
      <div class="q-px-lg row no-wrap items-start">
        <q-avatar
          v-if="post.created_by"
          @click="
            post.is_anonymous || (publicPost && !isAuthenticated)
              ? null
              : user.slug === (post.created_by.slug || '')
              ? $router.push({ name: 'Profile' })
              : $router.push({
                  name: 'User Profile',
                  params: { slug: post.created_by.slug }
                })
          "
          size="48px"
          class="q-mr-md shadow-3 non-selectable"
          :class="{
            'cursor-pointer':
              !post.is_anonymous && !publicPost && !isAuthenticated
          }"
          :color="
            post.is_anonymous
              ? 'accent'
              : post.created_by.icon_color || 'primary'
          "
        >
          <q-img
            v-if="post.created_by.photo"
            :src="post.created_by.photo"
          ></q-img>
          <q-icon
            v-else
            :name="
              post.is_anonymous
                ? 'fas fa-mask'
                : post.created_by.icon_name ||
                  avatarIcon[post.created_by.groups[0]]
            "
            color="white"
          ></q-icon>
        </q-avatar>
        <div class="column">
          <post-name-label
            :author="post.created_by"
            :anonymous="post.is_anonymous || (publicPost && !isAuthenticated)"
          >
            <span
              v-if="post.item_type === 'diary'"
              class="inline q-ml-sm"
              :class="[$q.dark.isActive ? 'text-white' : 'text-grey-8']"
            >
              <span>was feeling </span>
              <vue-reaction-emoji
                :reaction="reactions[post.mood_type]"
                is-active
                width="25px"
                height="25px"
                class="q-mx-xs inline-block"
              />
              <span v-text="`${post.mood_type} that time`"></span>
            </span>
          </post-name-label>
          <div
            v-if="post.slug"
            class="text-body2 row no-wrap"
            :class="$q.dark.isActive ? ' text-grey-6' : ' text-grey-9'"
          >
            <router-link
              :to="
                (publicPost && !isAuthenticated) || post.item_type === 'diary'
                  ? ''
                  : { name: 'Post Details', params: { slug: post.slug } }
              "
            >
              <span
                class="link-text cursor-pointer"
                v-text="$date(post.created_at).fromNow()"
              />
            </router-link>
            <div v-if="post.item_type !== 'status'">
              <q-icon
                name="fas fa-circle"
                size="4px"
                style="margin-top: -2px"
                color="grey-6"
                class="q-mx-sm"
              ></q-icon>
              <span>
                <q-icon
                  :name="postTypeIcon[post.item_type]"
                  size="12px"
                  :color="$q.dark.isActive ? 'white' : 'accent'"
                  style="margin-top: -4px"
                  class="q-mr-xs cursor-pointer"
                >
                  <q-tooltip content-class="text-body1">
                    <span v-text="postType[post.item_type]"
                  /></q-tooltip>
                </q-icon>
                <span
                  v-text="
                    post.item_type !== 'promotion'
                      ? postType[post.item_type]
                      : promotionType[post.promotion_type]
                  "
              /></span>
            </div>
          </div>
        </div>
        <q-space />
        <q-btn
          v-if="isAuthenticated && !shared"
          size="12px"
          style="margin-top: -3px"
          flat
          round
        >
          <q-icon name="fas fa-ellipsis-h" size="18px" />
          <q-menu
            v-model="isContextMenuVisible"
            content-class="shadow-10"
            anchor="bottom right"
            self="top right"
            auto-close
          >
            <q-list padding style="width: 300px" class="q-px-sm">
              <template v-for="menu in contextMenu">
                <q-item
                  @click="$emit(menu.action)"
                  :key="menu.name"
                  tag="label"
                  class="rounded-borders"
                  v-ripple
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
                      <span
                        v-if="menu.name === 'Save post'"
                        v-text="post.is_saved ? 'Unsave post' : menu.name"
                      ></span>
                      <span v-else v-text="menu.name" />
                    </q-item-label>
                    <q-item-label v-if="menu.description" caption>
                      <span
                        v-if="menu.name === 'Save post'"
                        v-text="
                          post.is_saved
                            ? 'Remove this to your saved items'
                            : menu.description
                        "
                      ></span>
                      <span v-else v-text="menu.description" />
                    </q-item-label>
                  </q-item-section>
                </q-item>
                <q-separator
                  v-if="menu.separator"
                  :key="`${menu.name}-divider`"
                  class="q-my-sm q-mx-md"
                />
              </template>
            </q-list>
          </q-menu>
        </q-btn>
      </div>
      <div v-if="!isSensitive" :class="{ 'q-mb-md': shared }">
        <div v-if="post.description" class="q-px-lg q-pb-sm">
          <p
            class="q-mb-none q-mt-md text-weight-regular text-body1 post-content"
            v-linkified:options="{ className: 'post-content-link' }"
            style="white-space: pre-wrap"
          >
            <span
              v-text="
                wholePost ||
                (publicPost && !isAuthenticated) ||
                post.item_type === 'diary'
                  ? post.description
                  : truncatedContent
              "
            />
            <span
            @click="$router.push({name: 'Post Details', params: {slug: post.slug}})"
              v-if="post.description.length > maxPreviewContent && !wholePost"
              >...
              <span class="link-text text-primary cursor-pointer"
                >See more</span
              ></span
            >
          </p>
        </div>

        <div
          v-if="(post.tags || []).length"
          class="q-pl-md q-ml-xs"
          :class="{ 'q-mt-md': !post.description }"
        >
          <span class="text-body1 q-mx-xs text-weight-medium"
            >Related Tags:</span
          >
          <q-chip
            v-for="tag in [...post.tags]"
            @click="$router.push({ name: 'Search', query: { keyword: tag } })"
            :key="tag"
            :color="$q.dark.isActive ? 'white' : 'accent'"
            class="text-body2 text-weight-medium q-mb-sm"
            clickable
            outline
            dense
          >
            <span v-text="tag" />
          </q-chip>
        </div>
      </div>
      <div v-else class="q-px-lg q-my-md">
        <q-card class="q-py-md q-px-lg" bordered flat>
          <span class="text-h6">Sensitive Content</span>
          <p>
            This post contains sensitive content which some users may find
            offensive or disturbing.
          </p>
          <q-btn @click="isSensitive = !isSensitive" no-caps color="primary">
            See Post
          </q-btn>
        </q-card>
      </div>
      <div v-if="post.shared_post" class="q-px-lg q-mt-sm q-mb-md">
        <base-post :post="post.shared_post" shared></base-post>
      </div>
      <template v-if="post.banner">
        <q-img
          @click="onBannerClick"
          style="max-height: 300px"
          class="q-mt-xs cursor-pointer"
          :class="{
            'q-mt-md': !post.description && !(post.tags || []).length,
            'q-mb-md': !shared
          }"
          :src="post.banner"
        ></q-img>
        <FsLightbox :toggler="showImage" :sources="[post.banner]" />
      </template>
      <div
        class="q-px-lg q-pt-xs q-pb-md bg"
        v-if="!shared && post.item_type !== 'diary'"
      >
        <q-btn
          @click="hasLiked ? unlikePost() : likePost()"
          class="q-mr-md"
          :disabled="!isAuthenticated"
          :class="{ 'text-red': hasLiked }"
          flat
          dense
          no-caps
        >
          <q-icon
            :name="hasLiked ? 'fas fa-heart' : 'far fa-heart'"
            size="16px"
          ></q-icon>
          <span class="text-body2 q-px-sm text-weight-medium">Care</span>
        </q-btn>
        <template v-if="isAuthenticated">
          <q-btn
            v-if="post.slug"
            :to="{ name: 'Post Details', params: { slug: post.slug } }"
            class="q-mr-md"
            dense
            flat
            no-caps
          >
            <q-icon name="far fa-comment-dots" size="18px"></q-icon>
            <span class="text-body2 q-px-sm text-weight-medium">Comment</span>
          </q-btn>
          <q-btn
            v-if="
              (!post.is_shared && !post.shared_post) ||
                (!post.is_shared &&
                  post.shared_post &&
                  !post.shared_post.is_shared)
            "
            :to="{ name: 'Post Creation', query: { shared: post.slug } }"
            dense
            flat
            no-caps
          >
            <q-icon name="far fa-share-square" size="18px"></q-icon>
            <span class="text-body2 q-px-sm text-weight-medium">Share</span>
          </q-btn>
        </template>
      </div>

      <template v-if="!isAuthenticated">
        <q-separator></q-separator>
        <div class="q-px-lg q-py-md text-subtitle1 text-center">
          Please
          <span
            @click="login"
            class="text-primary cursor-pointer link-text text-weight-medium"
            >login</span
          >
          or
          <span
            @click="signup"
            class="text-primary cursor-pointer link-text text-weight-medium"
            >sign up</span
          >
          to view and create comments
        </div>
      </template>
      <template v-else>
        <template v-if="wholePost">
          <!-- <q-separator></q-separator> -->
          <comment-field
            v-model="comment"
            class="q-px-lg q-pt-sm q-pb-md"
            @select="selectEmoji"
            :user="user"
            @click:comment="addComment"
          ></comment-field>
          <q-separator v-if="comments.length"></q-separator>
          <div class="q-my-md">
            <comment-reply
              v-for="comment in comments"
              :key="comment.slug"
              :comment="comment"
              @reply="addReply"
              class="q-pl-lg q-pt-md"
              @delete="deleteComment(comment.slug)"
              @report="showReportDialog(comment.slug)"
            >
              <template #author>
                <post-name-label
                  :author="comment.created_by"
                  :anonymous="comment.is_anonymous"
                ></post-name-label>
              </template>
              <template #replies>
                <comment-reply
                  v-for="reply in comment.children"
                  :key="reply.slug"
                  :comment="reply"
                  class="q-pl-lg"
                  reply
                  @delete="deleteComment(reply.slug)"
                  @report="showReportDialog(reply.slug)"
                >
                  <template #author>
                    <post-name-label
                      :author="reply.created_by"
                      :anonymous="reply.is_anonymous"
                    ></post-name-label>
                  </template>
                </comment-reply>
                <comment-field
                  v-if="addReplyList.includes(comment.slug)"
                  v-model="replies[comment.slug]"
                  :id="comment.slug"
                  :ref="comment.slug"
                  class="q-px-lg q-pb-sm"
                  @select="selectReplyEmoji($event, comment.slug)"
                  :user="user"
                  reply
                  @click:comment="addCommentReply(comment.slug)"
                ></comment-field>
              </template>
            </comment-reply>
          </div>
        </template>
      </template>
    </q-card>
    <app-dialog
      ref="deleteComment"
      :maximized="$q.screen.lt.md"
      width="560px"
      card-class="q-px-lg q-pb-lg q-pt-md"
      close
    >
      <template #header>
        <span class="">Delete Comment</span>
      </template>
      <template #default="{confirm, cancel}">
        <p class="text-body1">
          Are you sure you want to delete this comment?
        </p>

        <div class="q-mt-md">
          <q-btn @click="confirm" no-caps color="negative" class=" on-left"
            >Delete</q-btn
          >
          <q-btn @click="cancel" no-caps outline>Cancel</q-btn>
        </div>
      </template>
    </app-dialog>
    <app-dialog
      ref="reportComment"
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
          What problem are you having with this comment?
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
            Kindly help us to understand it further by giving your feedback
            about the reported issue?
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
            @click="reportComment"
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
  </div>
</template>

<script src="./BasePost.js" />

<style>
.post-content-link {
  color: #2196f3 !important;
  font-weight: 600;
  text-decoration: underline;
}
</style>
