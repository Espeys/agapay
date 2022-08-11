export default {
  props: {
    close: Boolean,
    width: {
      type: String,
      default: "600px"
    },
    width: {
      type: String,
      default: "600px"
    },
    height: String,
    cardClass: String,
    loading: Boolean
  },
  data() {
    return {
      isVisible: false,
      resolve: null
    };
  },
  methods: {
    showDialog() {
      this.isVisible = true;
      return new Promise(resolve => (this.resolve = resolve));
    },
    confirm() {
      this.resolve(true);
      this.isVisible = false;
    },
    cancel() {
      this.resolve(false);
      this.isVisible = false;
    }
  },
  watch: {
    isVisible(newValue) {
      if (!newValue) this.$emit("close-dialog", newValue);
    }
  }
};
