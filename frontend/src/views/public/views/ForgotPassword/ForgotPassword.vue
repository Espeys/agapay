<template>
  <div>
    <div>
      <p class="text-body1">
        <span v-if="!isRetrieved">
          Don't worry, just enter your email address and we will send you an
          email on how to retrieve your account.
          <span class="text-weight-medium">
            Please note that your recent password cannot be used again once we
            retrieve your account.
          </span>
        </span>
        <span v-else>
          We are able to retrieve your account successfully. We sent you an
          email on your email account,
          <span v-text="username" class="text-primary text-weight-medium"></span
          >, on how you will access your Agapay account temporarily.
        </span>
      </p>
      <div v-if="!isRetrieved">
        <app-form-input
          v-model="username"
          :error-message="fields[0]['error-message']"
          @input="deleteErrorMessages(fields, 'username')"
          @keypress.enter="retrieveAccount"
          outlined
          dense
          type="email"
          placeholder="Enter your email address..."
        >
        </app-form-input>
        <div class="q-mt-lg">
          <q-btn
            :class="{ 'full-width': $q.screen.lt.md }"
            @click="retrieveAccount"
            color="primary"
            class="on-left"
            no-caps
          >
            Continue
          </q-btn>
          <q-btn
            @click="$emit('cancel')"
            class="q-mt-md q-mt-md-none"
            :class="{ 'full-width': $q.screen.lt.md }"
            no-caps
            outline
          >
            Cancel
          </q-btn>
        </div>
      </div>
      <q-btn
        v-else
        @click="$emit('cancel')"
        :class="{ 'full-width': $q.screen.lt.md }"
        color="primary"
        no-caps
      >
        Okay
      </q-btn>
    </div>
    <q-inner-loading :showing="loading">
      <q-spinner-hourglass color="primary" size="5.5em" class="q-mb-md" />
      <span class="text-body2"> Please wait ...</span>
    </q-inner-loading>
  </div>
</template>

<script src="./ForgotPassword.js" />
