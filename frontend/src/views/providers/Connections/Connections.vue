<template>
  <div class="row justify-lg-around q-pl-md-lg q-pl-lg-none">
    <div class="col-12 col-md-8 col-lg-7">
      <div class="q-pa-md q-pa-md-none q-mb-sm q-mb-md-md">
        <span class="text-h4 text-weight-medium">Connections</span>

        <p class="text-body1 q-mb-none q-mt-sm">
          Here are the list of the service providers who wanted you as one of
          their connections.
        </p>
      </div>
      <q-tabs
        v-model="tabs"
        dense
        class="q-mt-sm q-mx-lg q-mx-md-none"
        align="left"
        content-class="text-body1"
        left-icon="fas fa-chevron-left"
        right-icon="fas fa-chevron-right"
        no-caps
      >
        <q-tab name="pending" label="Pending" />
        <q-tab name="support" label="Need Support" />
      </q-tabs>
      <q-tab-panels v-model="tabs">
        <q-tab-panel name="pending" class="q-px-xs">
          <q-list>
            <q-card
              v-for="connection in pendingConnections"
              :key="connection.slug"
              class="q-pa-sm q-mb-sm"
            >
              <q-item>
                <q-item-section avatar>
                  <q-avatar
                    class="cursor-pointer"
                    @click="
                      $router.push({
                        name: 'User Profile',
                        params: { slug: connection.user.slug }
                      })
                    "
                    :color="connection.user.icon_color || 'primary'"
                    size="40px"
                  >
                    <q-img
                      v-if="connection.user.photo"
                      :src="connection.user.photo"
                    ></q-img>
                    <q-icon
                      v-else
                      :name="
                        connection.user.icon_name ||
                          avatarIcon[connection.user.groups[0]]
                      "
                      color="white"
                    ></q-icon>
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <q-item-label
                    ><post-name-label
                      :author="connection.user"
                    ></post-name-label
                  ></q-item-label>
                  <q-item-label caption
                    ><span
                      v-text="$date(connection.created_at).fromNow()"
                    ></span
                  ></q-item-label>
                </q-item-section>
                <q-item-section
                  v-if="pendingConnection.includes(connection.user.slug)"
                  side
                >
                  <div>
                    <q-btn
                      @click="acceptConnection(connection.user.slug)"
                      no-caps
                      class="on-left"
                      color="primary"
                      >Accept</q-btn
                    >
                    <q-btn
                      @click="denyConnection(connection.user.slug)"
                      no-caps
                      outline
                      >Deny</q-btn
                    >
                  </div>
                </q-item-section>
              </q-item>
            </q-card>
          </q-list>
          <div v-if="!pendingConnection.length" class="q-py-md text-center">
            <span class="text-body1 text-grey-7"
              >There are no pending connections right now.</span
            >
          </div>
        </q-tab-panel>
        <q-tab-panel name="support" class="q-px-xs">
          <q-list>
            <q-card
              v-for="support in cachePendingSupport"
              :key="support.slug"
              class="q-pa-sm q-mb-sm"
            >
              <q-item>
                <q-item-section avatar>
                  <q-avatar class="cursor-pointer" color="primary" size="40px">
                    <q-icon name="fas fa-flag" color="white"></q-icon>
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <q-item-label
                    ><span v-text="support.reason"></span
                  ></q-item-label>
                  <q-item-label caption
                    ><span v-text="support.description"></span>
                  </q-item-label>
                  <q-item-label>
                    <q-btn
                      size="12px"
                      :to="{
                        name: 'Post Details',
                        params: { slug: support.attrs.slug }
                      }"
                      no-caps
                      class="q-mt-sm on-left"
                      color="accent"
                      >View</q-btn
                    >
                  </q-item-label>
                </q-item-section>
                <q-item-section
                  v-if="pendingSupportList.includes(support.slug)"
                  side
                >
                  <div>
                    <q-btn
                      @click="acceptSupport(support.slug)"
                      no-caps
                      class="on-left"
                      color="primary"
                      >Accept</q-btn
                    >
                    <q-btn @click="denySupport(support.slug)" no-caps outline
                      >Deny</q-btn
                    >
                  </div>
                </q-item-section>
              </q-item>
            </q-card>
          </q-list>
          <div v-if="!pendingSupports.length" class="q-py-md text-center">
            <span class="text-body1 text-grey-7"
              >There are no pending supports right now.</span
            >
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
    <div class="col-12 col-md-2 col-lg-4 gt-md"></div>
  </div>
</template>

<script src="./Connections.js" />
