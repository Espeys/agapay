import { PostNameLabel } from "@/views/components";
import store from "@/store";

export default {
  components: {
    PostNameLabel
  },
  data() {
    return {
      tabs: "pending",
      pendingConnections: [],
      cachePendingSupport: [],
      pendingSupports: [],
      avatarIcon: {
        regular: "fas fa-user",
        provider: "fas fa-hands-helping",
        organization: "fas fa-building"
      }
    };
  },
  computed: {
    user() {
      return this.$store.state.auth.user;
    },
    pendingConnection() {
      return this.$store.getters["profile/pendingConnectionsList"];
    },
    pendingSupportList() {
      return this.pendingSupports.map(support => support.slug);
    }
  },
  methods: {
    async acceptConnection(slug) {
      await this.$store.dispatch("profile/setConnectionStatus", {
        slug,
        status: "accept"
      });

      await this.$store.dispatch("profile/getPendingConnections");

      await this.$store.dispatch("profile/getUserConnections", {
        ownData: true,
        slug: this.user.slug
      });
    },
    async denyConnection(slug) {
      await this.$store.dispatch("profile/setConnectionStatus", {
        slug,
        status: "deny"
      });

      await this.$store.dispatch("profile/getPendingConnections");
    },
    async acceptSupport(slug) {
      const response = await this.$store.dispatch("post/acceptSupport", {
        slug
      });
      const { data } = await store.dispatch("post/viewSupports");

      this.pendingSupports = [...data.items];
    },
    async denySupport(slug) {
      await this.$store.dispatch("post/denySupport", {
        slug
      });

      const { data } = await store.dispatch("post/viewSupports");

      this.pendingSupports = [...data.items];
    }
  },
  async beforeRouteEnter(to, from, next) {
    const { data } = await store.dispatch("post/viewSupports");

    next(vm => {
      vm.cachePendingSupport = [...data.items];
      vm.pendingSupports = [...data.items];
      vm.pendingConnections = [...vm.$store.state.profile.pendingConnections];
    });
  }
};
