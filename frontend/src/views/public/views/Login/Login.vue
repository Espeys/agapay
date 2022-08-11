<template>
  <div>
    <div class="column items-center">
      <div>
        <q-img :src="require('@/assets/solo.png')" width="80px" />
      </div>
      <div class="text-center q-mt-md">
        <span class="text-h4 text-weight-bold">Login</span>
        <p class="text-body1 text-weight-regular ">
          Help us to break the stigma
        </p>
      </div>
    </div>
    <div class="q-mt-md q-px-md-lg">
      <app-form-input
        v-model="authCredentials.username"
        :error-message="fields[0]['error-message']"
        @input="deleteErrorMessages(fields, 'username')"
        @keypress.enter="login"
        label="Email address / Username"
        class="text-body1 q-mb-md"
        type="email"
        stack-label
        outlined
      />
      <app-form-input
        v-model="authCredentials.password"
        :error-message="fields[1]['error-message']"
        @input="deleteErrorMessages(fields, 'password')"
        @keypress.enter="login"
        type="password"
        label="Password"
        class="q-mb-lg"
        stack-label
        outlined
      />
      <div class="text-center row-md justify-between items-center">
        <q-btn
          @click="login"
          no-caps
          color="primary"
          class="text-body1 text-weight-bold"
          :class="{ 'full-width': $q.screen.lt.md }"
          >Login</q-btn
        >
        <span
          @click="$emit('show-forgot-password')"
          class="link-text cursor-pointer text-primary text-body-2 q-my-lg q-my-md-none"
          :class="{ block: $q.screen.lt.md }"
          >Forgot your password?</span
        >
      </div>
    </div>
    <q-separator class="q-my-lg q-mx-md-lg"></q-separator>
    <div class="column items-center">
      <p
        @click="$emit('switch-page')"
        class="q-mb-none text-body2 text-weight-medium cursor-pointer text-underline text-center"
      >
        Don't have an account yet? Sign up now.
      </p>
    </div>
    <q-inner-loading :showing="loading">
      <q-spinner-hourglass color="primary" size="5.5em" class="q-mb-md" />
      <span class="text-body2"> Please wait ...</span>
    </q-inner-loading>
  </div>
</template>

<script src="./Login.js" />
