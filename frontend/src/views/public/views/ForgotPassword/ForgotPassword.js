import { errorHandling, formMixins, asyncLoader } from "@/mixins";

export default {
  mixins: [errorHandling, formMixins, asyncLoader],
  data() {
    return {
      username: "",
      fields: [{ key: "username" }],
      isRetrieved: false
    };
  },
  methods: {
    async retrieveAccount() {
      this.startLoading();
      const response = await this.$store.dispatch("auth/retrieveAccount", {
        username: this.username
      });

      await this.timeout();
      this.stopLoading();

      const { data } = response;
      this.isRetrieved = data;
      if (!data) this.checkErrors(this.fields, response);
    }
  }
};
