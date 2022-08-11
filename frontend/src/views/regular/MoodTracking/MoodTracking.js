import {
  BasePost,
  AdsTrendsColumn,
  StickySideSection
} from "@/views/components";
import { VueReactionEmoji } from "vue-feedback-reaction";
import store from "@/store";

export default {
  components: {
    BasePost,
    VueReactionEmoji,
    AdsTrendsColumn,
    StickySideSection
  },
  data() {
    return {
      selectedYear: "2021",
      selectedMonth: "January",
      yearOptions: ["2021"],
      monthOptions: [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
      ],
      cacheData: {
        selectedYear: "2021",
        selectedMonth: "January"
      },
      posts: []
    };
  },
  computed: {
    currentMonth() {
      const now = new Date();

      return this.monthOptions[now.getMonth()];
    }
  },
  methods: {
    showFilters() {
      this.$refs.postFilters.showDialog();
    },
    onCloseDialog() {
      this.selectedYear = this.cacheData.selectedYear;
      this.selectedMonth = this.cacheData.selectedMonth;
    },
    onClear() {
      this.selectedYear = this.cacheData.selectedYear = "2021";
      this.selectedMonth = this.cacheData.selectedMonth = this.currentMonth;

      this.$router.push({ name: "Mood Tracking" });
      this.$refs.postFilters.cancel();
    },
    onApply() {
      this.cacheData.selectedYear = this.selectedYear;
      this.cacheData.selectedMonth = this.selectedMonth;

      this.$router.push({
        name: "Mood Tracking",
        query: { year: this.selectedYear, month: this.selectedMonth }
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
    }
  },
  mounted() {
    const { year = "2021", month = this.currentMonth } = this.$route.query;

    if (this.yearOptions.includes(year))
      this.selectedYear = this.cacheData.selectedYear = year;
    else this.selectedYear = "2021";
    if (this.monthOptions.includes(month))
      this.selectedMonth = this.cacheData.selectedMonth = month;
    else this.selectedMonth = this.currentMonth;
  },
  async beforeRouteEnter(to, from, next) {
    const { data } = await store.dispatch("post/getPosts", {
      qs_type: "diary",
      order_values: -1
    });

    next(vm => {
      vm.posts = [...data.items];
    });
  }
};
