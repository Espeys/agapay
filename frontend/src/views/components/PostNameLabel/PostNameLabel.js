export default {
  props: {
    author: Object,
    anonymous: Boolean
  },
  computed: {
    user() {
      return this.$store.state.auth.user;
    }
  }
};
