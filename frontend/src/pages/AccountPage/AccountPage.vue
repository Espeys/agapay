<template>
  <q-layout view="hHh lpR lFr">
    <q-header
      class="text-white q-px-md-md q-px-xs q-py-sm row justify-center"
      :class="[$q.dark.isActive ? 'bg-dark' : 'bg-white']"
      bordered
    >
      <q-toolbar class="row" style="max-width: 1464px">
        <div class="col-auto col-md-3">
          <router-link to="/">
            <q-img
              @click="reload"
              :src="require('@/assets/solo.png')"
              width="48px"
              class="cursor-pointer q-mr-md lt-md"
            />
            <q-img
              @click="reload"
              :src="
                require($q.dark.isActive
                  ? '@/assets/h-logo-white.png'
                  : '@/assets/h-logo.png')
              "
              width="160px"
              class="cursor-pointer gt-sm"
            />
          </router-link>
        </div>
        <div class="row col-grow justify-between q-pl-md-md">
          <div class="col-grow col-md-7">
            <app-form-input
              v-if="isAuthenticated"
              v-model="search"
              @keypress.enter="queryData"
              placeholder="Search ..."
              :standout="$q.dark.isActive"
              :outlined="!$q.dark.isActive"
              rounded
            >
              <template #prepend>
                <q-icon name="eva-search-outline"></q-icon>
              </template>
            </app-form-input>
          </div>

          <div class="col-auto col-lg-4 row items-center justify-end no-wrap">
            <div v-if="isAuthenticated">
              <q-btn
                :to="{ name: 'Post Creation' }"
                color="primary"
                class="q-ml-md q-mr-md-md"
                size="16px"
                round
                dense
              >
                <q-icon name="fas fa-feather" size="18px"></q-icon>
                <q-tooltip content-class="text-body2">
                  <span v-text="'Create Post'" />
                </q-tooltip>
              </q-btn>
              <q-btn
                v-for="({ icon, key, label, to }, index) in headerButtons"
                :key="icon"
                :color="$q.dark.isActive ? 'white' : 'grey-9'"
                class="gt-sm"
                :class="{ 'q-mr-md': index < headerButtons.length - 1 }"
                :to="to"
                round
                dense
                flat
              >
                <q-icon :name="icon"></q-icon>
                <q-badge
                  v-if="
                    key === 'notif' &&
                      notifications.filter(notif => !notif.is_readed).length
                  "
                  color="red"
                  text-color="white"
                  floating
                >
                  <span
                    v-text="
                      notifications.filter(notif => !notif.is_readed).length
                    "
                  ></span>
                </q-badge>
                <q-menu
                  v-if="key === 'notif'"
                  v-model="isNotificationVisible"
                  content-class="shadow-10"
                  anchor="bottom right"
                  self="top right"
                >
                  <div class="q-mx-lg q-mt-md">
                    <span class="text-h6">Notifications</span>
                    <q-separator class="q-mt-sm"></q-separator>
                  </div>
                  <q-list
                    v-if="notifications.length"
                    padding
                    style="width: 400px"
                    class="q-py-sm"
                  >
                    <q-item
                      v-for="notif in notifications"
                      :key="notif.slug"
                      @click="
                        redirect(
                          notif.type,
                          notif.attrs_json.from_slug ||
                            notif.attrs_json.post_slug,
                          notif.slug
                        )
                      "
                      v-ripple
                      class="rounded-borders q-mb-sm q-mx-sm"
                      clickable
                    >
                      <q-item-section avatar>
                        <q-avatar
                          size="56px"
                          :color="notif.created_by.icon_color || 'primary'"
                        >
                          <q-img
                            v-if="notif.created_by.photo"
                            :src="notif.created_by.photo"
                          />
                          <q-icon
                            v-else
                            color="white"
                            :name="
                              notif.created_by.icon_name ||
                                avatarIcon[notif.created_by.groups[0]]
                            "
                            size="20px"
                          ></q-icon>
                        </q-avatar>
                      </q-item-section>
                      <q-item-section>
                        <q-item-label class="text-body1" lines="3">
                          <span v-text="notif.text"></span>
                        </q-item-label>
                        <q-item-label caption>
                          <span v-text="$date(notif.created_at).fromNow()" />
                        </q-item-label>
                      </q-item-section>
                      <q-item-section v-if="!notif.is_readed" side>
                        <q-icon
                          @click.stop=""
                          v-ripple
                          name="fas fa-circle"
                          size="12px"
                          class="cursor-pointer"
                          color="primary"
                        />
                      </q-item-section>
                    </q-item>
                  </q-list>
                  <div
                    v-else
                    class="text-body1 q-px-lg q-py-md"
                    style="width: 400px"
                  >
                    No notifications yet.
                  </div>
                </q-menu>

                <q-tooltip content-class="text-body2">
                  <span v-text="label" />
                </q-tooltip>
              </q-btn>
              <q-btn
                :to="{ name: 'Profile' }"
                round
                class="q-mr-md-xs gt-sm q-ml-md cursor"
              >
                <q-avatar size="42px" :color="user.icon_color || 'primary'">
                  <q-img v-if="user.photo" :src="user.photo" />
                  <q-icon
                    v-else
                    :name="user.icon_name || avatarIcon[group]"
                    size="20px"
                  ></q-icon>
                </q-avatar>
                <q-badge v-if="isAnonymous" color="accent" floating rounded>
                  <q-icon name="fas fa-mask" size="12px"></q-icon>
                </q-badge>
                <q-tooltip content-class="text-body2">Profile</q-tooltip>
              </q-btn>
              <q-btn
                :color="$q.dark.isActive ? 'white' : 'grey-9'"
                class="q-mr-sm gt-sm"
                size="14px"
                icon="eva-arrow-down"
                round
                dense
                flat
              >
                <q-menu
                  v-model="isAccountMenuVisible"
                  content-class="shadow-10"
                  anchor="bottom right"
                  self="top right"
                >
                  <q-list padding style="width: 320px" class="q-pa-sm">
                    <q-item
                      v-ripple
                      class="rounded-borders"
                      :to="{ name: 'Settings' }"
                    >
                      <q-item-section avatar>
                        <q-avatar
                          :text-color="$q.dark.isActive ? 'white' : 'grey-9'"
                          size="md"
                          dark
                          square
                        >
                          <q-icon name="fas fa-cog" size="24px" />
                        </q-avatar>
                      </q-item-section>
                      <q-item-section>
                        <q-item-label
                          class="row text-body1"
                          :class="[
                            $q.dark.isActive ? 'text-white' : 'text-black'
                          ]"
                        >
                          <span>Settings</span>
                        </q-item-label>
                      </q-item-section>
                    </q-item>
                    <q-item
                      @click="logout"
                      v-ripple
                      class="rounded-borders"
                      clickable
                    >
                      <q-item-section avatar>
                        <q-avatar
                          :text-color="$q.dark.isActive ? 'white' : 'grey-9'"
                          size="md"
                          dark
                          square
                        >
                          <q-icon name="fas fa-sign-out-alt" size="24px" />
                        </q-avatar>
                      </q-item-section>
                      <q-item-section>
                        <q-item-label class="row text-body1">
                          <span>Logout</span>
                        </q-item-label>
                      </q-item-section>
                    </q-item>

                    <q-separator class="q-my-sm"></q-separator>
                    <q-item
                      v-if="group === 'regular'"
                      tag="label"
                      class="rounded-borders"
                      v-ripple
                    >
                      <q-item-section>
                        <q-item-label>Anonymous</q-item-label>
                        <q-item-label caption
                          >Do not show my name in public</q-item-label
                        >
                      </q-item-section>
                      <q-item-section avatar>
                        <app-form-input
                          field-type="toggle"
                          v-model="isAnonymous"
                          @input="toggleAnonymous"
                          checked-icon="fas fa-mask"
                          color="accent"
                          unchecked-icon="fas fa-user"
                        />
                      </q-item-section>
                    </q-item>

                    <q-item tag="label" class="rounded-borders" v-ripple dense>
                      <q-item-section>
                        <q-item-label>Dark Mode</q-item-label>
                      </q-item-section>
                      <q-item-section avatar>
                        <app-form-input
                          field-type="toggle"
                          v-model="darkMode"
                          @input="toggleDarkMode"
                          checked-icon="fas fa-moon"
                          color="yellow-7"
                          unchecked-icon="fas fa-sun"
                        />
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-menu>
                <q-tooltip content-class="text-body2">
                  <span v-text="'Account'" />
                </q-tooltip>
              </q-btn>
            </div>
            <div v-else class="row items-center justify-end no-wrap">
              <div class="gt-sm row no-wrap items-center">
                <q-btn
                  @click="login"
                  color="primary"
                  style="width: 128px"
                  class="q-mr-md text-body1 text-weight-bold"
                  no-caps
                  dense
                >
                  Log in
                </q-btn>
                <q-btn
                  @click="signup"
                  color="accent"
                  class="text-body1 text-weight-bold"
                  style="width: 128px"
                  no-caps
                  dense
                >
                  Sign up
                </q-btn>
              </div>
              <q-btn
                :color="$q.dark.isActive ? 'white' : 'grey-9'"
                size="20px"
                class="q-ml-sm q-mt-xs"
                flat
                round
                dense
              >
                <q-icon name="far fa-user-circle" size="md" />
                <q-menu
                  v-model="isMenuVisible"
                  content-class="shadow-10"
                  anchor="bottom right"
                  self="top right"
                >
                  <q-list padding style="width: 320px" class="q-px-sm">
                    <div class="lt-md">
                      <q-item
                        v-for="menu in userBasedMenu"
                        :key="menu.id"
                        v-ripple
                        class="rounded-borders"
                        :class="[
                          $q.dark.isActive ? 'text-white' : 'text-black'
                        ]"
                        :to="{ name: menu.to }"
                      >
                        <q-item-section avatar>
                          <q-avatar
                            :text-color="$q.dark.isActive ? 'white' : 'grey-9'"
                            size="md"
                            dark
                            square
                          >
                            <q-icon :name="menu.icon" size="24px" />
                          </q-avatar>
                        </q-item-section>
                        <q-item-section>
                          <q-item-label class="row text-body1">
                            <span v-text="menu.name" />
                          </q-item-label>
                        </q-item-section>
                      </q-item>

                      <q-separator class="q-my-sm q-mx-md" />
                    </div>

                    <q-item tag="label" class="rounded-borders" v-ripple dense>
                      <q-item-section>
                        <q-item-label>Dark Mode</q-item-label>
                      </q-item-section>
                      <q-item-section avatar>
                        <app-form-input
                          field-type="toggle"
                          v-model="darkMode"
                          @input="toggleDarkMode"
                          checked-icon="fas fa-moon"
                          color="yellow-7"
                          unchecked-icon="fas fa-sun"
                        />
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-menu>
              </q-btn>
            </div>
          </div>
        </div>
      </q-toolbar>
    </q-header>
    <q-page-container>
      <q-page :padding="$q.screen.gt.sm">
        <div class="row q-mx-auto no-wrap" style="max-width: 1464px">
          <div
            v-if="$route.name !== 'Navigation'"
            class="col-12 col-md-3 gt-sm column sticky"
            style="height: 85vh; top: 100px;"
          >
            <div>
              <q-list>
                <q-item
                  v-for="menu in userBasedMenu"
                  :key="menu.id"
                  v-ripple
                  class="rounded-borders"
                  :to="{ name: menu.to }"
                >
                  <q-item-section avatar>
                    <q-avatar
                      :text-color="
                        menu.to === activePathName
                          ? 'primary'
                          : $q.dark.isActive
                          ? 'white'
                          : 'grey-9'
                      "
                      size="md"
                      dark
                      square
                    >
                      <q-icon :name="menu.icon" size="24px" />
                    </q-avatar>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label class="row text-body1">
                      <span
                        v-text="menu.name"
                        :class="{
                          'text-weight-medium text-body1 text-primary':
                            menu.to === activePathName
                        }"
                      />
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>
              <div class="q-pl-md q-py-md text-body2 wrap row">
                <span v-for="keyword in policies" :key="keyword">
                  <span class="link-text cursor-pointer" v-text="keyword" />
                  <span class="text-grey-6 q-px-sm text-caption">●</span>
                </span>
                <div>
                  <span
                    class="text-weight-medium"
                    v-text="`© Agapay ${new Date().getFullYear()}`"
                  />
                </div>
              </div>
            </div>
          </div>
          <q-space />
          <div class="col-12 col-md-9" style="margin-bottom: 80px">
            <router-view />
          </div>
        </div>
      </q-page>
    </q-page-container>

    <q-card
      class="fixed-bottom lt-md shadow-up-2"
      :class="[
        { 'q-py-md q-px-md': !isAuthenticated, 'z-top': isAuthenticated }
      ]"
      bordered
      square
    >
      <div v-if="isAuthenticated && tabs.includes($route.name)">
        <q-tabs
          class="text-body2"
          indicator-color="primary"
          align="justify"
          switch-indicator
        >
          <q-route-tab name="home" :to="{ name: 'Home' }">
            <q-icon name="fa fa-home" size="20px"></q-icon>
          </q-route-tab>
          <q-route-tab name="profile" :to="{ name: 'Profile' }">
            <q-icon name="fas fa-user" size="20px"></q-icon>
          </q-route-tab>
          <q-route-tab name="message" :to="{ name: 'Messages' }">
            <q-icon name="fas fa-envelope" size="20px"></q-icon>
            <q-badge color="red" text-color="white" floating>
              2
            </q-badge>
          </q-route-tab>
          <q-route-tab name="notif" :to="{ name: 'Notification' }">
            <q-icon name="fas fa-bell" size="20px"></q-icon>
            <q-badge color="red" text-color="white" floating>
              2
            </q-badge>
          </q-route-tab>
          <q-route-tab name="menu" :to="{ name: 'Navigation' }">
            <q-icon name="fas fa-bars" size="20px"></q-icon>
          </q-route-tab>
        </q-tabs>
      </div>
      <div v-else-if="!isAuthenticated" class="column items-center">
        <div class="text-center q-mb-sm">
          <span class="text-h6 text-weight-medium">
            Let us know how we can help you!
          </span>
        </div>
        <div class="row no-wrap items-center q-mt-xs">
          <q-btn
            @click="login"
            color="primary"
            style="width: 128px"
            class="text-body1 text-weight-bold"
            no-caps
            dense
          >
            Log in
          </q-btn>
          <span class="q-mx-md text-body2 text-grey-7">or</span>
          <q-btn
            @click="signup"
            color="accent"
            style="width: 128px"
            class="text-body1 text-weight-bold"
            no-caps
            dense
          >
            Sign up
          </q-btn>
        </div>
      </div>
    </q-card>
    <app-dialog
      ref="login"
      :maximized="$q.screen.lt.md"
      card-class="q-px-md q-py-xl"
      width="560px"
      close
    >
      <login
        @switch-page="switchToSignup"
        @show-forgot-password="showForgotPassword"
      ></login>
    </app-dialog>
    <app-dialog
      ref="signup"
      :maximized="$q.screen.lt.md"
      card-class="q-px-md q-py-xl"
      width="560px"
      close
    >
      <signup @switch-page="switchToLogin"></signup>
    </app-dialog>
    <app-dialog
      ref="verificationDialog"
      :maximized="$q.screen.lt.md"
      card-class="q-px-xl q-py-lg"
      width="640px"
    >
      <div
        class="column items-center items-md-start row-md no-wrap-md q-gutter-x-lg"
      >
        <div>
          <q-img
            :src="require('@/assets/not-verified.svg')"
            width="160px"
            class="q-mb-md"
          ></q-img>
        </div>
        <div class="text-center">
          <p class="text-body1">
            Sorry for interrupting, but we found that your account is not
            verified yet. Kindly check your email account,
            <span
              v-text="user.username"
              class="text-primary text-weight-medium"
            />, as we provided you a verification link to proceed.
          </p>
          <q-btn @click="$router.go()" no-caps color="primary"
            >I have already activated my account
          </q-btn>
          <q-btn class="q-mt-md" outline @click="logout" no-caps
            >Logout, I will check it later</q-btn
          >
        </div>
      </div>
      <q-separator class="q-my-lg" v-if="group !== 'regular'"></q-separator>
      <div
        v-if="!user.is_certified && group !== 'regular'"
        class="column items-center items-md-start row-md no-wrap-md q-gutter-x-lg"
      >
        <div class="text-center">
          <span class="text-h6"
            >Why am I still seeing this after I verify my account?</span
          >
          <p class="text-body1 q-mt-sm">
            If you are a
            <span class="text-weight-medium">
              service provider (individual or organization)</span
            >, kindly email us at
            <span class="text-primary text-weight-medium"
              >agapayph@gmail.com</span
            >
            to initialize the verifcation and screening process of your account.
            Thank you for your consideration !
          </p>
        </div>
      </div>
    </app-dialog>
    <app-dialog
      ref="forgotPassword"
      :maximized="$q.screen.lt.md"
      card-class="q-px-lg q-pt-md q-pb-lg"
      width="560px"
      close
    >
      <template #header>
        <span>Forgot Password</span>
      </template>
      <forgot-password @cancel="closeForgotPassword"></forgot-password>
    </app-dialog>

    <app-dialog
      ref="sessionExpired"
      :maximized="$q.screen.lt.md"
      card-class="q-px-lg q-pt-md q-pb-lg"
      width="560px"
    >
      <template #header>
        <span>Session Expired</span>
      </template>
      <div>
        <p class="text-body1">
          Your session has expired. Please login again.
        </p>
        <q-btn @click="closeSessionExpired" color="primary" no-caps>Okay</q-btn>
      </div>
    </app-dialog>
    <app-dialog
      ref="deletePost"
      :maximized="$q.screen.lt.md"
      width="560px"
      card-class="q-px-lg q-pb-lg q-pt-md"
      close
    >
      <template #header>
        <span class="">Delete Post</span>
      </template>
      <template #default="{confirm, cancel}">
        <p class="text-body1">
          Are you sure you want to delete this post?
        </p>

        <div class="q-mt-md">
          <q-btn @click="confirm" no-caps color="negative" class=" on-left"
            >Delete</q-btn
          >
          <q-btn @click="cancel" no-caps outline>Cancel</q-btn>
        </div>
      </template>
    </app-dialog>
  </q-layout>
</template>

<script src="./AccountPage.js" />

<style scoped>
.scrollbox {
  overflow-y: hidden;
}

.scrollbox:hover,
.scrollbox:focus {
  overflow-y: scroll;
}
</style>
