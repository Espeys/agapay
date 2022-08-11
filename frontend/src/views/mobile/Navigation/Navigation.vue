<template>
  <div class="q-pa-md">
    <q-list>
      <q-item
        v-for="menu in userBasedMenu"
        :key="menu.to"
        v-ripple
        class="rounded-borders q-mb-sm"
        :class="[$q.dark.isActive ? 'text-white' : 'text-black']"
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
      <q-item
        v-ripple
        class="rounded-borders"
        :class="[$q.dark.isActive ? 'text-white' : 'text-black']"
        clickable
        @click="logout"
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
    </q-list>
    <div class="q-pl-md q-mt-sm text-body2 wrap row">
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
</template>

<script src="./Navigation.js" />
