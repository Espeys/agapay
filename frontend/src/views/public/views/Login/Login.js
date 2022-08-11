import { errorHandling, formMixins, asyncLoader } from "@/mixins";

export default {
  mixins: [errorHandling, formMixins, asyncLoader],
  data() {
    return {
      authCredentials: {
        username: "",
        password: ""
      },
      fields: [{ key: "username" }, { key: "password" }]
    };
  },
  methods: {
    async login() {
      this.startLoading();
      const response = await this.$store.dispatch(
        "auth/login",
        this.authCredentials
      );

      await this.timeout();

      this.stopLoading();

      const { success } = response;
      if (!success) this.checkErrors(this.fields, response);
      else this.$router.go();
    }
  }
};
