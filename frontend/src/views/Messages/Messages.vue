<template>
  <div class="q-py-md q-py-md-none q-px-md q-mx-md-sm">
    <div class="row full-width gt-sm">
      <q-card
        bordered
        style="width: 240px; overflow-y: auto; height: 590px"
        class="q-pa-sm"
      >
        <div class="q-pa-md">
          <span class="text-h5 text-weight-medium">Messages</span>
        </div>

        <q-list v-if="conversations.length">
          <q-item
            v-for="(conversation, i) in conversations"
            :key="conversation.slug"
            @click="selectCurrentConversation(i)"
            clickable
            v-ripple
          >
            <q-item-section avatar>
              <q-avatar color="primary">
                <q-icon name="fas fa-user" color="white"></q-icon>
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label lines="1" class="text-weight-medium text-body1">
                <span v-text="conversation.title"></span>
              </q-item-label>
              <q-item-label class="conversation__summary" caption lines="2">
                <q-icon
                  name="fas fa-check-circle"
                  size="10px"
                  class="q-mr-xs"
                  style="margin-top: -3px"
                  :color="
                    (conversation.preview || {}).is_readed ? 'positive' : null
                  "
                />
                <q-icon name="not_interested" v-if="conversation.deleted" />
                <span
                  v-text="
                    (conversation.preview || {}).text ||
                      `You are connected with ${conversation.title}`
                  "
                ></span>
              </q-item-label>
            </q-item-section>
            <!-- <q-item-section side>
              <q-item-label>
                <q-icon
                  name="fas fa-check-circle"
                  size="14px"
                  style="margin-top: -10px"
                  color="green"
                ></q-icon>
              </q-item-label>
            </q-item-section> -->
          </q-item>
        </q-list>
      </q-card>

      <div class="column col-grow relative-position">
        <q-card class="q-pa-md" bordered>
          <div class="text-body1">
            <span
              v-if="currentConversation.members"
              v-text="currentConversation.title"
            ></span>
            <span v-else>
              <q-icon name="fas fa-user" style="margin-top:-8px" left></q-icon>
              Select user to message
            </span>
          </div>
        </q-card>
        <div
          :class="$q.dark.isActive ? 'bg-dark' : 'bg-white'"
          style="height: 480px; overflow-y: scroll"
          ref="chatbox"
        >
          <div class="q-pa-lg">
            <q-chat-message
              v-for="message in messages"
              :key="message.slug"
              :name="message.created_by.full_name"
              avatar="https://cdn.quasar.dev/img/avatar4.jpg"
              :text="[message.text]"
              :sent="user.slug === message.created_by.slug"
              :stamp="$date(message.created_at).fromNow()"
            >
              <template #avatar>
                <q-avatar
                  :color="message.created_by.icon_color || 'primary'"
                  class="q-mx-lg"
                >
                  <q-img
                    v-if="message.created_by.photo"
                    :src="message.created_by.photo"
                  ></q-img>
                  <q-icon
                    v-else
                    :name="
                      message.created_by.icon_name ||
                        avatarIcon[message.created_by.groups[0]]
                    "
                    color="white"
                  ></q-icon>
                </q-avatar>
              </template>
            </q-chat-message>
          </div>
        </div>

        <q-card bordered>
          <q-toolbar class="row">
            <q-btn
              :disable="!Object.keys(currentConversation).length"
              round
              flat
              class="q-mr-sm"
            >
              <q-icon name="far fa-grin" size="22px" dark></q-icon>
              <q-menu>
                <v-emoji-picker
                  emoji-size="24"
                  emojis-by-row="8"
                  :dark="$q.dark.isActive"
                  @select="message += $event.data"
                />
              </q-menu>
            </q-btn>
            <q-input
              :disable="!Object.keys(currentConversation).length"
              @keypress.enter="sendMessage"
              rounded
              outlined
              dense
              class="col-grow q-mr-sm"
              v-model="message"
              placeholder="Type a message"
            />
            <q-btn
              @click="sendMessage"
              :disable="!Object.keys(currentConversation).length"
              round
              flat
              icon="fas fa-paper-plane"
            />
          </q-toolbar>
        </q-card>
        <q-inner-loading :showing="loading">
          <q-spinner-hourglass color="primary" size="5.5em" class="q-mb-md" />
          <span class="text-body2"> Please wait ...</span>
        </q-inner-loading>
      </div>
    </div>
  </div>
</template>

<script src="./Messages.js" />
