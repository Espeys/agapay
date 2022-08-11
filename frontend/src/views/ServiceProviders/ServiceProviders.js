import { request } from "@/services";

export default {
  data() {
    return {
      providers: [],
      avatarIcon: {
        regular: "fas fa-user",
        provider: "fas fa-hands-helping",
        organization: "fas fa-building"
      },
      pseudoRecommend: []
    };
  },
  computed: {
    user() {
      return this.$store.state.auth.user;
    }
  },
  async mounted() {
    const response = await request("recommend/services/empty/");
    console.log(response);
    if (response.success) {
      this.pseudoRecommend = [...response.data.items].splice(0,1);
    }

    const { success, data } = await request("recommend/services/");
    if (success) this.providers = [...data.items];
  }
};
