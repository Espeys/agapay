import { errorHandling, formMixins, asyncLoader } from "@/mixins";

export default {
  mixins: [errorHandling, formMixins, asyncLoader],
  data() {
    return {
      isChangingPassword: false,
      changePasswordFields: [
        { key: "old_password", attrs: { label: "Old Password" } },
        { key: "new_password", attrs: { label: "New Password" } }
      ],
      passwordData: {
        old_password: "",
        new_password: ""
      },
      disabled: false
    };
  },
  methods: {
    async changePassword() {
      this.startLoading();
      const response = await this.$store.dispatch(
        "auth/changePassword",
        this.passwordData
      );

      await this.timeout();
      this.stopLoading();

      const { success } = response;
      if (!success) this.checkErrors(this.changePasswordFields, response);
      else {
        this.$store.dispatch("auth/destroyUserCredentials");
        this.$root.showSessionExpired();
      }
    },
    cancelChanging() {
      this.isChangingPassword = this.disabled = false;
      this.passwordData.old_password = this.passwordData.new_password = "";
    }
  },
  watch: {
    isChangingPassword(nv) {
      if (nv) this.$nextTick(() => (this.disabled = nv));
    }
  }
};
