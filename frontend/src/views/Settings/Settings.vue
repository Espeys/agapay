<template>
  <div class="q-py-md q-py-md-none q-px-md q-mx-md-sm">
    <span class="text-h4 text-weight-medium">
      Settings
    </span>
    <div class="q-mt-md">
      <q-expansion-item
        v-model="isChangingPassword"
        :duration="0"
        popup
        icon="fas fa-lock"
        label="Change Password"
        header-class="text-body1 text-weight-medium"
        expand-icon="fas fa-chevron-right"
        expanded-icon="fas fa-times"
        :disable="disabled"
        caption="It's a good idea to use a strong password that you're not using elsewhere"
      >
        <q-card class="q-pb-lg q-px-md">
          <div
            class="q-mt-lg q-ml-md-xl relative-position"
            style="max-width: 480px"
          >
            <app-form-input
              v-for="field in changePasswordFields"
              :key="field.key"
              v-model="passwordData[field.key]"
              :error-message="field['error-message']"
              @input="deleteErrorMessages(changePasswordFields, field.key)"
              @keypress.enter="changePassword"
              v-bind="field.attrs"
              class="q-mb-md"
              type="password"
              outlined
            >
            </app-form-input>
            <p class="text-body2">
              Once you changed your password, you will be logged out of all your
              current sessions, including the one you're in right now.
            </p>
            <div class="q-my-md">
              <q-btn
                @click="changePassword"
                color="primary"
                class="on-left"
                no-caps
              >
                Save Changes
              </q-btn>
              <q-btn @click="cancelChanging" no-caps outline>
                Cancel
              </q-btn>
            </div>
            <q-inner-loading :showing="loading">
              <q-spinner-hourglass
                color="primary"
                size="5.5em"
                class="q-mb-md"
              />
              <span class="text-body2"> Please wait ...</span>
            </q-inner-loading>
          </div>
        </q-card>
      </q-expansion-item>
    </div>
  </div>
</template>

<script src="./Settings.js" />
