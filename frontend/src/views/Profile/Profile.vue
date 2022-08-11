<template>
  <div class="row justify-lg-around q-pl-md-lg q-pl-lg-none q-mt-md">
    <div class="col-12 col-md-8 col-lg-7">
      <div :class="[$q.screen.lt.md ? 'column items-center' : 'row no-wrap']">
        <q-avatar
          :color="userProfileData.icon_color || 'primary'"
          size="120px"
          class="q-mr-md-lg"
        >
          <q-img
            v-if="userProfileData.photo"
            :src="userProfileData.photo"
          ></q-img>
          <q-icon
            v-else
            :name="userProfileData.icon_name || avatarIcon[userGroup]"
            color="white"
          ></q-icon>
        </q-avatar>
        <div
          class="q-mt-md q-mt-md-none q-ml-md-md full-width"
          :class="[$q.screen.lt.md ? 'text-center' : 'text-left']"
        >
          <span class="text-h5 text-weight-medium">
            <span v-text="userProfileData.full_name" />
            <q-icon
              v-if="userProfileData.is_anonymous && !slug"
              name="fas fa-mask"
              size="sm"
              style="margin-top: -10px"
              color="accent"
              class="q-ml-sm cursor-pointer"
              right
            >
              <q-tooltip content-class="text-body1"
                >Your currently interacting as anonymous.</q-tooltip
              >
            </q-icon>
          </span>
          <div class="q-mt-xs q-mb-md">
            <p class="text-body1">
              <span
                v-if="
                  userProfileData.groups &&
                    userProfileData.groups[0] !== 'regular'
                "
                class="text-weight-medium text-uppercase"
                v-text="
                  userProfileData.groups[0] === 'organization'
                    ? 'Service Provider (Organization)'
                    : 'Service Provider (Individual)'
                "
              ></span>
              <span
                v-if="
                  userProfileData.groups &&
                    userProfileData.groups[0] !== 'regular' &&
                    userProfileData.profile.bio
                "
              >
                —
              </span>
              <span
                v-if="userProfileData.profile.bio"
                v-text="userProfileData.profile.bio"
              ></span>
            </p>
            <template v-if="!userProfileData.profile.bio">
              <div
                v-if="!slug"
                @click="editHeader"
                class="row justify-center justify-md-start items-center cursor-pointer"
              >
                <q-icon name="fas fa-plus" color="primary" left></q-icon>
                <span
                  class="text-body1 text-primary text-weight-bold link-text"
                >
                  Add bio</span
                >
              </div>
            </template>
          </div>
          <div
            class="q-ml-xs q-mt-sm row no-wrap justify-evenly justify-md-start "
          >
            <div
              v-for="{ name, icon, label } in engagements.filter(
                ({ name }) =>
                  userGroup !== 'regular' ||
                  (userGroup === 'regular' && name !== 'connection_count')
              )"
              :key="name"
              class="row items-center q-mb-md q-mr-md-lg"
            >
              <q-icon
                :name="icon"
                :color="$q.dark.isActive ? 'white' : 'grey-8'"
                left
              ></q-icon>
              <span
                class="text-weight-medium text-body1 q-mr-sm"
                v-text="userProfileData.profile[name]"
              ></span>
              <span
                class="text-body1"
                v-text="
                  morphFilters.plural(userProfileData.profile[name], label)
                "
              ></span>
            </div>
          </div>
          <div
            v-if="slug"
            class="row items-center justify-center justify-md-start"
          >
            <q-btn
              no-caps
              rounded
              @click="
                ownFollowing.includes(slug)
                  ? unfollowUser(slug)
                  : followUser(slug)
              "
              :outline="!ownFollowing.includes(slug)"
              color="primary"
              class="on-left"
            >
              <span
                v-text="ownFollowing.includes(slug) ? 'Followed' : 'Follow'"
              />
            </q-btn>
            <template v-if="ownGroup !== 'regular' && userGroup !== 'regular'">
              <q-btn
                v-if="!pendingConnection.includes(slug)"
                @click="
                  requestedConnection.includes(slug)
                    ? removeConnectionRequest()
                    : ownConnection.includes(slug)
                    ? null
                    : addAsConnection()
                "
                no-caps
                color="accent"
                class="on-left"
                :outline="
                  requestedConnection.includes(slug) ||
                    !ownConnection.includes(slug)
                "
              >
                <span
                  v-text="
                    requestedConnection.includes(slug)
                      ? 'Cancel Request'
                      : ownConnection.includes(slug)
                      ? 'Connected'
                      : 'Add as Connection'
                  "
                ></span>
                <q-menu
                  v-if="ownConnection.includes(slug)"
                  v-model="isContextMenuVisible"
                  content-class="shadow-10"
                  anchor="bottom left"
                  self="top left"
                  auto-close
                >
                  <q-list padding style="width: 260px" class="q-pa-sm">
                    <q-item
                      @click="removeConnection"
                      v-ripple
                      class="rounded-borders"
                      clickable
                    >
                      <q-item-section avatar>
                        <q-icon name="fas fa-window-close" size="sm"></q-icon>
                      </q-item-section>
                      <q-item-section>
                        <q-item-label class="text-body1">
                          <span>Remove Connection</span>
                        </q-item-label>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-menu>
              </q-btn>
              <q-btn v-else no-caps color="accent" class="on-left" outline>
                <span>Respond</span>
                <q-menu
                  v-model="isContextMenuVisible"
                  content-class="shadow-10"
                  anchor="bottom left"
                  self="top left"
                  auto-close
                >
                  <q-list padding style="width: 200px" class="q-pa-sm">
                    <q-item
                      @click="acceptConnection()"
                      v-ripple
                      class="rounded-borders"
                      clickable
                    >
                      <q-item-section>
                        <q-item-label class="text-body1">
                          <span>Accept</span>
                        </q-item-label>
                      </q-item-section>
                    </q-item>
                    <q-item
                      @click="denyConnection()"
                      v-ripple
                      class="rounded-borders"
                      clickable
                    >
                      <q-item-section>
                        <q-item-label class="text-body1">
                          <span>Deny</span>
                        </q-item-label>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-menu>
              </q-btn>
            </template>

            <q-btn
              v-if="
                ownGroup !== 'regular' ||
                  (ownGroup === 'regular' && userGroup !== 'regular')
              "
              :to="{ name: 'Messages', query: { slug: userProfileData.slug } }"
              no-caps
              round
              class="on-left"
              outline
            >
              <q-icon name="fas fa-comment-dots" size="xs" />
            </q-btn>
            <q-btn
              @click="showReportAccount"
              class="on-left"
              color="negative"
              no-caps
              round
              outline
            >
              <q-icon name="fas fa-flag" size="xs" />
            </q-btn>
          </div>
          <div v-if="!slug" :class="{ 'q-px-lg': $q.screen.lt.md }">
            <q-btn
              @click="editHeader"
              no-caps
              outline
              color="primary"
              class="on-left"
              :class="{ 'full-width q-my-sm': $q.screen.lt.md }"
            >
              Edit header
            </q-btn>
          </div>
        </div>
      </div>
      <q-tabs
        v-model="tabs"
        dense
        class="q-mt-lg q-mx-lg q-mx-md-none"
        align="left"
        content-class="text-body1"
        left-icon="fas fa-chevron-left"
        right-icon="fas fa-chevron-right"
        no-caps
      >
        <q-tab
          v-if="userGroup !== 'regular' || (userGroup === 'regular' && !slug)"
          name="intro"
          label="Intro"
        />
        <q-tab name="posts" label="Posts"> </q-tab>
        <q-tab name="followers" label="Followers" />
        <q-tab name="following" label="Following" />
        <q-tab
          v-if="userGroup !== 'regular'"
          name="connections"
          label="Connections"
        />
      </q-tabs>
      <q-tab-panels v-model="tabs">
        <q-tab-panel
          v-if="userGroup !== 'regular' || (userGroup === 'regular' && !slug)"
          class="q-px-none"
          name="intro"
        >
          <q-card class="q-pa-lg" :square="$q.screen.lt.md" bordered>
            <div v-if="userGroup !== 'regular'" class="q-mb-md">
              <div class="row justify-between">
                <span class="text-h6"
                  ><span v-text="userGroup" class="text-capitalize"></span>'s
                  Information</span
                >
                <q-btn
                  v-if="!slug"
                  @click="editProviderInfo"
                  round
                  dense
                  flat
                  size="md"
                >
                  <q-icon name="fas fa-edit" size="20px"></q-icon>
                </q-btn>
              </div>
              <div class="q-ml-xs q-mt-md">
                <template v-for="info in providerInfo">
                  <div
                    v-if="
                      !slug ||
                        (slug &&
                          userProfileData.profile[info.name] &&
                          typeof userProfileData.profile[info.name] ===
                            'string') ||
                        (slug &&
                          (userProfileData.profile[info.name] || []).length &&
                          typeof userProfileData.profile[info.name] ===
                            'object')
                    "
                    :key="info.name"
                    class="row items-center q-mb-lg no-wrap"
                  >
                    <q-icon
                      :name="info.icon"
                      :color="$q.dark.isActive ? 'white' : 'grey-8'"
                      class="q-mr-lg col-1"
                      size="22px"
                    ></q-icon>
                    <div
                      v-if="(userProfileData.profile[info.name] || []).length"
                    >
                      <template v-if="info.name === 'tags'">
                        <q-chip
                          v-for="tag in userProfileData.profile[info.name]"
                          :key="tag"
                          color="accent"
                          text-color="white"
                          class="text-body2 text-weight-medium q-mb-sm"
                          clickable
                          outline
                        >
                          <span v-text="tag" />
                        </q-chip>
                      </template>
                      <span
                        v-else
                        class="text-body1"
                        v-text="userProfileData.profile[info.name]"
                      ></span>
                    </div>
                    <template v-else>
                      <div
                        v-if="!slug"
                        @click="editProviderInfo"
                        class="row justify-center justify-md-start items-center cursor-pointer"
                      >
                        <q-icon
                          name="fas fa-plus"
                          color="primary"
                          size="14px"
                          left
                        ></q-icon>
                        <span
                          class="text-body1 text-primary text-weight-medium link-text"
                        >
                          Add <span v-text="info.label || info.name"
                        /></span>
                      </div>
                    </template>
                  </div>
                </template>
              </div>
            </div>
            <div v-else>
              <div>
                <div class="row justify-between items-center">
                  <span class="text-h6">Personal Information</span>
                  <q-btn
                    v-if="!slug"
                    @click="editRegularInfo"
                    round
                    dense
                    flat
                    size="md"
                  >
                    <q-icon name="fas fa-edit" size="20px"></q-icon>
                  </q-btn>
                </div>
                <p class="text-body1 q-my-sm">
                  Your information here will not be posted publicly. We are
                  asking for these information in times you need help and we can
                  know how to contact you.
                </p>
                <div class="q-ml-xs q-mt-md">
                  <template v-for="info in regularIntroInfo">
                    <div
                      v-if="!slug"
                      :key="info.name"
                      class="row items-center q-mb-lg no-wrap"
                    >
                      <q-icon
                        :name="info.icon"
                        :color="$q.dark.isActive ? 'white' : 'grey-8'"
                        class="q-mr-lg col-1"
                        size="22px"
                      ></q-icon>
                      <div
                        v-if="(userProfileData.profile[info.name] || []).length"
                      >
                        <template v-if="info.name === 'tags'">
                          <q-chip
                            v-for="tag in userProfileData.profile[info.name]"
                            :key="tag"
                            color="accent"
                            text-color="white"
                            class="text-body2 text-weight-medium q-mb-sm"
                            clickable
                            outline
                          >
                            <span v-text="tag" />
                          </q-chip>
                        </template>
                        <span
                          v-else
                          class="text-body1"
                          v-text="userProfileData.profile[info.name]"
                        ></span>
                      </div>
                      <template v-else>
                        <div
                          v-if="!slug"
                          @click="editRegularInfo"
                          class="row justify-center no-wrap justify-md-start items-center cursor-pointer"
                        >
                          <q-icon
                            name="fas fa-plus"
                            color="primary"
                            size="14px"
                            left
                          ></q-icon>
                          <span
                            class="text-body1 text-primary text-weight-medium link-text"
                          >
                            Add <span v-text="info.label || info.name"
                          /></span>
                        </div>
                      </template>
                    </div>
                  </template>
                </div>
              </div>
            </div>
          </q-card>
        </q-tab-panel>

        <q-tab-panel class="q-px-none" name="posts">
          <base-post
            v-for="(userPost, i) in userPosts"
            :key="userPost.slug"
            :post="userPost"
            @delete="deletePost(userPost.slug, i)"
            @save="bookmarkPost(userPost.slug, i, userPost.is_saved)"
            @report="showReportDialog(userPost.slug)"
            @support="showSupportDialog(userPost.slug)"
          ></base-post>
          <div class="q-py-md text-center">
            <span class="text-body1 text-grey-7">
              Looks like you have reached the end of this page
            </span>
          </div>
        </q-tab-panel>

        <q-tab-panel name="followers">
          <q-card
            v-for="follower in userFollower"
            :key="follower.slug"
            class="q-pa-xs q-mb-sm"
            :square="$q.screen.lt.md"
            bordered
          >
            <q-item>
              <q-item-section avatar class="q-mr-sm">
                <q-avatar
                  class="cursor-pointer"
                  @click="
                    $router.push({
                      name: 'User Profile',
                      params: { slug: follower.slug }
                    })
                  "
                  :color="follower.icon_color || 'primary'"
                  size="40px"
                >
                  <q-img v-if="follower.photo" :src="follower.photo"></q-img>
                  <q-icon
                    v-else
                    :name="follower.icon_name || avatarIcon[follower.groups[0]]"
                    color="white"
                  ></q-icon>
                </q-avatar>
              </q-item-section>
              <q-item-section class="text-body1 text-weight-medium inline">
                <post-name-label :author="follower"></post-name-label>
                <q-item-label v-if="follower.groups[0] !== 'regular'" caption>
                  <span
                    v-text="
                      follower.groups[0] === 'provider'
                        ? 'Service Provider (Individual)'
                        : 'Service Provider (Organization)'
                    "
                  ></span>
                </q-item-label>
              </q-item-section>
              <q-item-section v-if="follower.slug !== user.slug" side>
                <q-btn
                  @click="
                    ownFollowing.includes(follower.slug)
                      ? unfollowUser(follower.slug)
                      : followUser(follower.slug)
                  "
                  color="primary"
                  rounded
                  :outline="!ownFollowing.includes(follower.slug)"
                  no-caps
                  ><span
                    v-text="
                      ownFollowing.includes(follower.slug)
                        ? 'Followed'
                        : 'Follow'
                    "
                  ></span
                ></q-btn>
              </q-item-section>
            </q-item>
          </q-card>
          <div v-if="!userFollower.length" class="q-py-md text-center">
            <span class="text-body1 text-grey-7">
              This account has no followers yet.
            </span>
          </div>
        </q-tab-panel>

        <q-tab-panel name="following">
          <q-card
            v-for="following in userFollowing"
            :key="following.slug"
            class="q-pa-xs q-mb-sm"
            :square="$q.screen.lt.md"
            bordered
          >
            <q-item>
              <q-item-section avatar class="q-mr-sm">
                <q-avatar
                  class="cursor-pointer"
                  @click="
                    $router.push({
                      name: 'User Profile',
                      params: { slug: following.slug }
                    })
                  "
                  :color="following.icon_color || 'primary'"
                  size="40px"
                >
                  <q-img v-if="following.photo" :src="following.photo"></q-img>
                  <q-icon
                    v-else
                    :name="
                      following.icon_name || avatarIcon[following.groups[0]]
                    "
                    color="white"
                  ></q-icon>
                </q-avatar>
              </q-item-section>
              <q-item-section class="text-body1 text-weight-medium inline">
                <post-name-label :author="following"></post-name-label>
                <q-item-label v-if="following.groups[0] !== 'regular'" caption>
                  <span
                    v-text="
                      following.groups[0] === 'provider'
                        ? 'Service Provider (Individual)'
                        : 'Service Provider (Organization)'
                    "
                  ></span>
                </q-item-label>
              </q-item-section>
              <q-item-section v-if="following.slug !== user.slug" side>
                <q-btn
                  @click="
                    ownFollowing.includes(following.slug)
                      ? unfollowUser(following.slug)
                      : followUser(following.slug)
                  "
                  color="primary"
                  rounded
                  :outline="!ownFollowing.includes(following.slug)"
                  no-caps
                  ><span
                    v-text="
                      ownFollowing.includes(following.slug)
                        ? 'Followed'
                        : 'Follow'
                    "
                  ></span
                ></q-btn>
              </q-item-section>
            </q-item>
          </q-card>
          <div v-if="!userFollowing.length" class="q-py-md text-center">
            <span class="text-body1 text-grey-7">
              This account has no following users yet.
            </span>
          </div>
        </q-tab-panel>

        <q-tab-panel v-if="userGroup !== 'regular'" name="connections">
          <q-card
            v-for="connections in userConnections"
            :key="connections.user.slug"
            class="q-pa-xs q-mb-sm"
            :square="$q.screen.lt.md"
            bordered
          >
            <q-item>
              <q-item-section avatar class="q-mr-sm">
                <q-avatar
                  class="cursor-pointer"
                  @click="
                    $router.push({
                      name: 'User Profile',
                      params: { slug: connections.user.slug }
                    })
                  "
                  :color="connections.user.icon_color || 'primary'"
                  size="40px"
                >
                  <q-img
                    v-if="connections.user.photo"
                    :src="connections.user.photo"
                  ></q-img>
                  <q-icon
                    v-else
                    :name="
                      connections.user.icon_name ||
                        avatarIcon[connections.user.groups[0]]
                    "
                    color="white"
                  ></q-icon>
                </q-avatar>
              </q-item-section>
              <q-item-section class="text-body1 text-weight-medium inline">
                <post-name-label :author="connections.user"></post-name-label>
                <q-item-label
                  v-if="connections.user.groups[0] !== 'regular'"
                  caption
                >
                  <span
                    v-text="
                      connections.user.groups[0] === 'provider'
                        ? 'Service Provider (Individual)'
                        : 'Service Provider (Organization)'
                    "
                  ></span>
                </q-item-label>
              </q-item-section>
              <q-item-section v-if="connections.user.slug !== user.slug" side>
                <q-btn
                  @click="
                    ownFollowing.includes(connections.user.slug)
                      ? unfollowUser(connections.user.slug)
                      : followUser(connections.user.slug)
                  "
                  color="primary"
                  rounded
                  :outline="!ownFollowing.includes(connections.user.slug)"
                  no-caps
                  ><span
                    v-text="
                      ownFollowing.includes(connections.user.slug)
                        ? 'Followed'
                        : 'Follow'
                    "
                  ></span
                ></q-btn>
              </q-item-section>
            </q-item>
          </q-card>
          <div v-if="!userConnections.length" class="q-py-md text-center">
            <span class="text-body1 text-grey-7">
              This account has no connections yet.
            </span>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
    <div class="col-12 col-md-2 col-lg-4 gt-md">
      <ads-trends-column></ads-trends-column>
      <sticky-side-section></sticky-side-section>
    </div>
    <app-dialog
      ref="editHeaderForms"
      :maximized="$q.screen.lt.md"
      width="560px"
      :loading="loading"
      card-class="q-pa-lg"
      close
    >
      <template #header>
        <span class="">Edit Header</span>
      </template>
      <div>
        <div
          v-if="userGroup === 'regular'"
          class="row items-center no-wrap q-gutter-x-lg"
        >
          <q-avatar :color="headerData.icon_color" size="88px">
            <q-icon
              :name="headerData.icon_name"
              size="lg"
              color="white"
            ></q-icon>
          </q-avatar>
          <div class="col-grow column q-gutter-y-md">
            <app-form-input
              v-model="headerData.icon_name"
              field-type="select"
              label="Icon"
              :options="iconOptions"
              emit-value
              map-options
              dense
              outlined
            >
            </app-form-input>

            <app-form-input
              v-model="headerData.icon_color"
              field-type="select"
              label="Color"
              :options="colorOptions"
              dense
              outlined
              emit-value
              map-options
            >
            </app-form-input>
          </div>
        </div>
        <div v-else class="column items-center no-wrap q-gutter-x-lg">
          <q-avatar color="primary" size="88px">
            <q-img v-if="photoURL" :src="photoURL"></q-img>
            <q-img
              v-else-if="userProfileData.photo"
              :src="userProfileData.photo"
            ></q-img>
            <q-icon
              v-else
              :name="avatarIcon[ownGroup]"
              size="lg"
              color="white"
            ></q-icon>
          </q-avatar>

          <div>
            <q-btn
              @click="fileUpload"
              color="accent"
              no-caps
              class="q-mt-md"
              :class="{ 'on-left': userProfileData.photo }"
              >Upload</q-btn
            >
            <q-btn
              v-if="userProfileData.photo"
              @click="removePhoto"
              outline
              no-caps
              class="q-mt-md"
              >Remove</q-btn
            >
          </div>
        </div>
      </div>
      <q-separator class="q-my-lg"></q-separator>
      <div>
        <app-form-input
          v-model="headerData.bio"
          outlined
          label="Bio"
          hint="Maximum of 320 characters only"
          type="textarea"
          rows="3"
          maxlength="320"
        >
        </app-form-input>
        <q-btn
          @click="updateHeaderData"
          class="full-width q-mt-lg"
          color="primary"
          no-caps
        >
          Save Changes
        </q-btn>
      </div>
    </app-dialog>
    <app-dialog
      ref="editProviderIntroForms"
      :maximized="$q.screen.lt.md"
      width="560px"
      card-class="q-pa-lg"
      :loading="loading"
      close
    >
      <template #header>
        <span class="">Edit Intro</span>
      </template>
      <div class="column q-gutter-y-md">
        <template v-for="field in providerInfoFields">
          <app-form-input
            :key="field.key"
            v-model="providerIntro[field.key]"
            :field-type="field.fieldType"
            @new-value="createValue"
            v-bind="field.attrs"
            outlined
          >
            <template
              v-if="
                field.fieldType === 'select' && providerIntro[field.key].length
              "
              #selected
            >
              <q-chip
                v-for="(tag, i) in providerIntro[field.key]"
                :key="tag"
                dense
                square
                color="accent"
                text-color="white"
                class="text-weight-medium"
                close
                removable
                icon-remove="fas fa-times"
                @remove="$delete(providerIntro[field.key], i)"
              >
                <span v-text="tag" />
              </q-chip>
            </template>
          </app-form-input>
          <app-form-input
            v-if="field.key === 'email'"
            :value="providerIntro.email === user.username"
            :key="`${field.key}-check`"
            @input="setContactEmail"
            field-type="checkbox"
            label="Use my username as my contact email"
            class="text-body2"
            dense
          ></app-form-input>
        </template>
        <q-btn
          @click="updateProviderIntro"
          class="full-width q-mt-lg"
          color="primary"
          no-caps
        >
          Save Changes
        </q-btn>
      </div>
    </app-dialog>
    <app-dialog
      ref="editRegularIntroForms"
      :maximized="$q.screen.lt.md"
      width="560px"
      card-class="q-pa-lg"
      :loading="loading"
      close
    >
      <template #header>
        <span class="">Edit Intro</span>
      </template>
      <div class="column q-gutter-y-md">
        <template v-for="field in regularInfoFields">
          <app-form-input
            :key="field.key"
            v-model="regularIntro[field.key]"
            v-bind="field.attrs"
            outlined
          >
          </app-form-input>
          <app-form-input
            v-if="field.key === 'email'"
            :value="regularIntro.email === user.username"
            :key="`${field.key}-check`"
            @input="setRegularContactEmail"
            field-type="checkbox"
            label="Use my username as my contact email"
            class="text-body2"
            dense
          ></app-form-input>
        </template>
        <q-btn
          @click="updateRegularIntro"
          class="full-width q-mt-lg"
          color="primary"
          no-caps
        >
          Save Changes
        </q-btn>
      </div>
    </app-dialog>
    <app-dialog
      ref="editRegularIntroForms"
      :maximized="$q.screen.lt.md"
      width="560px"
      card-class="q-pa-lg"
      :loading="loading"
      close
    >
      <template #header>
        <span class="">Edit Intro</span>
      </template>
      <div class="column q-gutter-y-md">
        <template v-for="field in regularInfoFields">
          <app-form-input
            :key="field.key"
            v-model="regularIntro[field.key]"
            v-bind="field.attrs"
            outlined
          >
          </app-form-input>
          <app-form-input
            v-if="field.key === 'email'"
            :value="regularIntro.email === user.username"
            :key="`${field.key}-check`"
            @input="setRegularContactEmail"
            field-type="checkbox"
            label="Use my username as my contact email"
            class="text-body2"
            dense
          ></app-form-input>
        </template>
        <q-btn
          @click="updateRegularIntro"
          class="full-width q-mt-lg"
          color="primary"
          no-caps
        >
          Save Changes
        </q-btn>
      </div>
    </app-dialog>
    <app-dialog
      ref="reportAccount"
      :maximized="$q.screen.lt.md"
      width="560px"
      card-class="q-px-lg q-pb-lg q-pt-md"
      :loading="loading"
      close
    >
      <template #header>
        <span class="">Report Account</span>
      </template>
      <template #default="{cancel}">
        <p class="text-body1 q-mb-sm text-weight-medium">
          What problem are you having with
          <span v-text="userProfileData.full_name"></span>?
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
            @click="reportAccount"
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
    <app-dialog
      ref="removeConnection"
      :maximized="$q.screen.lt.md"
      width="560px"
      card-class="q-px-lg q-pb-lg q-pt-md"
      close
    >
      <template #header>
        <span class="">Remove Connection</span>
      </template>
      <template #default="{confirm, cancel}">
        <p class="text-body1">
          Are you sure you want to remove
          <span v-text="userProfileData.full_name"></span> on your connections?
        </p>

        <div class="q-mt-md">
          <q-btn @click="confirm" no-caps color="negative" class=" on-left"
            >Yes</q-btn
          >
          <q-btn @click="cancel" no-caps outline>Cancel</q-btn>
        </div>
      </template>
    </app-dialog>
    <report-dialog ref="report" @click:report="reportPost" :loading="loading" />
    <support-dialog
      ref="support"
      @click:support="supportPost"
      :loading="loading"
    ></support-dialog>
    <input
      @change="onUpload"
      type="file"
      ref="fileUploader"
      v-show="false"
      accept=".png,.jpeg,.jpg"
    />
  </div>
</template>

<script src="./Profile.js" />
