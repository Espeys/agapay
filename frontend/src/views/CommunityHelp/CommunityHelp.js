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
  data() {
    return {
      filterViews: "",
      filters: [
        { label: "All", value: "" },
        { label: "Requesting help", value: "request" },
        { label: "Offering help", value: "offer" }
      ],
      helpType: "service",
      helpOptions: [
        { label: "All", value: "" },
        { label: "Goods", value: "good" },
        { label: "Time", value: "time" },
        { label: "Services", value: "service" },
        { label: "Information", value: "information" },
        { label: "Others", value: "other" }
      ],
      cacheData: {
        filterViews: "",
        helpType: "service"
      },
      posts: [],
      reportedSlug: "",
      supportSlug: ""
    };
  },

  methods: {
    showFilters() {
      this.$refs.postFilters.showDialog();
      this.setCacheData();
    },
    setCacheData() {
      this.cacheData.filterViews = this.filterViews;
      this.cacheData.helpType = this.helpType;
    },
    changeData(value, name) {
      if (name === "filters") this.filterViews = value;
      else this.helpType = value;
    },
    onCloseDialog() {
      this.filterViews = this.cacheData.filterViews;
      this.helpType = this.cacheData.helpType;
    },
    onClear() {
      this.filterViews = "";
      this.helpType = "service";
      this.setCacheData();
      this.$refs.postFilters.cancel();
    },
    onApply() {
      this.setCacheData();
      this.$refs.postFilters.confirm();
    },
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
    const { data: offer } = await store.dispatch("post/getPosts", {
      filter: JSON.stringify({ item_type: "offer" }),
      order_values: -1
    });

    const { data: request } = await store.dispatch("post/getPosts", {
      filter: JSON.stringify({ item_type: "request" }),
      order_values: -1
    });

    next(vm => {
      vm.posts = [...offer.items, ...request.items].sort(
        (a, b) => -a.created_at.localeCompare(b.created_at)
      );
    });
  }
};
