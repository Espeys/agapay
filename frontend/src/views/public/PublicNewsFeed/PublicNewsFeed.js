import {
  BasePost,
  AdsTrendsColumn,
  StickySideSection,
  ReportDialog,
  SupportDialog
} from "@/views/components";

import { formMixins, asyncLoader } from "@/mixins";

import store from "@/store";
import { request } from "@/services";
export default {
  components: {
    BasePost,
    AdsTrendsColumn,
    StickySideSection,
    ReportDialog,
    SupportDialog
  },
  mixins: [formMixins, asyncLoader],
  data() {
    return {
      topics: [
        "Anxiety Philippines",
        "COVID-19",
        "Mental Health Day",
        "Cabin Fever",
        "Dolomite for Mental Health"
      ],
      posts: {},
      reportedSlug: "",
      supportSlug: "",
      pseudoPosts: []
    };
  },
  computed: {
    isAuthenticated() {
      return this.$store.getters["auth/isAuthenticated"];
    }
  },
  methods: {
    async deletePost(slug, index) {
      const dialogResponse = await this.$root.deletePost();

      if (!dialogResponse) return;
      const { success } = await this.$store.dispatch("post/deletePost", {
        slug
      });
      if (success) this.$delete(this.posts, index);
    },
    async bookmarkPost(slug, index, isSaved) {
      let action = "post/unsavePost";

      if (!isSaved) action = "post/savePost";

      const response = await this.$store.dispatch(action, {
        slug
      });

      const { success, data } = response;

      if (success) this.$set(this.posts, index, data);
    },
    showReportDialog(slug) {
      this.reportedSlug = slug;
      this.$refs.report.showReportDialog();
    },
    async reportPost(reportData) {
      const payload = { ...reportData, slug: this.reportedSlug };

      this.startLoading();
      const response = await this.$store.dispatch("post/reportPost", payload);
      await this.timeout();
      this.stopLoading();

      const { success } = response;
      if (success) {
        this.$refs.report.cancel();
        this.$q.notify({
          message: "Thank you for letting us know.",
          classes: "text-body1",
          position: this.$q.screen.gt.sm ? "bottom-left" : "bottom",
          icon: "fas fa-flag",
          multiLine: this.$q.screen.gt.sm
        });
      }
    },
    showSupportDialog(slug) {
      this.supportSlug = slug;
      this.$refs.support.showSupportDialog();
    },
    async supportPost(supportData) {
      let payload = { ...supportData, post_slug: this.supportSlug };

      payload.slugs = JSON.stringify(payload.slugs);
      this.startLoading();
      const response = await this.$store.dispatch("post/supportPost", payload);
      await this.timeout();
      this.stopLoading();

      const { success } = response;
      if (success) {
        this.$refs.support.cancel();
        this.$q.notify({
          message: "Thank you for letting us know.",
          classes: "text-body1",
          position: this.$q.screen.gt.sm ? "bottom-left" : "bottom",
          icon: "fas fa-flag",
          multiLine: this.$q.screen.gt.sm
        });
      }
    }
  },
  async beforeRouteEnter(to, from, next) {
    let visiblePost = [];
    let pseudoItems = [];

    const { data: promotions } = await store.dispatch("post/getPosts", {
      filter: JSON.stringify({ item_type: "promotion" }),
      order_values: -1
    });
    if (store.getters['auth/isAuthenticated']) {
      const { data: recommended, success } = await request(
        "recommend/promotions/"
      );

      if (success) {
        if (recommended.items.length) visiblePost = [...recommended.items];
        else visiblePost = [...promotions.items];
      }

      const { data: pseudo, success: pseudoSuccess } = await request(
        "recommend/promotions/empty/"
      );

      console.log(pseudo)
      console.log(pseudoSuccess)
      if (pseudoSuccess) pseudoItems = [...pseudo.items];
    } else visiblePost = [...promotions.items];

    next(vm => {
      vm.posts = [...visiblePost];
      vm.pseudoPosts = [...pseudoItems];
    });
  }
};
