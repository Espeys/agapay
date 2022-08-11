export default {
  props: {
    loading: Boolean
  },
  data() {
    return {
      supportReasons: [
        "Emotional",
        "Need of Urgent Support",
        "Self-harm",
        "Suicide",
        "Sensitive Content"
      ],
      supportData: {
        reason: "",
        description: "",
        slugs: []
      }
    };
  },
  computed: {
    following() {
      return this.$store.state.profile.following
        .filter(user => user.groups[0] !== "regular")
        .map(user => ({ label: user.full_name, value: user.slug }));
    }
  },
  methods: {
    showSupportDialog() {
      this.supportData.reason = this.supportData.description = "";
      this.supportData.slugs = [];
      this.$refs.supportPost.showDialog();
    },
    cancel() {
      this.$refs.supportPost.cancel();
    },
    submit() {
      this.$emit("click:support", this.supportData);
    }
  }
};
