<template>
  <div>
    <div class="column items-center">
      <div>
        <q-img :src="require('@/assets/solo.png')" width="80px" />
      </div>
      <div class="text-center q-mt-md">
        <span class="text-h4 text-weight-bold">Create an account</span>
        <p class="text-body1 text-weight-regular ">
          Every little helps.
        </p>
      </div>
    </div>
    <div class="q-mt-md q-px-md-lg">
      <app-form-input
        v-model="selectedUserType"
        field-type="select"
        label="I am a ..."
        class="q-mb-md"
        :options="userTypes"
        emit-value
        map-options
        outlined
      />
      <app-form-input
        v-for="field in selectedSpecificFields"
        :key="field.key"
        v-model="signupData[field.key]"
        :error-message="field['error-message']"
        @input="
          deleteErrorMessages(specificSignupFields[selectedUserType], field.key)
        "
        @keypress.enter="signup"
        class="q-mb-md"
        v-bind="field.attrs"
        outlined
      />
      <app-form-input
        v-for="field in defaultSignupFields"
        :key="field.key"
        v-model="signupData[field.key]"
        :error-message="field['error-message']"
        @input="deleteErrorMessages(defaultSignupFields, field.key)"
        @keypress.enter="signup"
        class="q-mb-md"
        v-bind="field.attrs"
        outlined
      />
      <div class="q-mt-lg">
        <p class="text-body1">
          By signing up, I agree to the
          <span class="link-text text-primary cursor-pointer">
            Terms of Use
          </span>
          and
          <span class="link-text text-primary cursor-pointer"
            >Privacy Policy</span
          >.
        </p>
      </div>
      <div>
        <q-btn
          @click="signup"
          no-caps
          color="primary"
          :class="{ 'full-width': $q.screen.lt.md }"
          class="text-body1 text-weight-bold"
          >Sign up</q-btn
        >
      </div>
    </div>
    <q-separator class="q-my-lg q-mx-md-lg"></q-separator>
    <div class="column items-center">
      <p
        @click="$emit('switch-page')"
        class="q-mb-none text-body2 text-weight-medium cursor-pointer text-underline text-center"
      >
        Already have an account ? Login here.
      </p>
    </div>
    <q-inner-loading :showing="loading">
      <q-spinner-hourglass color="primary" size="5.5em" class="q-mb-md" />
      <span class="text-body2"> Please wait ...</span>
    </q-inner-loading>
  </div>
</template>

<script src="./Signup.js" />
