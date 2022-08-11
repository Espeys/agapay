import {
  BasePost,
  AdsTrendsColumn,
  StickySideSection,
  ReportDialog,
  SupportDialog
} from "@/views/components";

import { formMixins, asyncLoader } from "@/mixins";

import store from "@/store";
export default {
  components: {
    BasePost,
    AdsTrendsColumn,
    StickySideSection,
    ReportDialog,
    SupportDialog
  },
  mixins: [formMixins, asyncLoader],
  props: {
    slug: String
  },

  data() {
    return {
      postDetails: {},
      commentsList: [],
      reportedSlug: "",
      supportSlug: ""
    };
  },
  methods: {
    async deletePost(slug, index) {
      const dialogResponse = await this.$root.deletePost();

      if (!dialogResponse) return;
      const { success } = await this.$store.dispatch("post/deletePost", {
        slug
      });
      if (success) this.$router.push({ name: "Home" });
    },
    async bookmarkPost(slug, isSaved) {
      let action = "post/unsavePost";

      if (!isSaved) action = "post/savePost";

      const response = await this.$store.dispatch(action, {
        slug
      });

      const { success, data } = response;

      if (success) this.postDetails = { ...data };
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
    const { data: details } = await store.dispatch("post/getPosts", {
      slug: to.params.slug
    });

    const { data: comments } = await store.dispatch(
      "post/getPostComments",
      to.params.slug
    );

    next(vm => {
      vm.postDetails = { ...details };

      vm.commentsList = [...comments.items];

      const { is_liked = false, censorship = false } = details;

      vm.$refs.post.populatePostDetails({
        comments: vm.commentsList,
        is_liked,
        censorship
      });
    });
  },
  watch: {
    "$route.params"() {
      this.$router.go();
    }
  }
};
