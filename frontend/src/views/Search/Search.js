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
      filterViews: "",
      filters: [
        { label: "All", value: "" },
        { label: "Status", value: "status" },
        { label: "Promotions", value: "promotion" },
        { label: "Requesting help", value: "request" },
        { label: "Offering help", value: "offer" }
      ],
      cacheFilterViewsData: "",
      posts: [],
      reportedSlug: "",
      supportSlug: ""
    };
  },
  computed: {},
  methods: {
    showFilters() {
      this.$refs.postFilters.showDialog();
    },
    onCloseDialog() {
      this.filterViews = this.cacheFilterViewsData;
    },
    onClear() {
      this.filterViews = this.cacheFilterViewsData = "";
      this.$router.push({ name: "Home" });
      this.$refs.postFilters.cancel();
    },
    onApply() {
      this.cacheFilterViewsData = this.filterViews;

      if (!this.filterViews) this.$router.push({ name: "Home" });
      else
        this.$router.push({
          name: "Home",
          query: { categories: this.filterViews }
        });
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
  watch: {
    "$route.query"(newValue, oldValue) {
      this.$router.go();
    }
  },
  mounted() {
    const { categories = "" } = this.$route.query;
    const postFilters = this.filters.map(filter => filter.value);

    if (postFilters.includes(categories))
      this.filterViews = this.cacheFilterViewsData = categories;
    else this.filterViews = "";
  },
  async beforeRouteEnter(to, from, next) {
    const { data } = await store.dispatch("post/getPosts", {
      q: to.query.keyword,
      order_values: -1
    });

    const { data: posts } = await request("accounts/profile/search/", {
      q: to.query.keyword,
      order_values: -1
    });

    next(vm => {
      vm.posts = [...data.items];
    });
  }
};
