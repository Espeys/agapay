export default {
  props: {
    loading: Boolean
  },
  data() {
    return {
      reportReasons: [
        "False Information",
        "Spam",
        "Hate Speech",
        "Terrorism",
        "Harassment / Bullying",
        "Violence",
        "Racism",
        "Nudity"
      ],
      reportData: {
        reason: "",
        description: ""
      }
    };
  },
  methods: {
    showReportDialog() {
      this.reportData.reason = this.reportData.description = "";
      this.$refs.reportPost.showDialog();
    },
    cancel() {
      this.$refs.reportPost.cancel();
    },
    submit() {
      this.$emit("click:report", this.reportData);
    }
  }
};
