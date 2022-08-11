<template>
  <div class="q-py-md q-py-md-none q-px-md q-mx-md-sm">
    <span class="text-h4 text-weight-medium">
      Service Provider
    </span>
    <div class="q-mt-md" v-if="pseudoRecommend.length">
      <span class="text-h5 text-weight-medium">
        Recommended for you
      </span>
    </div>
    <div class="row q-mt-md">
      <div
        v-for="provider in pseudoRecommend"
        :key="provider.slug"
        class="col-md-4  q-gutter-lg"
      >
        <q-card class="column q-mx-lg q-mb-lg q-pa-lg items-center">
          <div class="">
            <q-avatar :color="provider.icon_color || 'primary'" size="120px">
              <q-img v-if="provider.photo" :src="provider.photo"></q-img>
              <q-icon
                v-else
                :name="provider.icon_name || avatarIcon[provider.groups[0]]"
                color="white"
              ></q-icon>
            </q-avatar>
          </div>
          <div class="q-mt-md text-center">
            <div>
              <span
                class="text-h5 text-weight-bold"
                v-text="provider.full_name"
              ></span>
              <q-icon
                name="fas fa-check-circle"
                color="green"
                style="margin-top: -8px"
                right
              ></q-icon>
            </div>
            <p v-text="provider.profile.bio"></p>
            <q-btn
              @click="
                user.slug === provider.slug
                  ? $router.push({ name: 'Profile' })
                  : $router.push({
                      name: 'User Profile',
                      params: { slug: provider.slug }
                    })
              "
              color="primary"
              no-caps
              >View Profile</q-btn
            >
          </div>
        </q-card>
      </div>
    </div>
    <div class="q-mt-md" v-if="pseudoRecommend.length">
      <span class="text-h5 text-weight-medium">
        Other providers you might be interested
      </span>
    </div>
    <div class="row q-mt-md">
      <div
        v-for="provider in providers"
        :key="provider.slug"
        class="col-md-4  q-gutter-lg"
      >
        <q-card class="column q-mx-lg q-mb-lg q-pa-lg items-center">
          <div class="">
            <q-avatar :color="provider.icon_color || 'primary'" size="120px">
              <q-img v-if="provider.photo" :src="provider.photo"></q-img>
              <q-icon
                v-else
                :name="provider.icon_name || avatarIcon[provider.groups[0]]"
                color="white"
              ></q-icon>
            </q-avatar>
          </div>
          <div class="q-mt-md text-center">
            <div>
              <span
                class="text-h5 text-weight-bold"
                v-text="provider.full_name"
              ></span>
              <q-icon
                name="fas fa-check-circle"
                color="green"
                style="margin-top: -8px"
                right
              ></q-icon>
            </div>
            <p v-text="provider.profile.bio"></p>
            <q-btn
              @click="
                user.slug === provider.slug
                  ? $router.push({ name: 'Profile' })
                  : $router.push({
                      name: 'User Profile',
                      params: { slug: provider.slug }
                    })
              "
              color="primary"
              no-caps
              >View Profile</q-btn
            >
          </div>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script src="./ServiceProviders.js" />
