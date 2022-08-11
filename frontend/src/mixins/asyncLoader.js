export default {
  data() {
    return {
      delay: null
    };
  },
  methods: {
    timeout(ms = 1000) {
      return new Promise(resolve => {
        this.delay = setTimeout(resolve, ms);
      });
    }
  },
  beforeDestroy() {
    clearTimeout(this.delay);
  }
};
